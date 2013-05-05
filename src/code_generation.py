__author__ = 'Robin Keunen', 'Robin Keunen'

from src.misc import add_to_class
import src.ast as ast
import llvm.core as lc
#import llvm.ee as le
#import llvm.passes as lp

# The LLVM module, which holds all the IR code.
g_llvm_module = lc.Module.new('jit')
# FIXME make this non-local
#ast.ASTNode.llvm_module = lc.Module.new('jit')

# The LLVM instruction builder. Created whenever a new function is entered.
g_llvm_builder = None
# FIXME make this non-local
# ast.ASTNode.llvm_builder = None

# A dictionary that keeps track of which values are defined in the current scope
# and what their LLVM representation is.
# TODO fix to get closures (using Scopes?)
# FIXME make this non-local
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


def CreateEntryBlockAlloca(function, var_name):
    """
    Creates an alloca instruction in the entry block of the function.
    This is used for mutable variables.
    """
    entry = function.get_entry_basic_block()
    builder = lc.Builder.new(entry)
    builder.position_at_beginning(entry)
    return builder.alloca(lc.Type.double(), var_name)


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
    # Look up the name in the global module table.
    f = g_llvm_module.get_function_named(self.name)

    # Check for argument mismatch error.
    if len(f.args) != len(self.args):
        raise RuntimeError('Incorrect number of arguments passed.')

    arg_values = [i.CodeGen() for i in self.args]

    return g_llvm_builder.call(f, arg_values, 'calltmp')


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
    'OR':  lambda l, r: g_llvm_builder.or_(l, r, 'or_tmp'),
    'AND': lambda l, r: g_llvm_builder.and_(l, r, 'and_tmp'),
    'EQ':  lambda l, r: g_llvm_builder.icmp(lc.icmp_EQ, l, r, 'eq_tmp'),
    'NEQ': lambda l, r: g_llvm_builder.icmp(lc.icmp_NEQ, l, r, 'neq_tmp'),
    'LT':  lambda l, r: g_llvm_builder.icmp(lc.icmp_SLT, l, r, 'lt_tmp'),
    'GT':  lambda l, r: g_llvm_builder.icmp(lc.icmp_SGT, l, r, 'gt_tmp'),
    'LEQ': lambda l, r: g_llvm_builder.icmp(lc.icmp_SLE, l, r, 'leq_tmp'),
    'GEQ': lambda l, r: g_llvm_builder.icmp(lc.icmp_SGE, l, r, 'geq_tmp'),
    'PLUS':   lambda l, r: g_llvm_builder.add(l, r, 'add_temp'),
    'MINUS':  lambda l, r: g_llvm_builder.sub(l, r, 'sub_temp'),
    'TIMES':  lambda l, r: g_llvm_builder.mul(l, r, 'mul_temp'),
    'DIVIDE': lambda l, r: g_llvm_builder.sdiv(l, r, 'div_temp'),
    'MOD':    lambda l, r: print("Modulo not implemented")
}


@add_to_class(ast.Clause)
def generate_code(self):
    # TODO type check
    # TODO NOT operand
    # TODO grouped clauses or useless? note: p[0] = p[2]

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