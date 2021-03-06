# -----------------------------------------------------------------------------
# code_generation.py
# Generates the LLVM code
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------
from llvm.ee import ExecutionEngine
from llvm.passes import FunctionPassManager

from src.type_checking import Environment

from src.misc import add_to_class, trace
import src.ast as ast
import llvm.core as lc
#import llvm.ee as le
import llvm.passes as lp

# The LLVM module, which holds all the IR code.
g_llvm_module = lc.Module.new('jit')

# The LLVM instruction builder. Created whenever a new function is entered.
g_llvm_builder = None

# g_llvm_pass_manager = FunctionPassManager.new(g_llvm_module)
# g_llvm_executor = ExecutionEngine.new(g_llvm_module)
# g_llvm_pass_manager.add(g_llvm_executor.target_data)
#
# # Set up the optimizer pipeline. Start with registering info about how the
# # target lays out data structures.
#
# # Promote allocas to registers.
# g_llvm_pass_manager.add(lp.PASS_PROMOTE_MEMORY_TO_REGISTER)
# # Do simple "peephole" optimizations and bit-twiddling optzns.
# g_llvm_pass_manager.add(lp.PASS_INSTRUCTION_COMBINING)
# # Reassociate expressions.
# g_llvm_pass_manager.add(lp.PASS_REASSOCIATE)
# # Eliminate Common SubExpressions.
# g_llvm_pass_manager.add(lp.PASS_GVN)
# # Simplify the control flow graph (deleting unreachable blocks, etc).
# g_llvm_pass_manager.add(lp.PASS_CFG_SIMPLIFICATION)
#
# g_llvm_pass_manager.initialize()

# named value
# A dictionary that keeps track of which values are defined in the current scope
# and what their LLVM representation is.

TY_INT = "TY_INT"
TY_FLOAT = "TY_FLOAT"
TY_BOOL = "TY_BOOL"
TY_STRING = "TY_STRING"
TY_FUNC = "TY_FUNC"
TY_VOID = "TY_VOID"
TY_RT = "TY_RT"

llvm_type = {
    TY_BOOL: lc.Type.int(1),
    TY_INT: lc.Type.int(),
    TY_FLOAT: lc.Type.float(),
    TY_STRING: None,  # TODO string type as arg http://bit.ly/10PRVKW
    TY_FUNC: None,  # TODO func type as arg
}

# helper function
def CreateEntryBlockAlloca(function, type_tuple, var_name):
    """
    Creates an alloca instruction in the entry block of the function.
    This is used for mutable variables.
    :param function: TODO
    :param type_tuple:
    :param var_name:
    """
    entry = function.entry_basic_block
    builder = lc.Builder.new(entry)
    builder.position_at_beginning(entry)
    # unpack
    ty, *t = type_tuple
    if ty in (TY_FUNC, TY_VOID, TY_RT):
        raise TypeError("think more")  # FIXME block alloca
    return builder.alloca(llvm_type[ty], var_name)


@add_to_class(ast.ASTNode)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    raise NotImplementedError


@add_to_class(ast.Statement_sequence)
def generate_code(self, named_values=None):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    # create anonymous function to link statements
    # FIXME global module
    # FIXME only

    if named_values is None:
        named_values = Environment()

    # make anonymous function on entry point
    global g_llvm_builder
    if g_llvm_builder is None:
        ty = lc.Type.void()
        func_type = lc.Type.function(ty, [])
        function = lc.Function.new(g_llvm_module, func_type, "")
        # Create a new basic block to start insertion into.
        block = function.append_basic_block('top-level')
        g_llvm_builder = lc.Builder.new(block)
    # else:
    #     function = g_llvm_builder.basic_block.function
    #     block = function.append_basic_block('stmt_seq')
    #     g_llvm_builder = lc.Builder.new(block)

    for statement in self.statement_sequence:
        stmt = statement.generate_code(named_values)


