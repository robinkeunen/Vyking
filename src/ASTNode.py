__author__ = 'Robin Keunen'


class ASTNode(object):
    """
    Abstract class for nodes. Childs must implement
     accept(ASTNodeVisitor)
    """

    def accept(self):
        raise NotImplementedError("Should have implemented this")

    def get_type(self):
        raise NotImplementedError("Should have implemented this")

    def get_children(self):
        raise NotImplementedError("Should have implemented this")


class Statement(ASTNode):
    pass


class Assignment(Statement):
    def __init__(self, variable, right):
        self.type = "assignment"
        self.variable = variable
        self.right = right


class Expression(ASTNode):
    pass


class BinopExpression(Expression):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op


class Atom(ASTNode):
    pass


class Vinteger(Atom):
    def __init__(self, value):
        self.type = "INT"
        self.value = value


class ID(Atom):
    def __init__(self, name, value):
        self.type = "ID"
        self.name = name
        self.value = value