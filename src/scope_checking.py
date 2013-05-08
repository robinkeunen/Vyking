__author__ = 'Robin Keunen', 'Pierre Vyncke'

from src.misc import add_to_class
import src.ast as ast


class Environment(object):
    """
    Keeps track of the variables and functions in the scope
    """

    def __init__(self, surrounding=None):
        self.local = {}
        self.surrounding = surrounding

    def add(self, name, data):
        self.local[name] = data

    def get(self, name):
        if name in self.local:
            return self.local[name]
        elif self.surrounding is not None and name in self.surrounding:
            return self.surrounding[name]
        else:
            raise NameError("NameError : name '%s' is not defined" % name)

    def copy(self):
        obj_copy = Environment()
        obj_copy.local = self.local.copy()
        obj_copy.surrounding = self.surrounding.copy()

@add_to_class(ast.Statement_sequence)
def generate_code(self):
    pass


@add_to_class(ast.Assignment)
def generate_code(self):
    pass


@add_to_class(ast.Return)
def generate_code(self):
    pass


@add_to_class(ast.Funcall)
def generate_code(self):
    pass


@add_to_class(ast.Print)
def generate_code(self):
    pass


@add_to_class(ast.If)
def generate_code(self):
    pass


@add_to_class(ast.Elif)
def generate_code(self):
    pass


@add_to_class(ast.Else)
def generate_code(self):
    pass


@add_to_class(ast.While)
def generate_code(self):
    pass


@add_to_class(ast.Fundef)
def generate_code(self):
    pass


@add_to_class(ast.Clause)
def generate_code(self):
    pass


@add_to_class(ast.Expression)
def generate_code(self):
    pass


@add_to_class(ast.ID)
def generate_code(self):
    pass


@add_to_class(ast.Vinteger)
def generate_code(self):
    pass


@add_to_class(ast.Vfloat)
def generate_code(self):
    pass


@add_to_class(ast.Vboolean)
def generate_code(self):
    pass


@add_to_class(ast.Vstring)
def generate_code(self):
    pass


@add_to_class(ast.Map)
def generate_code(self):
    pass


@add_to_class(ast.Pair)
def generate_code(self):
    pass