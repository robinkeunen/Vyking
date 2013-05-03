__author__ = 'Robin Keunen', 'Robin Keunen'

from src.misc import add_to_class
import src.ast as ast
import llvm
import llvm.core as lc
#import llvm.ee as le
#import llvm.passes as lp

# The LLVM module, which holds all the IR code.
g_llvm_module = lc.Module.new('jit')

# The LLVM instruction builder. Created whenever a new function is entered.
g_llvm_builder = None
# FIXME might need  a fix
g_llvm_builder = lc.Builder.new(lc.BasicBlock)

# A dictionary that keeps track of which values are defined in the current scope
# and what their LLVM representation is.
g_named_values = {}


class Scope(object):
    """
    Keeps track of the variable in the scope
    """

    def __init__(self, environment=None):
        self.local = {}
        self.environment = environment

    def add(self):
        pass

    def get(self, name):
        if name in self.local:
            return self.local[name]
        elif name in self.environment:
            return self.environment[name]
        else:
            raise NameError("NameError : name '%s' is not defined" % name)


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

int_binops = {
    'OR':     lambda l, r: g_llvm_builder.or_(l, r, 'ortmp'),
    'AND':    lambda l, r: g_llvm_builder.and_(l, r, 'andtmp'),
    'EQ':     lambda l, r: g_llvm_builder.icmp(lc.icmp_EQ, l, r, 'cmptmp'),
    'NEQ':    lambda l, r: g_llvm_builder.icmp(lc.icmp_NEQ, l, r, 'cmptmp'),
    'LT':     lambda l, r: g_llvm_builder.icmp(lc.icmp_SLT, l, r, 'cmptmp'),
    'GT':     lambda l, r: g_llvm_builder.icmp(lc.icmp_SGT, l, r, 'cmptmp'),
    'LEQ':    lambda l, r: g_llvm_builder.icmp(lc.icmp_SLE, l, r, 'cmptmp'),
    'GEQ':    lambda l, r: g_llvm_builder.icmp(lc.icmp_SGE, l, r, 'cmptmp'),
    'PLUS':   lambda l, r: g_llvm_builder.add(l, r, 'addtemp'),
    'MINUS':  lambda l, r: g_llvm_builder.sub(l, r, 'suntemp'),
    'TIMES':  lambda l, r: g_llvm_builder.mul(l, r, 'multemp'),
    'DIVIDE': lambda l, r: g_llvm_builder.sdiv(l, r, 'divtemp'),
    'MOD':    lambda l, r: print("Modulo not implemented")
}

@add_to_class(ast.Clause)
def generate_code(self):
    # TODO type check
    # TODO NOT operand
    # TODO grouped clauses or useless? p[0] = p[2]

    left = self.left.generate_code()
    right = self.right.generate_code()

    return int_binops[self.op](left, right)

@add_to_class(ast.Expression)
def generate_code(self):
    # TODO type check
    # TODO Uminus -> deal in ast

    left = self.left.generate_code()
    right = self.right.generate_code()

    return int_binops[self.op](left, right)


@add_to_class(ast.ID)
def generate_code(self):
    # TODO scope lookup
    if self.name in g_named_values:
        return g_named_values[self.name]
    else:
        raise NameError("NameError : name '%s' is not defined" % self.name)


@add_to_class(ast.Vinteger)
def generate_code(self):
    return lc.Constant.int(lc.Type.int(), self.value)


@add_to_class(ast.Vfloat)
def generate_code(self):
    return lc.Constant.real(lc.Type.float(), self.value)


@add_to_class(ast.Vboolean)
def generate_code(self):
    if self.value:
        v = 1
    else:
        v = 0
    return lc.Constant.int(lc.Type.int(1), v)


@add_to_class(ast.Vstring)
def generate_code(self):
    return lc.Constant.string(self.data)


@add_to_class(ast.Map)
def generate_code(self):
    pass


@add_to_class(ast.Pair)
def generate_code(self):
    pass