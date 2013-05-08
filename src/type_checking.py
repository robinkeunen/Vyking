__author__ = 'Robin Keunen', 'Pierre Vyncke'

from src.misc import add_to_class
import src.ast as ast


@add_to_class(ast.Statement_sequence)
def type_check(self):
    pass


@add_to_class(ast.Declaration)
def generate_class(self):
    pass


@add_to_class(ast.Assignment)
def type_check(self):
    pass


@add_to_class(ast.Return)
def type_check(self):
    pass


@add_to_class(ast.Funcall)
def type_check(self):
    pass


@add_to_class(ast.Print)
def type_check(self):
    pass


@add_to_class(ast.If)
def type_check(self):
    pass


@add_to_class(ast.Elif)
def type_check(self):
    pass


@add_to_class(ast.Else)
def type_check(self):
    pass


@add_to_class(ast.While)
def type_check(self):
    pass


@add_to_class(ast.Fundef)
def type_check(self):
    pass


@add_to_class(ast.Prototype)
def type_check(self):
    pass


@add_to_class(ast.Clause)
def type_check(self):
    pass


@add_to_class(ast.Expression)
def type_check(self):
    pass


@add_to_class(ast.ID)
def type_check(self):
    pass


@add_to_class(ast.Vinteger)
def type_check(self):
    pass


@add_to_class(ast.Vfloat)
def type_check(self):
    pass


@add_to_class(ast.Vboolean)
def type_check(self):
    pass


@add_to_class(ast.Vstring)
def type_check(self):
    pass


@add_to_class(ast.Map)
def type_check(self):
    pass


@add_to_class(ast.Pair)
def type_check(self):
    pass