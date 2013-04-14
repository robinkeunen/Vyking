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
            result += str(st) + "\n"
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


class Funcall(Statement):
    def __init__(self, id, args=[]):
        self.type = "funcall"
        self.id = id
        self.args = args
    def __str__(self):
        args_repr = "["
        for arg in self.args:
            args_repr += str(arg)
        args_repr += "]"
        return "(f:%s %s)" % (self.id, args_repr)


class If(Statement):
    def __init__(self, clause, suite, if_closure=None):
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


class Elif(Statement):
    def __init__(self, clause, suite, if_closure=None):
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


class Else(Statement):
    def __init__(self, suite):
        self.type = "else"
        self.suite = suite

    def __str__(self):
        return "(ELSE %s)" % str(self.suite)


class While(Statement):
    def __init__(self, clause, suite):
        self.type = "while"
        self.clause = clause
        self.suite = suite

    def __str__(self):
        return "(WHILE %s \n %s)" % (str(self.clause), str(self.suite))


class Fundef(Statement):
    def __init__(self, id, suite, parameters=[]):
        self.id = id
        self.parameters = parameters
        self.suite = suite

    def __str__(self):
        parameters ="["
        for p in self.parameters:
            parameters += str(p) + ' '
        parameters += "]"
        return "(DEFUN %s %s \n %s)" % (str(self.id), parameters, str(self.suite))


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


class Clause(Test):
    def __init__(self, left, op, right):
        self.type = 'clause'
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        if self.left is None:
            return "(%s %s)" % (self.op, self.right)
        else:
            return "(%s %s %s)" % (self.op, self.left, self.right)


class Atom(ASTNode):
    pass


class Vinteger(Atom):
    def __init__(self, value):
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT %d)" % self.value


class Vfloat(Atom):
    def __init__(self, value):
        self.type = "FLOAT"
        self.value = value

    def __str__(self):
        return "(FLOAT %d)" % self.value


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
        if self.value is None:
            return self.name
        else:
            return "(%s " % self.name + str(self.value) + ")"

class Vstring(Atom):
    def __init__(self, data):
        self.type = "string"
        self.data = data

    def __str__(self):
        return self.data
