import sys

__author__ = 'Robin Keunen', 'Pierre Vyncke'

from src.misc import add_to_class
import src.ast as ast

TY_INT = "TY_INT"
TY_FLOAT = "TY_FLOAT"
TY_BOOL = "TY_BOOL"
TY_STRING = "TY_STRING"
TY_FUNC = "TY_FUNC"
TY_VOID = "TY_VOID"
TY_RT = "TY_RT"


class Environment(object):
    """
    Keeps track of the variables and functions in the scope
    and their type
    """

    def __init__(self, non_local=None, defun_block=False):
        self.local = {}
        self.non_local = non_local
        self.defun_block = defun_block
        if defun_block:
            self.closed_variable = {}

    def add(self, name, data):
        self.local[name] = data

    def get(self, name):
        if name in self.local:
            return self.local[name]
        elif self.non_local is not None and name in self.non_local:
            if self.defun_block:
                self.closed_variable[name] = self.non_local[name]
            return self.non_local[name]
        else:
            raise NameError

    def copy(self):
        obj_copy = Environment()
        obj_copy.local = self.local.copy()
        obj_copy.non_local = self.non_local.copy()


@add_to_class(ast.ASTNode)
def type_check(self, **kw):
    raise NotImplementedError


@add_to_class(ast.Statement_sequence)
def type_check(self, **kw):
    pass


@add_to_class(ast.Declaration)
def generate_class(self):
    pass


@add_to_class(ast.Assignment)
def type_check(self, **kw):
    pass


@add_to_class(ast.Return)
def type_check(self, **kw):
    pass


@add_to_class(ast.Funcall)
def type_check(self, **kw):
    pass


@add_to_class(ast.Print)
def type_check(self, **kw):
    pass


@add_to_class(ast.If)
def type_check(self, **kw):
    pass


@add_to_class(ast.Elif)
def type_check(self, **kw):
    pass


@add_to_class(ast.Else)
def type_check(self, **kw):
    pass


@add_to_class(ast.While)
def type_check(self, **kw):
    pass


@add_to_class(ast.Fundef)
def type_check(self, **kw):
    pass


@add_to_class(ast.Prototype)
def type_check(self, **kw):
    pass


_allowed = {
    ('NOT', TY_BOOL),
    (TY_BOOL,   'AND', TY_BOOL),
    (TY_BOOL,   'OR', TY_BOOL),
    (TY_INT,    'EQ', TY_INT),
    (TY_FLOAT,  'EQ', TY_FLOAT),
    (TY_BOOL,   'EQ', TY_BOOL),
    (TY_STRING, 'EQ', TY_STRING),
    (TY_FUNC,   'EQ', TY_FUNC),
    (TY_VOID,   'EQ', TY_VOID),
    (TY_RT,     'EQ', TY_RT),
    (TY_INT,    'NEQ', TY_INT),
    (TY_FLOAT,  'NEQ', TY_FLOAT),
    (TY_BOOL,   'NEQ', TY_BOOL),
    (TY_STRING, 'NEQ', TY_STRING),
    (TY_FUNC,   'NEQ', TY_FUNC),
    (TY_VOID,   'NEQ', TY_VOID),
    (TY_RT,     'NEQ', TY_RT),
    (TY_INT,    'LEQ', TY_INT),
    (TY_FLOAT,  'LEQ', TY_FLOAT),
    (TY_FLOAT,  'LEQ', TY_INT),
    (TY_INT,    'LEQ', TY_FLOAT),
    (TY_INT,    'GEQ', TY_INT),
    (TY_FLOAT,  'GEQ', TY_FLOAT),
    (TY_FLOAT,  'GEQ', TY_INT),
    (TY_INT,    'GEQ', TY_FLOAT),
    (TY_INT,    'LT', TY_INT),
    (TY_FLOAT,  'LT', TY_FLOAT),
    (TY_FLOAT,  'LT', TY_INT),
    (TY_INT,    'LT', TY_FLOAT),
    (TY_INT,    'GT', TY_INT),
    (TY_FLOAT,  'GT', TY_FLOAT),
    (TY_FLOAT,  'GT', TY_INT),
    (TY_INT,    'GT', TY_FLOAT),
    (TY_INT,    'PLUS', TY_INT),
    (TY_FLOAT,  'PLUS', TY_FLOAT),
    (TY_FLOAT,  'PLUS', TY_INT),
    (TY_INT,    'PLUS', TY_FLOAT),
    (TY_INT,    'MINUS', TY_INT),
    (TY_FLOAT,  'MINUS', TY_FLOAT),
    (TY_FLOAT,  'MINUS', TY_INT),
    (TY_INT,    'MINUS', TY_FLOAT),
    (TY_INT,    'TIMES', TY_INT),
    (TY_FLOAT,  'TIMES', TY_FLOAT),
    (TY_FLOAT,  'TIMES', TY_INT),
    (TY_INT,    'TIMES', TY_FLOAT),
    (TY_INT,    'DIVIDE', TY_INT),
    (TY_FLOAT,  'DIVIDE', TY_FLOAT),
    (TY_FLOAT,  'DIVIDE', TY_INT),
    (TY_INT,    'DIVIDE', TY_FLOAT),
    (TY_STRING, 'PLUS', TY_STRING),
    ('UMINUS', TY_INT),
    ('UNMINUS', TY_FLOAT),
}