@add_to_class(ast.Assignment)
def create_local_variable(self, named_values):
    """
    Creates a local variable into scope
    :param named_values: The environment
    """
    function = g_llvm_builder.basic_block.function

    # Register all variables and emit their initializer.
    var_name = self.left.get_name()
    var_value = self.right.generate_code(named_values)

    ty = self.environment[var_name]
    alloca = CreateEntryBlockAlloca(function, tuple(ty), var_name)
    g_llvm_builder.store(var_value, alloca)

    named_values[var_name] = alloca

    return alloca


@add_to_class(ast.Assignment)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    name = self.left.get_name()
    if name in named_values:
        variable = named_values[name]
        value = self.right.generate_code(named_values)
        g_llvm_builder.store(value, variable)
    else:
        self.create_local_variable(named_values)


@add_to_class(ast.Return)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    value = self.value.generate_code(named_values)
    return value


@add_to_class(ast.Funcall)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    # Look up the name in the global module table.
    f = g_llvm_module.get_function_named(self.name.get_name())
    f_environment = named_values[self.name.get_name()]
    # FIXME get closures
    # Check for argument mismatch error.
    if len(f.args) != len(self.args):
        raise RuntimeError('Incorrect number of arguments passed.')

    arg_values = [i.generate_code(named_values) for i in self.args]

    return g_llvm_builder.call(f, arg_values, 'calltmp')


@add_to_class(ast.Print)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    pass


@add_to_class(ast.If)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """

    clause = self.clause.generate_code(named_values)

    # convert to 1-bit bool
    # FIXME type
    condition_bool = g_llvm_builder.icmp(
        lc.ICMP_NE, clause, lc.Constant.int(lc.Type.int(1), 0), 'ifcond')

    function = g_llvm_builder.basic_block.function

    # Create blocks for the then and else cases. Insert the 'then' block at the
    # end of the function.
    suite_block = function.append_basic_block('suite')
    closure_block = function.append_basic_block('closure')
    merge_block = function.append_basic_block('ifcond')

    if self.if_closure is None:
        g_llvm_builder.cbranch(condition_bool, suite_block, merge_block)
    else:
        g_llvm_builder.cbranch(condition_bool, suite_block, closure_block)

    # Build suite block
    g_llvm_builder.position_at_end(suite_block)
    suite_value = self.suite.generate_code(named_values)
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    suite_block = g_llvm_builder.basic_block

    # Build closure block
    g_llvm_builder.position_at_end(closure_block)
    if self.if_closure is not None:
        closure_value = self.if_closure.generate_code(named_values)
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    closure_block = g_llvm_builder.basic_block

    # Build merge block.
    g_llvm_builder.position_at_end(merge_block)
    phi = g_llvm_builder.phi(lc.Type.int(), 'iftmp')
    phi.add_incoming(suite_block, suite_block)
    if self.if_closure is not None:
        phi.add_incoming(closure_value, closure_block)

    return phi


@add_to_class(ast.Elif)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    clause = self.clause.generate_code(named_values)

    # convert to 1-bit bool
    # FIXME type
    condition_bool = g_llvm_builder.icmp(
        lc.ICMP_NE, clause, lc.Constant.int(lc.Type.int(1), 0), 'ifcond')

    function = g_llvm_builder.basic_block.function

    # Create blocks for the then and else cases. Insert the 'then' block at the
    # end of the function.
    suite_block = function.append_basic_block('suite')
    closure_block = function.append_basic_block('closure')
    merge_block = function.append_basic_block('ifcond')

    if self.if_closure is None:
        g_llvm_builder.cbranch(condition_bool, suite_block, merge_block)
    else:
        g_llvm_builder.cbranch(condition_bool, suite_block, closure_block)

    # Build suite block
    g_llvm_builder.position_at_end(suite_block)
    suite_value = self.suite.generate_code(named_values)
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    suite_block = g_llvm_builder.basic_block

    # Build closure block
    g_llvm_builder.position_at_end(closure_block)
    if self.if_closure is not None:
        closure_value = self.if_closure.generate_code
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    closure_block = g_llvm_builder.basic_block

    # Build merge block.
    g_llvm_builder.position_at_end(merge_block)
    phi = g_llvm_builder.phi(lc.Type.int(), 'iftmp')
    phi.add_incoming(suite_block, suite_block)
    if self.if_closure is not None:
        phi.add_incoming(closure_value, closure_block)

    return phi


@add_to_class(ast.Else)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    return self.suite.generate_code(named_values)


@add_to_class(ast.While)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    pass


# helper function
@add_to_class(ast.Prototype)
def CreateArgumentAllocas(self, function, named_values):
    """
    Create an alloca for each argument and register the argument in the symbol
    table so that references to it will succeed.
    """
    if self.ty_params[0] is None:
        return named_values
    nested_scope = Environment(named_values, defun_block=True)
    for type_name, arg in zip(self.ty_params, function.args):
        ty, name = type_name
        ty = ty,
        alloca = CreateEntryBlockAlloca(function, ty, name.get_name())
        g_llvm_builder.store(arg, alloca)
        nested_scope[name.get_name()] = alloca

    return nested_scope


@add_to_class(ast.Prototype)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    # Create an alloca for each argument and register the argument in the symbol
    # table so that references to it will succeed.

    func_type = lc.Type.function(lc.Type.int(),
                                (lc.Type.int(),) * len(self.ty_params),
                                False)

    # create function signature
    # FIXME other function types

    function = lc.Function.new(g_llvm_module,
                               func_type,
                               self.name.get_name())

    # TODO closures
    # add parameters to function block
    if self.ty_params[0] is not None:
        for param, p_name in zip(function.args, self.ty_params):
            param.name = p_name[1].get_name()

    return function


@add_to_class(ast.Fundef)
def generate_code(self, named_values):
    """
