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


class INT(Atom):
    def __init__(self, value):
        self.type = "INT"
        self.value = value