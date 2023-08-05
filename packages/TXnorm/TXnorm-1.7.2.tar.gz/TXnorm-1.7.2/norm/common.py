# Copyright (c) Matt Haggard.
# See LICENSE for details.

from zope.interface import implements
from zope.interface.declarations import implementer
from twisted.internet import defer

from functools import partial

from collections import deque, defaultdict

from norm.interface import IAsyncCursor, IRunner, IPool


@implementer(IAsyncCursor)
class BlockingCursor(object):
    """
    I wrap a single DB-API2 db cursor in an asynchronous api.
    """

    def __init__(self, cursor):
        self.cursor = cursor


    def execute(self, sql, params=()):
        return defer.maybeDeferred(self.cursor.execute, sql, params)


    def fetchone(self):
        return defer.maybeDeferred(self.cursor.fetchone)


    def fetchall(self):
        return defer.maybeDeferred(self.cursor.fetchall)


    def lastRowId(self):
        return defer.succeed(self.cursor.lastrowid)


    def close(self):
        return defer.maybeDeferred(self.cursor.close)


@implementer(IRunner)
class BlockingRunner(object):
    """
    I wrap a single DB-API2 db connection in an asynchronous api.
    """

    cursorFactory = BlockingCursor


    def __init__(self, conn):
        """
        @param conn: A synchronous database connection.
        """
        self.conn = conn


    def runQuery(self, qry, params=()):
        return self.runInteraction(self._runQuery, qry, params)
    

    def _runQuery(self, cursor, qry, params):
        d = cursor.execute(qry, params)
        d.addCallback(lambda _: cursor.fetchall())
        return d


    def runOperation(self, qry, params=()):
        return self.runInteraction(self._runOperation, qry, params)


    def _runOperation(self, cursor, qry, params):
        return cursor.execute(qry, params)


    def runInteraction(self, function, *args, **kwargs):
        cursor = self.cursorFactory(self.conn.cursor())
        d = defer.maybeDeferred(function, cursor, *args, **kwargs)
        d.addCallback(self._commit)
        d.addErrback(self._rollback)
        return d


    def _commit(self, result):
        self.conn.commit()
        return result


    def _rollback(self, result):
        self.conn.rollback()
        return result


    def close(self):
        return defer.maybeDeferred(self.conn.close)


@implementer(IRunner)
class ConnectionPool(object):


    db_scheme = None


    def __init__(self, pool=None):
        self.pool = pool or NextAvailablePool()
        self._makeConnection = None


    def setConnect(self, func, *args, **kwargs):
        """
        Set the function to be called to make a db connection.
        """
        self._makeConnection = partial(func, *args, **kwargs)


    def makeConnection(self):
        """
        Using the function previously set with L{setConnect}, make a new
        connection.
        """
        return defer.maybeDeferred(self._makeConnection)


    def add(self, conn):
        self.pool.add(conn)


    def runInteraction(self, function, *args, **kwargs):
        return self._runWithConn('runInteraction', function, *args, **kwargs)


    def runQuery(self, *args, **kwargs):
        return self._runWithConn('runQuery', *args, **kwargs)


    def runOperation(self, *args, **kwargs):
        return self._runWithConn('runOperation', *args, **kwargs)


    def _finish(self, result, conn):
        self.pool.done(conn)
        return result


    def _runWithConn(self, name, *args, **kwargs):
        d = self.pool.get()
        d.addCallback(self._startRunWithConn, name, *args, **kwargs)
        return d


    def _startRunWithConn(self, conn, name, *args, **kwargs):
        m = getattr(conn, name)
        d = m(*args, **kwargs)
        if self._makeConnection:
            d.addErrback(self._retryOnDisconnect, conn, name, args, kwargs)
        return d.addBoth(self._finish, conn)


    def _retryOnDisconnect(self, failure, conn, name, args, kwargs):
        """
        XXX UNTESTED
        """
        # check if it's the connection
        d = conn.runQuery('select 1')
        d.addCallbacks(
            self._connectionTestSucceeded,
            self._connectionTestFailed,
            callbackArgs=(failure,),
            errbackArgs=(conn, name, args, kwargs, failure),
        )
        return d


    def _connectionTestSucceeded(self, result, original_failure):
        """
        The connection is good; fail like you were going to.
        """
        return original_failure


    @defer.inlineCallbacks
    def _connectionTestFailed(self, result, bad_conn, name, args, kwargs,
                              original_failure):
        """
        The connection is bad, try the query again.
        """
        retval = original_failure
        try:
            new_conn = yield self.makeConnection()
            m = getattr(new_conn, name)
            retval = yield m(*args, **kwargs)
            self.pool.remove(bad_conn)
            self.pool.add(new_conn)
        except:
            pass
        defer.returnValue(retval)


    def close(self):
        dlist = []
        for item in self.pool.list():
            dlist.append(defer.maybeDeferred(item.close))
        return defer.gatherResults(dlist)        



@implementer(IPool)
class NextAvailablePool(object):
    """
    I give you the next available object in the pool.
    """

    def __init__(self):
        self._options = deque()
        self._all_options = []
        self._pending = deque()
        self._pending_removal = defaultdict(lambda:[])


    def add(self, option):
        self._options.append(option)
        self._all_options.append(option)
        self._fulfillNextPending()


    def remove(self, option):
        try:
            self._options.remove(option)
            self._all_options.remove(option)
            return defer.succeed(option)
        except ValueError:
            d = defer.Deferred()
            self._pending_removal[option].append(d)
            return d


    def get(self):
        d = defer.Deferred()
        self._pending.append(d)
        self._fulfillNextPending()
        return d


    def _fulfillNextPending(self):
        if self._pending and self._options:
            self._pending.popleft().callback(self._options.popleft())


    def done(self, option):
        if option in self._pending_removal:
            dlist = self._pending_removal.pop(option)
            map(lambda d: d.callback(option), dlist)
            self._all_options.remove(option)
            return
        self._options.append(option)
        self._fulfillNextPending()


    def list(self):
        return self._all_options





