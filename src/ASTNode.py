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
    def __init__(self, name, right):
        self.type = "assignment"
        self.name = name
        self.right = right

    def __str__(self):
        return "(ASSIGN, %s, " % self.name + str(self.right) + ")"


class Expression(ASTNode):
    pass


class BinopExpression(Expression):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "(" + self.op + ', ' + str(self.left) + ', ' + str(self.right) + ')'


class Atom(ASTNode):
    pass


class Vinteger(Atom):
    def __init__(self, value):
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT, %d)" % self.value


class ID(Atom):
    """
    Represents an ID in the AST, if value is not set,
    semantic analysis must check it has been assigned
    """
    def __init__(self, name, value=None):
        self.type = "ID"
        self.name = name
        self.value = value

    def __str__(self):
        return "(%s, " % self.name +  str(self.value) + ")"