@add_to_class(ast.Clause)
def type_check(self, **kw):
    self.environment = kw.get('environment', None)

    if self.op == 'NOT':
        ty_right, *t = self.right.type_check(**kw)
        combination = (self.op, ty_right)

    else:
        ty_left, *t = self.left.type_check(**kw)
        ty_right, *t = self.right.type_check(**kw)
        combination = (ty_left, self.op, ty_right)

    if TY_RT in combination:
        sys.stderr.write("line%d: warning: could not resolve type on operation %s"
                         % (self.lineno, self.op))
        return TY_BOOL,

    elif combination in _allowed:
        return TY_BOOL,

    else:
        if len(combination) == 1:
            raise TypeError("line %d: type %s invalid with '-', expect bool"
                            % (self.lineno, ty_right))
        else:
            raise TypeError("line %d: given %s and %s with op %s"
                            % (self.lineno, ty_left, ty_right, self.op))


@add_to_class(ast.Expression)
def type_check(self, **kw):
    self.environment = kw.get('environment', None)

    if self.op == 'UMINUS':
        ty_right, *t = self.right.type_check(**kw)
        combination = (self.op, ty_right)

    else:
        ty_left, *t = self.left.type_check(**kw)
        ty_right, *t = self.right.type_check(**kw)
        combination = (ty_left, self.op, ty_right)

    if TY_RT in combination:
        sys.stderr.write("line%d: warning: could not resolve type on operation %s"
                         % (self.lineno, self.op))
        return TY_RT,

    elif combination in _allowed:
        if len(combination) == 3 and ty_right != ty_left:
            return TY_FLOAT,
        else:
            return ty_right,

    else:
        if len(combination) == 1:
            raise TypeError("line %d: type %s invalid with '-', expect int of float"
                            % (self.lineno, ty_right))
        else:
            raise TypeError("line %d: given %s and %s with op %s"
                            % (self.lineno, ty_left, ty_right, self.op))


@add_to_class(ast.ID)
def type_check(self, **kw):
    self.environment = kw.get('environment', None)
    try:
        return self.environment.get(self.name)
    except NameError:
        raise NameError("line%d: name error, %s is not defined."
                        % (self.lineno, self.name))


@add_to_class(ast.Vinteger)
def type_check(self, **kw):
    return TY_INT,


@add_to_class(ast.Vfloat)
def type_check(self, **kw):
    return TY_FLOAT,


@add_to_class(ast.Vboolean)
def type_check(self, **kw):
    return TY_BOOL,


@add_to_class(ast.Vstring)
def type_check(self, **kw):
    return TY_STRING, len(self.data)


@add_to_class(ast.Map)
def type_check(self, **kw):
    pass


@add_to_class(ast.Pair)
def type_check(self, **kw):
    pass