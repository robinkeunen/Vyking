# -----------------------------------------------------------------------------
# ast.py
# Nodes of the abstract syntax tree for the Vyking language.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------


__author__ = 'Robin Keunen'


class ASTNode(object):
    """
    Abstract class for nodes of the syntax tree.
    Children must implement accept(ASTNodeVisitor)
    (Visitor design pattern)
    """

    # accept visitor (not implemented yet)
    def accept(self):
        raise NotImplementedError("Should have implemented this")

    def get_type(self):
        raise NotImplementedError("Should have implemented this")

    def get_children(self):
        raise NotImplementedError("Should have implemented this")


class Statement(ASTNode):
    pass


class Statement_sequence():
    def __init__(self, statement_sequence):
        self.type = "statement_sequence"
        self.statement_sequence = statement_sequence

    def __str__(self):
        result = ""
        for st in self.statement_sequence:
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
    def __init__(self, name, args=[]):
        """

        :param name:
        :param args:
        """
        self.type = "funcall"
        self.name = name
        self.args = args

    def __str__(self):
        args_repr = "["
        for arg in self.args:
            args_repr += str(arg)
        args_repr += "]"
        return "(f:%s %s)" % (self.name, args_repr)


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
    def __init__(self, name, suite, parameters=[]):
        """

        :param name:
        :param suite:
        :param parameters:
        """
        self.name = name
        self.parameters = parameters
        self.suite = suite

    def __str__(self):
        parameters = "["
        for p in self.parameters:
            parameters += str(p) + ' '
        parameters += "]"
        return "(DEFUN %s %s \n %s)" % (str(self.name), parameters, str(self.suite))


class Expression(ASTNode):
    def __init__(self, left, op, right):
        self.type = "Expression"
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        if self.left is None:
            return "(%s %s)" % (self.op, self.right)
        else:
            return "(%s %s %s)" % (self.op, str(self.left), str(self.right))


class Clause(ASTNode):
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


class Vboolean(Atom):
    def __init__(self, value):
        self.type = "boolean"
        self.value = value

    def __str__(self):
        return str(self.value)

class Map(Statement):
    def __init__(self, funcname, vlist):
        self.funcname = funcname
        self.vlist

    def __str__(self):
        return "(%s %s" %(self.funcname, str(self.vlist))

class Pair(Atom):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        pass