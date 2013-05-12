from src.type_checking import Environment

__author__ = 'Robin Keunen', 'Robin Keunen'

from src.misc import add_to_class
import src.ast as ast
import llvm.core as lc
#import llvm.ee as le
#import llvm.passes as lp

# The LLVM module, which holds all the IR code.
g_llvm_module = lc.Module.new('jit')
# FIXME make this non-global
#ast.ASTNode.llvm_module = lc.Module.new('jit')

# The LLVM instruction builder. Created whenever a new function is entered.
g_llvm_builder = None
# FIXME make this non-global
# ast.ASTNode.llvm_builder = None

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

# helper function
def CreateEntryBlockAlloca(function, ty, var_name):
    """
    Creates an alloca instruction in the entry block of the function.
    This is used for mutable variables.
    """
    entry = function.entry_basic_block
    builder = lc.Builder.new(entry)
    builder.position_at_beginning(entry)
    return builder.alloca(ty, var_name)


@add_to_class(ast.ASTNode)
def generate_code(self, named_values):
    raise NotImplementedError


@add_to_class(ast.Statement_sequence)
def generate_code(self, named_values):
    # create anonymous function to link statements
    # FIXME global module
    # FIXME only

    # make anonymous function on entry point
    global g_llvm_builder
    if g_llvm_builder is None:
        ty = lc.Type.void()
        func_type = lc.Type.function(ty, [])
        function = lc.Function.new(g_llvm_module, func_type, "")
        # Create a new basic block to start insertion into.
        block = function.append_basic_block('top-level')
        g_llvm_builder = lc.Builder.new(block)

    for statement in self.statement_sequence:
        statement.generate_code(named_value)


@add_to_class(ast.Assignment)
def create_local_variable(self):
    """
    Creates a local variable into scope
    """
    function = g_llvm_builder.basic_block.function

    # Register all variables and emit their initializer.
    var_name = self.left.name
    var_expression = self.right
    var_value = var_expression.generate_code(named_value)

    # FIXME type
    alloca = CreateEntryBlockAlloca(function, lc.Type.int(), var_name)
    g_llvm_builder.store(var_value, alloca)

    # Remember the old variable binding so that we can restore the binding
    # when we unrecurse.
    old_bindings[var_name] = self.named_values.get(var_name, None)

    # Remember this binding.
    self.named_values[var_name] = alloca

    # FIXME clean local variables
    # # Pop all our variables from scope.
    # for var_name in self.variables:
    #     if old_bindings[var_name] is not None:
    #         named_values[var_name] = old_bindings[var_name]
    #     else:
    #         del named_values[var_name]

    # Return the body computation.
    return alloca


@add_to_class(ast.Assignment)
def generate_code(self, named_values):
    name = self.left.get_name()
    if name in named_values:
        variable = named_values[name]
        value = self.right.generate_code(named_value)
        g_llvm_builder.store(value, variable)
    else:
        pass
        self.create_local_variable()


@add_to_class(ast.Return)
def generate_code(self, named_values):
    pass


@add_to_class(ast.Funcall)
def generate_code(self, named_values):
    # Look up the name in the global module table.
    f = g_llvm_module.get_function_named(self.name)

    # Check for argument mismatch error.
    if len(f.args) != len(self.args):
        raise RuntimeError('Incorrect number of arguments passed.')

    arg_values = [i.CodeGen() for i in self.args]

    return g_llvm_builder.call(f, arg_values, 'calltmp')


@add_to_class(ast.Print)
def generate_code(self, named_values):
    pass


@add_to_class(ast.If)
def generate_code(self, named_values):
    clause = self.clause.generate_code(named_value)

    # convert to 1-bit bool
    # FIXME type
    condition_bool = g_llvm_builder.icmp(
        lc.ICMP_NE, clause, lc.Constant.real(lc.Type.int(), 0), 'ifcond')

    function = g_llvm_builder.basic_block.function

    # Create blocks for the then and else cases. Insert the 'then' block at the
    # end of the function.
    suite_block = function.append_basic_block('suite')
    closure_block = function.append_basic_block('closure')
    merge_block = function.append_basic_block('ifcond')

    g_llvm_builder.cbranch(condition_bool, suite_block, closure_block)

    # Build suite block
    g_llvm_builder.position_at_end(suite_block)
    suite_value = self.suite.generate_code(named_value)
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    suite_block = g_llvm_builder.basic_block

    # Build closure block
    g_llvm_builder.position_at_end(closure_block)
    closure_value = self.if_closure.generate_code
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    closure_block = g_llvm_builder.basic_block

    # Build merge block.
    g_llvm_builder.position_at_end(merge_block)
    phi = g_llvm_builder.phi(lc.Type.int(), 'iftmp')
    phi.add_incoming(suite_block, suite_block)
    phi.add_incoming(closure_value, closure_block)

    return phi


