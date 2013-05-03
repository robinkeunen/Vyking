# -----------------------------------------------------------------------------
# ast.py
# Nodes of the abstract syntax tree for the Vyking language.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------
import itertools
from src import pydot


counter = itertools.count()


class ASTNode(object):
    """
    Abstract class for nodes of the syntax tree.
    Children must implement accept(ASTNodeVisitor)
    (Visitor design pattern)
    """
    id_counter = 0

    #def __init__(self, lineno, lexpos):
    def __init__(self):
        self.type = None
        #self.lineno = lineno
        #self.lexpos = lexpos
        self.id = counter.__next__()

    # accept visitor (not implemented yet)
    def accept(self):
        raise NotImplementedError("Should have implemented this")

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


class Statement(ASTNode):
    pass


class Statement_sequence(ASTNode):
    def __init__(self, statement_sequence):
        super().__init__()
        self.type = "statement_sequence"
        self.statement_sequence = statement_sequence

    def __str__(self):
        result = ""
        for st in self.statement_sequence:
            result += str(st) + "\n"
        return result

    def get_children(self):
        return self.statement_sequence


class Assignment(Statement):
    def __init__(self, name, right):
        super().__init__()
        self.type = "assignment"
        self.name = name
        self.right = right

    def __str__(self):
        return "(ASSIGN %s " % self.name + str(self.right) + ")"

    def get_children(self):
        return [self.name, self.right]


class Return(Statement):
    def __init__(self, value):
        super().__init__()
        self.type = "return_statement"
        self.value = value

    def __str__(self):
        return "(RETURN %s)" % self.value

    def get_children(self):
        return [self.value]


class Funcall(Statement):
    def __init__(self, name, args=[]):
        """

        :param name:
        :param args:
        """
        super().__init__()
        self.type = "funcall"
        self.name = name
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
    def __init__(self, expression):
        super().__init__()
        self.type = 'print'
        self.expression = expression

    def __str__(self):
        return "(print %s)" % str(self.expression)

    def get_children(self):
        return [self.expression]


class If(Statement):
    def __init__(self, clause, suite, if_closure=None):
        super().__init__()
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
    def __init__(self, clause, suite, if_closure=None):
        super().__init__()
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
    def __init__(self, suite):
        super().__init__()
        self.type = "else"
        self.suite = suite

    def __str__(self):
        return "(ELSE %s)" % str(self.suite)

    def get_children(self):
        return [self.suite]


class While(Statement):
    def __init__(self, clause, suite):
        super().__init__()
        self.type = "while"
        self.clause = clause
        self.suite = suite

    def __str__(self):
        return "(WHILE %s \n %s)" % (str(self.clause), str(self.suite))

    def get_children(self):
        return [self.clause, self.suite]


class Fundef(Statement):
    def __init__(self, name, suite, parameters=[]):
        """

        :param name:
        :param suite:
        :param parameters:
        """
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.suite = suite

    def __str__(self):
        parameters = "("
        for p in self.parameters:
            parameters += str(p) + ' '
        parameters += ")"
        return "(DEFUN %s %s \n %s)" % (str(self.name), parameters, str(self.suite))

    def get_children(self):
        return [self.name, self.parameters, self.suite]


class Clause(ASTNode):
    def __init__(self, left, op, right):
        super().__init__()
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
    def __init__(self, left, op, right):
        super().__init__()
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
    def __init__(self, value):
        super().__init__()
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT %d)" % self.value

    def get_children(self):
        return list()


class Vfloat(Atom):
    def __init__(self, value):
        super().__init__()
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

    def __init__(self, name, value=None):
        super().__init__()
        self.type = "ID"
        self.name = name
        self.value = value

    def __str__(self):
        if self.value is None:
            return self.name
        else:
            return "(%s " % self.name + str(self.value) + ")"

    def get_children(self):
        return list()


class Vstring(Atom):
    def __init__(self, data):
        super().__init__()
        self.type = "string"
        self.data = data

    def __str__(self):
        return self.data

    def get_children(self):
        return list()


class Vboolean(Atom):
    def __init__(self, value):
        super().__init__()
        self.type = "boolean"
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return list()


class Map(Statement):
    def __init__(self, funcname, vlist):
        super().__init__()
        self.funcname = funcname
        self.vlist = vlist

    def __str__(self):
        return "(%s %s" % (self.funcname, str(self.vlist))

    def get_children(self):
        return [self.funcname, self.vlist]


class Pair(Atom):
    def __init__(self, head, tail):
        super().__init__()
        self.head = head
        self.tail = tail

    def __str__(self):
        pass

    def get_children(self):
        return [self.head, self.tail]


if __name__ == "__main__":
    node = Vinteger(10)