Generates the LLVM code
    :param named_values: The environment
    """
    # clear scope
    # FIXME closures, might have to play here

    function = self.prototype.generate_code(named_values)

    # Create a new basic block to start insertion into.
    block = function.append_basic_block('entry')
    # FIXME make non global
    global g_llvm_builder
    g_llvm_builder = lc.Builder.new(block)

    # Add all arguments to the symbol table and create their allocas.
    nested_scope = self.prototype.CreateArgumentAllocas(function, named_values)

    # Finish off the function.
    try:

        return_value = self.suite.generate_code(nested_scope)
        g_llvm_builder.ret(return_value)

        # Validate the generated code, checking for consistency.
        function.verify()

        # Optimize the function.
        # TODO optimizer support
        # g_llvm_pass_manager.run(function)
    except:
        function.delete()
        raise

    return function


int_binops = {
    'OR': lambda l, r: g_llvm_builder.or_(l, r, 'or_tmp'),
    'AND': lambda l, r: g_llvm_builder.and_(l, r, 'and_tmp'),
    'EQ': lambda l, r: g_llvm_builder.icmp(lc.ICMP_EQ, l, r, 'eq_tmp'),
    'NEQ': lambda l, r: g_llvm_builder.icmp(lc.ICMP_NEQ, l, r, 'neq_tmp'),
    'LT': lambda l, r: g_llvm_builder.icmp(lc.ICMP_SLT, l, r, 'lt_tmp'),
    'GT': lambda l, r: g_llvm_builder.icmp(lc.ICMP_SGT, l, r, 'gt_tmp'),
    'LEQ': lambda l, r: g_llvm_builder.icmp(lc.ICMP_SLE, l, r, 'leq_tmp'),
    'GEQ': lambda l, r: g_llvm_builder.icmp(lc.ICMP_SGE, l, r, 'geq_tmp'),
    'PLUS': lambda l, r: g_llvm_builder.add(l, r, 'add_temp'),
    'MINUS': lambda l, r: g_llvm_builder.sub(l, r, 'sub_temp'),
    'TIMES': lambda l, r: g_llvm_builder.mul(l, r, 'mul_temp'),
    'DIVIDE': lambda l, r: g_llvm_builder.sdiv(l, r, 'div_temp'),
    'MOD': lambda l, r: print("Modulo not implemented")
}

float_binops = {
    'OR': lambda l, r: g_llvm_builder.or_(l, r, 'or_tmp'),
    'AND': lambda l, r: g_llvm_builder.and_(l, r, 'and_tmp'),
    'EQ': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_OEQ, l, r, 'eq_tmp'),
    'NEQ': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_ONE, l, r, 'neq_tmp'),
    'LT': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_OLT, l, r, 'lt_tmp'),
    'GT': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_OGT, l, r, 'gt_tmp'),
    'LEQ': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_OLE, l, r, 'leq_tmp'),
    'GEQ': lambda l, r: g_llvm_builder.fcmp(lc.FCMP_OGE, l, r, 'geq_tmp'),
    'PLUS': lambda l, r: g_llvm_builder.fadd(l, r, 'add_temp'),
    'MINUS': lambda l, r: g_llvm_builder.fsub(l, r, 'sub_temp'),
    'TIMES': lambda l, r: g_llvm_builder.fmul(l, r, 'mul_temp'),
    'DIVIDE': lambda l, r: g_llvm_builder.fdiv(l, r, 'div_temp'),
    'MOD': lambda l, r: print("Modulo not implemented")
}


@add_to_class(ast.Clause)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    ty = self.type
    if len(ty) == 2 and ty[0] == 'NOT':
        return g_llvm_builder.not_(self.right.generate_code(named_values), 'not_tmp')

    left = self.left.generate_code(named_values)
    right = self.right.generate_code(named_values)

    tyl, _, tyr = ty
    if tyl == tyr:
        if tyl == TY_INT:
            return int_binops[self.op](left, right)
        elif tyl == TY_FLOAT:
            return float_binops[self.op](left, right)
    else:
        if tyl == TY_INT:
            left = g_llvm_builder.sitofp(left, llvm_type[TY_FLOAT], 'cast_tmp')
        else:
            right = g_llvm_builder.sitofp(right, llvm_type[TY_FLOAT], 'cast_tmp')

    return float_binops[self.op](left, right)


@add_to_class(ast.Expression)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    ty = self.type
    if len(ty) == 2 and ty[0] == 'UMINUS':
        left = g_llvm_builder.Constant.int(llvm_type[ty[1]], 0)
        ty = (ty[1],) + ty
    else:
        left = self.left.generate_code(named_values)
    right = self.right.generate_code(named_values)

    tyl, _, tyr = ty
    if tyl == tyr:
        if tyl == TY_INT:
            return int_binops[self.op](left, right)
        else:
            return float_binops[self.op](left, right)
    else:
        if tyl == TY_INT:
            left = g_llvm_builder.sitofp(left, llvm_type[TY_FLOAT], 'cast_tmp')
        else:
            right = g_llvm_builder.sitofp(right, llvm_type[TY_FLOAT], 'cast_tmp')

    return float_binops[self.op](left, right)


@add_to_class(ast.ID)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    if self.name in named_values:
        # load from stack
        return g_llvm_builder.load(named_values[self.name], self.name)
    else:
        raise NameError("line %d: NameError : name '%s' is not defined"
                        % (self.lineno, self.name))


@add_to_class(ast.Vinteger)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    return lc.Constant.int(lc.Type.int(), self.value)


@add_to_class(ast.Vfloat)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    return lc.Constant.real(lc.Type.float(), self.value)


@add_to_class(ast.Vboolean)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    if self.value:
        v = 1
    else:
        v = 0
    return lc.Constant.int(lc.Type.int(1), v)


@add_to_class(ast.Vstring)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    return lc.Constant.string(self.data)


@add_to_class(ast.Map)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    pass


@add_to_class(ast.Pair)
def generate_code(self, named_values):
    """
    Generates the LLVM code
    :param named_values: The environment
    """
    pass