@add_to_class(ast.Elif)
def generate_code(self, named_values):
    clause = self.clause.generate_code(named_value)

    # convert to 1-bit bool
    # FIXME type
    condition_bool = g_llvm_builder.icmp(
        lc.ICMP_NE, clause, lc.Constant.real(lc.Type.int(), 0), 'elifcond')

    function = g_llvm_builder.basic_block.function

    # Create blocks for the then and else cases. Insert the 'then' block at the
    # end of the function.
    suite_block = function.append_basic_block('suite')
    closure_block = function.append_basic_block('closure')
    merge_block = function.append_basic_block('elifcond')

    g_llvm_builder.cbranch(condition_bool, suite_block, closure_block)

    # Build suite block
    g_llvm_builder.position_at_end(suite_block)
    suite_value = self.suite.generate_code(named_value)
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    suite_block = g_llvm_builder.basic_block

    # Build closure block
    g_llvm_builder.position_at_end(closure_block)
    closure_value = self.if_closure.generate_code
    g_llvm_builder.branch(merge_block)

    # Computation of suite can change de block, get block for the phi node
    closure_block = g_llvm_builder.basic_block

    # Build merge block.
    g_llvm_builder.position_at_end(merge_block)
    phi = g_llvm_builder.phi(lc.Type.int(), 'eliftmp')
    phi.add_incoming(suite_block, suite_block)
    phi.add_incoming(closure_value, closure_block)

    return phi


@add_to_class(ast.Else)
def generate_code(self, named_values):
    return self.suite.generate_code(named_value)


@add_to_class(ast.While)
def generate_code(self, named_values):
    pass


type_code = {
    TY_BOOL: lc.Type.int(1),
    TY_INT: lc.Type.int(),
    TY_FLOAT: lc.Type.float(),
    TY_STRING: None,  # TODO string type as arg http://bit.ly/10PRVKW
    TY_FUNC: None,  # TODO func type as arg
}


# helper function
@add_to_class(ast.Prototype)
def CreateArgumentAllocas(self, function):
    """
    Create an alloca for each argument and register the argument in the symbol
    table so that references to it will succeed.
    """
    for type_name, arg in zip(self.ty_params, function.args):
        ty, name = type_name
        alloca = CreateEntryBlockAlloca(function, lc.Type.int(), name)
        g_llvm_builder.store(arg, alloca)
        named_values[name] = alloca


@add_to_class(ast.Prototype)
def generate_code(self, named_values):
    # Create an alloca for each argument and register the argument in the symbol
    # table so that references to it will succeed.
    pass


@add_to_class(ast.Fundef)
def generate_code(self, named_values):
    # clear scope
    # FIXME closures, might have to play here
    named_values.clear()

    # create function signature
    # FIXME other function types

    func_type = lc.Type.function(lc.Type.int(),
                                 (lc.Type.int(),) * len(self.parameters),
                                 False)
    function = lc.Function.new(g_llvm_module,
                               func_type,
                               self.id.name)

    # FIXME check
    # check if defined?
    # if function.name != self.name:

    # TODO closures
    # add parameters to function block
    for param, p_name in zip(function.args, self.parameters):
        param.name = p_name

    # Create a new basic block to start insertion into.
    block = function.append_basic_block('entry')
    # FIXME make non global
    global g_llvm_builder
    g_llvm_builder = lc.Builder.new(block)

    # Add all arguments to the symbol table and create their allocas.
    self.CreateArgumentAllocas(function)

    # Finish off the function.
    try:
        return_value = self.suite.generate_code(named_value)
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


@add_to_class(ast.Clause)
def generate_code(self, named_values):
    # TODO type check
    # TODO NOT operand
    # TODO grouped clauses or useless? note: p[0] = p[2]

    left = self.left.generate_code(named_value)
    right = self.right.generate_code(named_value)

    return int_binops[self.op](left, right)


@add_to_class(ast.Expression)
def generate_code(self, named_values):
    # TODO type check
    # TODO Uminus -> deal in ast

    left = self.left.generate_code(named_value)
    right = self.right.generate_code(named_value)

    return int_binops[self.op](left, right)


@add_to_class(ast.ID)
def generate_code(self, named_values):
    # TODO scope lookup
    if self.name in named_values:
        # load from stack
        return g_llvm_builder.load(named_values[self.name], self.name)
    else:
        raise NameError("line %d: NameError : name '%s' is not defined"
                        % (self.lineno, self.name))


@add_to_class(ast.Vinteger)
def generate_code(self, named_values):
    return lc.Constant.int(lc.Type.int(), self.value)


@add_to_class(ast.Vfloat)
def generate_code(self, named_values):
    return lc.Constant.real(lc.Type.float(), self.value)


@add_to_class(ast.Vboolean)
def generate_code(self, named_values):
    if self.value:
        v = 1
    else:
        v = 0
    return lc.Constant.int(lc.Type.int(1), v)


@add_to_class(ast.Vstring)
def generate_code(self, named_values):
    return lc.Constant.string(self.data)


@add_to_class(ast.Map)
def generate_code(self, named_values):
    pass


@add_to_class(ast.Pair)
def generate_code(self, named_values):
    pass