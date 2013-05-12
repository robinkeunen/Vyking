# -----------------------------------------------------------------------------
# ast.py
# Nodes of the abstract syntax tree for the Vyking language.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------
import itertools
#from src import pydot


counter = itertools.count()


class ASTNode(object):
    """
    Abstract class for nodes of the syntax tree.
    Children must implement accept(ASTNodeVisitor)
    (Visitor design pattern)
    """

    def __init__(self, lineno, lexpos):
        self.type = None
        self.lineno = lineno
        self.lexpos = lexpos
        self.id = counter.__next__()

    def get_type(self):
        return self.type

    def get_children(self):
        """Returns a list of the node's children"""
        raise NotImplementedError("Should have implemented this")

    def make_tree_graph(self, dot=None, edgeLabels=True):
        """
        Makes a dot object to write subtree to output
        """
        if not dot: dot = pydot.Dot()
        dot.add_node(pydot.Node(self.id, label=self.type))
        label = edgeLabels and len(self.get_children()) - 1

        for i, c in enumerate(self.get_children()):
            if issubclass(c.__class__, ASTNode):
                c.make_tree_graph(dot=dot, edgeLabels=edgeLabels)
                edge = pydot.Edge(self.id, c.id)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
        return dot


class Statement_sequence(ASTNode):
    def __init__(self, statement_sequence, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "statement_sequence"
        self.statement_sequence = statement_sequence

    def __str__(self):
        result = ""
        for st in self.statement_sequence:
            result += str(st) + "\n"
        return result

    def get_children(self):
        return self.statement_sequence


class Statement(ASTNode):
    pass


class Assignment(Statement):
    def __init__(self, left, right, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "assignment"
        self.left = left
        self.right = right

    def __str__(self):
        return "(ASSIGN %s " % self.left + str(self.right) + ")"

    def get_children(self):
        return [self.left, self.right]


class Return(Statement):
    def __init__(self, value, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "return_statement"
        self.value = value

    def __str__(self):
        return "(RETURN %s)" % self.value

    def get_children(self):
        return [self.value]


class Funcall(Statement):
    def __init__(self, name, lineno, lexpos, args=None):
        super().__init__(lineno, lexpos)
        self.type = "funcall"
        self.name = name
        if args is None:
            self.args = []
        else:
            self.args = args

    def __str__(self):
        args_repr = "("
        for arg in self.args:
            args_repr += str(arg)
        args_repr += ")"
        return "(f:%s %s)" % (self.name, args_repr)

    def get_children(self):
        return [self.name, self.args]


class Print(Statement):
    def __init__(self, clause, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = 'print'
        self.clause = clause

    def __str__(self):
        return "(print %s)" % str(self.clause)

    def get_children(self):
        return [self.clause]


class If(Statement):
    def __init__(self, clause, suite, lineno, lexpos, if_closure=None):
        super().__init__(lineno, lexpos)
        self.type = "if_statement"
        self.clause = clause
        self.suite = suite
        self.if_closure = if_closure

    def __str__(self):
        if self.if_closure is None:
            return "(IF %s \n\t %s)" \
                   % (str(self.clause), str(self.suite))
        else:
            return "(IF %s \n\t %s %s)" \
                   % (str(self.clause), str(self.suite), str(self.if_closure))

    def get_children(self):
        return [self.clause, self.suite, self.if_closure]


class Elif(Statement):
    def __init__(self, clause, suite, lineno, lexpos, if_closure=None):
        super().__init__(lineno, lexpos)
        self.type = "elif_statement"
        self.clause = clause
        self.suite = suite
        self.if_closure = if_closure

    def __str__(self):
        if self.if_closure is None:
            return "(ELIF %s \n\t %s)" \
                   % (str(self.clause), str(self.suite))
        else:
            return "(ELIF %s \n\t %s %s)" \
                   % (str(self.clause), str(self.suite), str(self.if_closure))

    def get_children(self):
        return [self.clause, self.suite, self.if_closure]


class Else(Statement):
    def __init__(self, suite, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "else"
        self.suite = suite

    def __str__(self):
        return "(ELSE %s)" % str(self.suite)

    def get_children(self):
        return [self.suite]


class While(Statement):
    def __init__(self, clause, suite, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "while"
        self.clause = clause
        self.suite = suite

    def __str__(self):
        return "(WHILE %s \n %s)" % (str(self.clause), str(self.suite))

    def get_children(self):
        return [self.clause, self.suite]


class Fundef(Statement):
    def __init__(self, prototype, suite, lineno, lexpos):
        """

        :param name:
        :param suite:
        :param parameters:
        """
        super().__init__(lineno, lexpos)
        self.type = 'Fundef'
        self.prototype = prototype
        self.suite = suite

    def __str__(self):
        if self.suite is None:
            return "(EXTERN %s)" %(str(self.prototype))
        else:
            return "(DEFUN %s \n %s)" % (str(self.prototype), str(self.suite))

    def get_children(self):
        if self.suite is None:
            return [self.prototype]
        else:
            return [self.prototype, self.suite]


class Prototype(ASTNode):
    def __init__(self, return_ty, name, ty_params, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "prototype"
        self.return_ty = return_ty
        self.name = name
        self.ty_params = ty_params

    def __str__(self):
        parameters = "["
        for t, p in self.ty_params:
            parameters += "%s %s, " % (t, str(p))
        parameters = parameters[:-2] + "]"
        return "%s: %s %s" % (self.return_ty,
                              str(self.name),
                              parameters)

    def get_name(self):
        return self.name.get_name()

    def get_children(self):
        return [self.return_ty, self.name, self.ty_params]


class Clause(ASTNode):
    def __init__(self, left, op, right, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = 'clause'
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        if self.left is None:
            return "(%s %s)" % (self.op, self.right)
        else:
            return "(%s %s %s)" % (self.op, self.left, self.right)

    def get_children(self):
        return [self.left, self.right]


class Expression(ASTNode):
    def __init__(self, left, op, right, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "Expression"
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        if self.left is None:
            return "(%s %s)" % (self.op, self.right)
        else:
            return "(%s %s %s)" % (self.op, str(self.left), str(self.right))

    def get_children(self):
        return [self.left, self.right]


class Atom(ASTNode):
    pass


class Vinteger(Atom):
    def __init__(self, value, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT %d)" % self.value

    def get_children(self):
        return list()


class Vfloat(Atom):
    def __init__(self, value, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "FLOAT"
        self.value = value

    def __str__(self):
        return "(FLOAT %d)" % self.value

    def get_children(self):
        return list()


class ID(Atom):
    """
    Represents an ID in the AST, if value is not set,
    semantic analysis must check it has been assigned
    """

    def __init__(self, name, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "ID"
        self.name = name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_children(self):
        return list()


class Vstring(Atom):
    def __init__(self, data, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "string"
        self.value = data

    def __str__(self):
        return self.value

    def get_children(self):
        return list()


class Vboolean(Atom):
    def __init__(self, value, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.type = "boolean"
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return list()


class Map(Statement):
    def __init__(self, funcname, vlist, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.funcname = funcname
        self.vlist = vlist

    def __str__(self):
        return "(%s %s" % (self.funcname, str(self.vlist))

    def get_children(self):
        return [self.funcname, self.vlist]


class Pair(Atom):
    def __init__(self, head, tail, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.head = head
        self.tail = tail

    def __str__(self):
        return "[%s, %s]" % ( self.head, self.tail)

    def get_children(self):
        return [self.head, self.tail]

class Head(Atom):
    def __init__(self, pair, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.pair = pair

    def __str__(self):
        return "[Head : %s]" % (self.pair)

    def get_children(self):
        return [self.pair]

class Tail(Atom):
    def __init__(self, pair, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.pair = pair

    def __str__(self):
        return "[Tail : %s]" % (self.pair)

    def get_children(self):
        return [self.pair]

class Append(Atom):
    def __init__(self, pair1, pair2, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.pair1 = pair1
        self.pair2 = pair2

    def __str__(self):
        return "[Append : %s %s]" % (self.pair1, self.pair2)

    def get_children(self):
        return [self.pair1, self.pair2]

class Cons(Atom):
    def __init__(self, data, pair, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.data = data
        self.pair = pair

    def __str__(self):
        return "[Cons : %s %s]" % (self.data, self.pair)

    def get_children(self):
        return [self.data, self.pair]

class Map(Atom):
    def __init__(self, id, pair, lineno, lexpos):
        super().__init__(lineno, lexpos)
        self.id = id
        self.pair = pair

    def __str__(self):
        return "[Map : %s %s]" % (self.id, self.pair)

    def get_children(self):
        return [self.id, self.pair]