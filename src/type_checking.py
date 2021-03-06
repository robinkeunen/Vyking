import sys

__author__ = 'Robin Keunen', 'Pierre Vyncke'

from src.misc import add_to_class, decorator
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

class Environment(object):
    """
    Keeps track of the variables and functions in the scope
    and their type
    """

    def __init__(self, non_local=None, defun_block=False):
        self.local = {}
        if non_local is None:
            self.non_local = {}
        else:
            self.non_local = non_local
        self.defun_block = defun_block
        if defun_block:
            self.closed_variable = {}

    def __str__(self):
        rep = str(self.local) + '\n'
        rep += 'up:' + str(self.non_local) + '\n'
        return rep

    def assign(self, name, data):
        """
        TODO
        :param name:
        :param data:
        """
        if name in self.local:
            self.local[name] = data
        elif self.non_local is not None \
                and name in self.non_local:
            self.non_local.assign(name, data)
        else:
            self.local[name] = data

    def get(self, name):
        """
        Get the type from its name
        :param name: its name
        :return: the type
        """
        if name in self.local:
            return self.local[name]
        elif name in self.non_local:
            # remember closed names
            if self.defun_block:
                self.closed_variable[name] = self.non_local.get(name)
            return self.non_local.get(name)
        else:
            return None

    def copy(self):
        """
        Copy the object

        """
        obj_copy = Environment()
        obj_copy.local = self.local.copy()
        obj_copy.non_local = self.non_local.copy()

    def __contains__(self, name):
        if name in self.local:
            return True
        elif name in self.non_local:
            return True
        else:
            return False

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.assign(name, value)


_trace_level = 0


@decorator
def trace(f):
    """
    TODO
    :param f:
    :return:
    """
    indent = '    '

    def _f(self, **args):
        """
        TODO
        :param self:
        :param args:
        :return:
        """
        global _trace_level
        rep_args = args.copy()
        rep_args.pop('environment', None)
        signature = '%s.tc(%s)' % (self.type, rep_args)
        print('%s--> %s' % (_trace_level * indent, signature))
        _trace_level += 1
        try:
            result = f(self, **args)
            if result is not None:
                print('%s<-- %s == %s' % ((_trace_level - 1) * indent,
                                          self.type, result))
        finally:
            _trace_level -= 1
        return result

    _trace_level = 0
    return _f


class VykingException(Exception):
    pass


@add_to_class(ast.ASTNode)
def set_environment(self, **kw):
    """
        TODO
    :param self:
    :param kw:
    :raise:
    """
    self.environment = kw.get('environment', None)
    if self.environment is None:
        raise VykingException("Environnement is not defined")


@add_to_class(ast.ASTNode)
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    raise NotImplementedError


@add_to_class(ast.Statement_sequence)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    entry_point = kw.pop('entry_point', False)
    if entry_point:
        self.environment = Environment()
    else:
        self.set_environment(**kw)

    kw['environment'] = self.environment
    for stmt in self.get_children():
        stmt.type_check(**kw)

    return None


@add_to_class(ast.Assignment)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    ty_rhs = self.right.type_check(**kw)
    self.environment.assign(self.left.get_name(), ty_rhs)
    return None


@add_to_class(ast.Return)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    # get return constraints
    constraint = kw.get('return_constraint', None)
    ty, *t = self.value.type_check(**kw)
    self.ret_ty = ty
    if self.value is None and constraint == TY_VOID:
        return None
    if constraint != ty:
        raise TypeError("line %d: expected %s return type, given %s"
                        % (self.lineno, constraint, ty))
    return None


@add_to_class(ast.Funcall)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    # get function return type
    tp = self.environment.get(self.name.get_name())
    if tp is None:
        raise NameError("line %d: %s is not defined"
                        % (self.lineno, self.name))
    ty = tp[0]
    if ty == TY_RT:
        return TY_RT,
    if ty != TY_FUNC:
        raise TypeError("line %d: %s is not a callable"
                        % (self.lineno, self.name))

    # prototype is (return type, [args' type])
    prototype = tp[1]
    ret_ty, args_ty = prototype

    # check args number and type

    if len(args_ty) != len(self.args):
        raise TypeError(
            "line %d: %s takes %d arguments, given %d."
            % (self.lineno, self.name, len(args_ty), len(self.args)))
    for arg_ty, arg in zip(args_ty, self.args):
        expected_type = arg_ty[0]
        given_ty, *t = arg.type_check(**kw)
        if expected_type != given_ty:
            raise TypeError("line %d: expected %s arg type, given %s"
                            % (self.lineno, expected_type, given_ty))
    return ret_ty,


