# Copyright (c) Matt Haggard.
# See LICENSE for details.

from norm.orm.base import classInfo, Property

from collections import defaultdict
from itertools import product
from datetime import date, datetime


class CompileError(Exception):
    pass



class Query(object):
    """
    I am a query for a set of objects.  Pass me to L{IOperator.query}.
    """


    def __init__(self, select, *constraints, **kwargs):
        """
        @param select: Class(es) to return in the result.  This may either be
            a single class or a list/tuple of classes.
        @param constraints: A L{Comparison} or other compileable expression.

        @param kwargs:
            joins
        """
        if type(select) not in (list, tuple):
            select = (select,)
        self.select = select
        if constraints:
            self.constraints = And(*constraints)
        else:
            self.constraints = None
        self.joins = kwargs.pop('joins', None) or []
        self._classes = []
        self._props = []
        self._process()


    def _process(self):
        self._classes = []
        self._props = []
        for item in self.select:
            info = classInfo(item)
            keys = sorted(info.attributes.values())
            self._props.extend(keys)
            self._classes.append(item)


    def properties(self):
        """
        Get a tuple of the Properties that will be returned by the query.
        """
        return tuple(self._props)


    def classes(self):
        """
        Return a list of classes involved in the query.
        """
        return self._classes


    def find(self, select, constraints=None, joins=None):
        """
        Search for another kind of object with additional constraints.
        """
        all_constraints = [x for x in [self.constraints, constraints] if x]
        joins = joins or []
        return Query(select, *all_constraints, joins=self.joins + joins)



def _aliases(pool='abcdefghijklmnopqrstuvwxyz'):
    for i in range(1, 255):
        for item in product(pool, repeat=i):
            yield ''.join(item)



class State(object):
    """
    Compilation state and life-line to the whole compilation process.
    """

    compiler = None


    def __init__(self):
        pool = _aliases()
        self._aliases = defaultdict(lambda:next(pool))
        self.classes = []


    def compile(self, thing):
        return self.compiler.compile(thing, self)


    def tableAlias(self, cls):
        """
        Return a name that can be used (repeatedly) as an alias for a class'
        table.
        """
        alias = self._aliases[cls]
        if cls not in self.classes:
            self.classes.append(cls)
        return alias



class Compiler(object):
    """
    I compile "things" into "other things" (most typically, objects into SQL)
    """


    def __init__(self, fallbacks=None):
        self.classes = {}
        self.fallbacks = fallbacks or []


    def when(self, *cls):
        def deco(f):
            for c in cls:
                self.classes[c] = f
            return f
        return deco


    def compile(self, thing, state=None):
        state = state or State()
        if not state.compiler:
            state.compiler = self
        cls = thing.__class__
        classes = [cls] + list(cls.__bases__)
        for c in classes:
            if c in self.classes:
                return self.classes[c](thing, state)
        for fallback in self.fallbacks:
            try:
                return fallback.compile(thing, state)
            except CompileError:
                pass
        raise CompileError("I don't know how to compile %r" % (thing,))


compiler = Compiler()


