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


class Statement_sequence():
    def __init__(self, statement, statement_sequence=None):
        self.type = "statement_sequence"
        if statement_sequence is None:
            self.stat_list = [statement]
        else:
            self.stat_list = [statement] + statement_sequence.stat_list

    def __str__(self):
        result = ""
        for st in self.stat_list:
            result += str(st) + "\n\t"
        return result


class Assignment(Statement):
    def __init__(self, name, right):
        self.type = "assignment"
        self.name = name
        self.right = right

    def __str__(self):
        return "(ASSIGN %s " % self.name + str(self.right) + ")"


class Return(Statement):
    def __init__(self, value):
        self.type = "return_statement"
        self.value = value

    def __str__(self):
        return "(RETURN %s)" % self.value


class If(Statement):
    def __init__(self, test, else_):
        self.type = "if_statement"
        self.test = test
        self.else_ = else_

    def __str__(self):
        return "(IF %s \n %s" % (str(self.test), str(self.else_))


class Expression(ASTNode):
    pass


class Expression(Expression):
    def __init__(self, left, op, right):
        self.type = "Expression"
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "(%s %s %s)" % (self.op, self.left, self.right)


class Test(ASTNode):
    pass


class BinopTest(Test):
    def __init__(self, left, op, right):
        self.type = 'test'
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.op, self.left, self.right)


class Atom(ASTNode):
    pass


class Vinteger(Atom):
    def __init__(self, value):
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT %d)" % self.value


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
        return "(%s " % self.name + str(self.value) + ")"