@add_to_class(ast.Print)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    self.ty = self.clause.type_check(**kw)
    return None


@add_to_class(ast.If)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    ty_clause, *t = self.clause.type_check(**kw)
    if ty_clause != TY_BOOL:
        raise TypeError('line %d: "if" clause must be a bool, given %s'
                        % (self.lineno, ty_clause))

    # suite
    nested_scope = Environment(self.environment)
    kw['environment'] = nested_scope
    self.suite.type_check(**kw)

    # closure
    if self.if_closure is not None:
        kw['environment'] = self.environment
        self.if_closure.type_check(**kw)

    return None


@add_to_class(ast.Elif)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    ty_clause, *t = self.clause.type_check(**kw)
    if ty_clause != TY_BOOL:
        raise TypeError('line %d: "elif" clause must be a bool, given %s'
                        % (self.lineno, ty_clause))

    # suite
    nested_scope = Environment(self.environment)
    kw['environment'] = nested_scope
    self.suite.type_check(**kw)

    # closure
    if self.if_closure is not None:
        kw['environment'] = self.environment
        self.if_closure.type_check(**kw)

    return None


@add_to_class(ast.Else)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)

    nested_scope = Environment(self.environment)
    kw['environment'] = nested_scope
    self.suite.type_check(**kw)

    return None


@add_to_class(ast.While)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    ty_clause, *t = self.clause.type_check(**kw)
    if ty_clause != TY_BOOL:
        raise TypeError('line %d: "while" clause must be a bool, given %s'
                        % (self.lineno, ty_clause))

    # suite
    nested_scope = Environment(self.environment)
    kw['environment'] = nested_scope
    self.suite.type_check(**kw)

    return None


@add_to_class(ast.Fundef)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    # prototype : (return type, [args type])
    nested_scope = Environment(self.environment, defun_block=True)
    signature = self.prototype.type_check(environment=nested_scope)
    self.environment.assign(self.prototype.get_name(),
                            (TY_FUNC, signature))
    if self.suite is not None:
        self.suite.type_check(environment=nested_scope,
                              return_constraint=signature[0])

    return None


@add_to_class(ast.Prototype)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)

    def helper(tp):
        if tp[0] == TY_FUNC:
            sys.stderr.write("Warning line %d: no static check of functions "
                             "passed as argument\n" % (self.lineno))
            return TY_RT,
        else:
            return tp[0],

    if self.ty_params[0] is None:
        signature = (self.return_ty, tuple())
    else:
        signature = (self.return_ty, tuple(helper(tp) for tp in self.ty_params))
        for arg in self.ty_params:
            ty, name = arg
            if ty == TY_FUNC:
                sys.stderr.write("Warning line %d: no static check of functions "
                                 "passed as argument\n" % (self.lineno))
                self.environment.assign(name.get_name(), (TY_RT, TY_FUNC))
            else:
                self.environment.assign(name.get_name(), (ty,))
    self.signature = signature
    return signature