@compiler.when(Query)
def compile_Query(query, state):
    # select
    props = query.properties()
    columns = []
    select_args = []
    for prop in props:
        s, q = state.compile(prop)
        columns.append(s)
        select_args.extend(q)
    select_clause = ['SELECT %s' % (','.join(columns),)]

    # where
    where_clause = []
    where_args = []
    constraints = query.constraints
    if constraints:
        s, a = state.compile(constraints)
        where_clause = ['WHERE %s' % (s,)]
        where_args.extend(a)

    # from
    from_args = []
    tables = []
    joins = []
    join_args  = []
    join_classes = []

    joins_per_table = defaultdict(lambda:[])

    for j in query.joins:        
        # figure out which tables are involved in this left join for a clue
        # on where to put the left join.
        tmp_state = State()
        compiler.compile(j.on, tmp_state)
        classes = tmp_state.classes
        classes.remove(j.cls)
        
        join_classes.append(j.cls)
        s, a = state.compile(j)
        joins.append(s)
        join_args.extend(a)

        joins_per_table[classes[0]].append((j.cls,s,a))

    classes = [x for x in state.classes]
    for j in join_classes:
        if j in classes:
            classes.remove(j)

    for cls in classes:
        s, a = state.compile(Table(cls))
        slist = [s]
        alist = list(a)
        classes_in_this_from = [cls]
        while classes_in_this_from:
            this_cls = classes_in_this_from.pop(0)
            # append any joins that depend on this class
            for jcls,js,ja in joins_per_table[this_cls]:
                slist.append(js)
                alist.extend(ja)
                classes_in_this_from.append(jcls)
        tables.append(' '.join(slist))
        from_args.extend(alist)

    from_clause = ['FROM %s' % (','.join(tables)),]    

    sql = ' '.join(select_clause + from_clause + where_clause)
    args = tuple(select_args + from_args + where_args)
    return sql, args



@compiler.when(Property)
def compile_Property(x, state):
    alias = state.tableAlias(x.cls)
    return '%s.%s' % (alias, x.column_name), ()



class Table(object):
    """
    I wrap an ORM class and compile to an aliased table.
    """

    def __init__(self, cls):
        self.cls = cls


@compiler.when(Table)
def compile_Table(table, state):
    info = classInfo(table.cls)
    return '%s AS %s' % (info.table, state.tableAlias(table.cls)), ()


@compiler.when(str, bytes, int, bool, date, datetime)
def compile_str(x, state):
    return ('?', (x,))


@compiler.when(type(None))
def compile_None(x, state):
    return ('NULL', ())



class Comparison(object):

    op = None

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def __eq__(self, other):
        print('Comparison.__eq__', other)


class Eq(Comparison):
    op = '='


class Neq(Comparison):
    op = '!='


class Gt(Comparison):
    op = '>'


class Gte(Comparison):
    op = '>='


class Lt(Comparison):
    op = '<'


class Lte(Comparison):
    op = '<='


@compiler.when(Comparison)
def compile_Comparison(x, state):
    left, left_args = state.compile(x.left)
    right, right_args = state.compile(x.right)
    return ('%s %s %s' % (left, x.op, right), left_args + right_args)


def compile_Comparison_null(x, null_op, state):
    op = x.op
    left = ''
    left_args = ()
    right = ''
    right_args = ()
    if x.left is None:
        left = 'NULL'
        op = null_op
    else:
        left, left_args = state.compile(x.left)
    if x.right is None:
        right = 'NULL'
        op = null_op
    else:
        right, right_args = state.compile(x.right)
    return ('%s %s %s' % (left, op, right), left_args + right_args)


@compiler.when(Eq)
def compile_Eq(x, state):
    return compile_Comparison_null(x, 'IS', state)


@compiler.when(Neq)
def compile_Neq(x, state):
    return compile_Comparison_null(x, 'IS NOT', state)



class LogicalBinaryOp(object):

    join = None

    def __init__(self, *items):
        self.items = items

class And(LogicalBinaryOp):
    join = ' AND '


class Or(LogicalBinaryOp):
    join = ' OR '


@compiler.when(LogicalBinaryOp)
def compile_Joiner(x, state):
    parts = []
    args = ()
    for item in x.items:
        sql, item_args = state.compile(item)
        parts.append(sql)
        args = args + item_args

    return ('('+x.join.join(parts)+')', args)


class Join(object):

    oper = 'JOIN'

    def __init__(self, cls, on):
        self.cls = cls
        self.on = on



class LeftJoin(Join):

    oper = 'LEFT JOIN'


@compiler.when(Join)
def compile_Join(x, state):
    table = classInfo(x.cls).table
    alias = state.tableAlias(x.cls)
    on_sql, on_args = state.compile(x.on)
    return ('%s %s AS %s ON %s' % (x.oper, table, alias, on_sql), on_args)





