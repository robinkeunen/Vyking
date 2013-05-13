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
        """
        Initialization function
        :param lineno: line number
        :param lexpos: position
        """
        self.type = None
        self.lineno = lineno
        self.lexpos = lexpos
        self.id = counter.__next__()

    def get_type(self):
        """
        returns the type of the node
        :return: the type of the node
        """
        return self.type

    def get_children(self):
        """Returns a list of the node's children
        """
        raise NotImplementedError("Should have implemented this")


class Statement_sequence(ASTNode):
    def __init__(self, statement_sequence, lineno, lexpos):
        """
        Initialization function
        :param statement_sequence: Instructions list
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "statement_sequence"
        self.statement_sequence = statement_sequence

    def __str__(self):
        """
        Returns a string representation of the class
        :return: a string representation of the class
        """
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
        """
        Initialization function
        :param left: the left member of the assignment
        :param right: the right member of the assignmenet
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        Initialization function
        :param value: Value of the return
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "return_statement"
        self.value = value

    def __str__(self):
        return "(RETURN %s)" % self.value

    def get_children(self):
        return [self.value]


class Funcall(Statement):
    def __init__(self, name, lineno, lexpos, args=None):
        """
        Initialization function
        :param name: name of the function
        :param lineno: line number
        :param lexpos: position
        :param args: arguments
        """
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
        """
        Initialization function
        :param clause: the clause of the print
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = 'print'
        self.clause = clause

    def __str__(self):
        return "(print %s)" % str(self.clause)

    def get_children(self):
        return [self.clause]


class If(Statement):
    def __init__(self, clause, suite, lineno, lexpos, if_closure=None):
        """
        Initialization function
        :param clause: The clause
        :param suite: The suite block
        :param lineno: Line Number
        :param lexpos: Position
        :param if_closure: The Closure
        """
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
        """
        Init function
        :param clause: The Clause
        :param suite: The Suite Block
        :param lineno: Line Number
        :param lexpos: Position
        :param if_closure: The Closure Block
        """
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
        """
        Init function
        :param suite: The Suite Block
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "else"
        self.suite = suite

    def __str__(self):
        return "(ELSE %s)" % str(self.suite)

    def get_children(self):
        return [self.suite]


class While(Statement):
    def __init__(self, clause, suite, lineno, lexpos):
        """
        Init
        :param clause: The clause
        :param suite: The suite block
        :param lineno: line number
        :param lexpos: position
        """
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
        Init
        :param prototype: Prototype of the fundef
        :param suite: The suite block
        :param lineno: line number
        :param lexpos: position
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
        """
        Init for a function prototype
        :param return_ty: return type
        :param name: name of the function
        :param ty_params: parametres types
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        Init
        :param left: Left term of the clause
        :param op: Clause operator
        :param right: Right term of the clause
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        Init
        :param left: left term of the expression
        :param op: expression operator
        :param right: right term of the expression
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        Init
        :param value: value of the integer
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "INT"
        self.value = value

    def __str__(self):
        return "(INT %d)" % self.value

    def get_children(self):
        return list()


class Vfloat(Atom):
    def __init__(self, value, lineno, lexpos):
        """
        Init
        :param value: value of the float
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        Init
        :param name: id name
        :param lineno: line number
        :param lexpos: position
        """
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
        """
        init
        :param data: content of the string
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "string"
        self.value = data

    def __str__(self):
        return self.value

    def get_children(self):
        return list()


class Vboolean(Atom):
    def __init__(self, value, lineno, lexpos):
        """
        Init
        :param value: boolean value
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.type = "boolean"
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_children(self):
        return list()


class Map(Statement):
    def __init__(self, funcname, vlist, lineno, lexpos):
        """
        Init
        :param funcname: name of the function
        :param vlist: list on which the function will be applied
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.funcname = funcname
        self.vlist = vlist

    def __str__(self):
        return "(%s %s" % (self.funcname, str(self.vlist))

    def get_children(self):
        return [self.funcname, self.vlist]


class Pair(Atom):
    def __init__(self, head, tail, lineno, lexpos):
        """
        Init
        :param head: head of the pair
        :param tail: tail of the pair
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.head = head
        self.tail = tail

    def __str__(self):
        return "[%s, %s]" % ( self.head, self.tail)

    def get_children(self):
        return [self.head, self.tail]

class Head(Atom):
    def __init__(self, pair, lineno, lexpos):
        """
        Init
        :param pair: pair of which this is the head
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.pair = pair

    def __str__(self):
        return "[Head : %s]" % (self.pair)

    def get_children(self):
        return [self.pair]

class Tail(Atom):
    def __init__(self, pair, lineno, lexpos):
        """
        Init
        :param pair: pair of which this is the tail
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.pair = pair

    def __str__(self):
        return "[Tail : %s]" % (self.pair)

    def get_children(self):
        return [self.pair]

class Append(Atom):
    def __init__(self, pair1, pair2, lineno, lexpos):
        """
        Init
        :param pair1: 1st pair
        :param pair2: 2nd pair
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.pair1 = pair1
        self.pair2 = pair2

    def __str__(self):
        return "[Append : %s %s]" % (self.pair1, self.pair2)

    def get_children(self):
        return [self.pair1, self.pair2]

class Cons(Atom):
    def __init__(self, data, pair, lineno, lexpos):
        """
        Init
        :param data: clause
        :param pair: pair
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.data = data
        self.pair = pair

    def __str__(self):
        return "[Cons : %s %s]" % (self.data, self.pair)

    def get_children(self):
        return [self.data, self.pair]

class Map(Atom):
    def __init__(self, id, pair, lineno, lexpos):
        """
        Init
        :param id: id
        :param pair: pair
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.id = id
        self.pair = pair

    def __str__(self):
        return "[Map : %s %s]" % (self.id, self.pair)

    def get_children(self):
        return [self.id, self.pair]

class Apply(Atom):
    def __init__(self, id, pair, lineno, lexpos):
        """
        Init
        :param id: id
        :param pair: pair
        :param lineno: line number
        :param lexpos: position
        """
        super().__init__(lineno, lexpos)
        self.id = id
        self.pair = pair

    def __str__(self):
        return "[Apply : %s %s]" % (self.id, self.pair)

    def get_children(self):
        return [self.id, self.pair]