_allowed = {
    ('NOT', TY_BOOL),
    (TY_BOOL, 'AND', TY_BOOL),
    (TY_BOOL, 'OR', TY_BOOL),
    (TY_INT, 'EQ', TY_INT),
    (TY_FLOAT, 'EQ', TY_FLOAT),
    (TY_FLOAT, 'EQ', TY_FLOAT),
    (TY_FLOAT, 'EQ', TY_INT),
    (TY_BOOL, 'EQ', TY_BOOL),
    (TY_STRING, 'EQ', TY_STRING),
    (TY_FUNC, 'EQ', TY_FUNC),
    (TY_VOID, 'EQ', TY_VOID),
    (TY_RT, 'EQ', TY_RT),
    (TY_INT, 'NEQ', TY_INT),
    (TY_FLOAT, 'NEQ', TY_FLOAT),
    (TY_BOOL, 'NEQ', TY_BOOL),
    (TY_STRING, 'NEQ', TY_STRING),
    (TY_FUNC, 'NEQ', TY_FUNC),
    (TY_VOID, 'NEQ', TY_VOID),
    (TY_RT, 'NEQ', TY_RT),
    (TY_INT, 'LEQ', TY_INT),
    (TY_FLOAT, 'LEQ', TY_FLOAT),
    (TY_FLOAT, 'LEQ', TY_INT),
    (TY_INT, 'LEQ', TY_FLOAT),
    (TY_INT, 'GEQ', TY_INT),
    (TY_FLOAT, 'GEQ', TY_FLOAT),
    (TY_FLOAT, 'GEQ', TY_INT),
    (TY_INT, 'GEQ', TY_FLOAT),
    (TY_INT, 'LT', TY_INT),
    (TY_FLOAT, 'LT', TY_FLOAT),
    (TY_FLOAT, 'LT', TY_INT),
    (TY_INT, 'LT', TY_FLOAT),
    (TY_INT, 'GT', TY_INT),
    (TY_FLOAT, 'GT', TY_FLOAT),
    (TY_FLOAT, 'GT', TY_INT),
    (TY_INT, 'GT', TY_FLOAT),
    (TY_INT, 'PLUS', TY_INT),
    (TY_FLOAT, 'PLUS', TY_FLOAT),
    (TY_FLOAT, 'PLUS', TY_INT),
    (TY_INT, 'PLUS', TY_FLOAT),
    (TY_INT, 'MINUS', TY_INT),
    (TY_FLOAT, 'MINUS', TY_FLOAT),
    (TY_FLOAT, 'MINUS', TY_INT),
    (TY_INT, 'MINUS', TY_FLOAT),
    (TY_INT, 'TIMES', TY_INT),
    (TY_FLOAT, 'TIMES', TY_FLOAT),
    (TY_FLOAT, 'TIMES', TY_INT),
    (TY_INT, 'TIMES', TY_FLOAT),
    (TY_INT, 'DIVIDE', TY_INT),
    (TY_FLOAT, 'DIVIDE', TY_FLOAT),
    (TY_FLOAT, 'DIVIDE', TY_INT),
    (TY_INT, 'DIVIDE', TY_FLOAT),
    (TY_STRING, 'PLUS', TY_STRING),
    ('UMINUS', TY_INT),
    ('UNMINUS', TY_FLOAT),
}


@add_to_class(ast.Clause)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.environment = kw.get('environment', None)

    if self.op == 'NOT':
        ty_right, *t = self.right.type_check(**kw)
        combination = (self.op, ty_right)

    else:
        ty_left, *t = self.left.type_check(**kw)
        ty_right, *t = self.right.type_check(**kw)
        combination = (ty_left, self.op, ty_right)

    self.type = combination

    if TY_RT in combination:
        sys.stderr.write("line %d: warning: could not resolve type on operation %s\n"
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
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)

    if self.op == 'UMINUS':
        ty_right, *t = self.right.type_check(**kw)
        combination = (self.op, ty_right)

    else:
        ty_left, *t = self.left.type_check(**kw)
        ty_right, *t = self.right.type_check(**kw)
        combination = (ty_left, self.op, ty_right)

    self.type = combination

    if TY_RT in combination:
        sys.stderr.write("line%d: warning: could not resolve type on operation %s\n"
                         % (self.lineno, self.op))
        if combination[0] != TY_RT:
            return combination[0],
        elif len(combination) == 3 and combination[2] != 3:
            return combination[2],
        else:
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
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    self.set_environment(**kw)
    res = self.environment.get(self.name)
    if res is None:
        raise NameError("line%d: name error, %s is not defined."
                        % (self.lineno, self.name))
    else:
        return res


@add_to_class(ast.Vinteger)
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    return TY_INT,


@add_to_class(ast.Vfloat)
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    return TY_FLOAT,


@add_to_class(ast.Vboolean)
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    return TY_BOOL,


@add_to_class(ast.Vstring)
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    return TY_STRING, len(self.value)


@add_to_class(ast.Map)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    pass


@add_to_class(ast.Pair)
@trace
def type_check(self, **kw):
    """
    checks if the type of the children is consistent with the semantics of the node
    :param kw: dictionnary carrying inherited attributes
    :raise: TypeError if types don't match with the semantics
    """
    pass
