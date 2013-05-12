# -----------------------------------------------------------------------------
# scratch.py
# Base class for all expression nodes.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------



class ExpressionNode(object):
   pass

# Expression class for numeric literals like "1.0".
class NumberExpressionNode(ExpressionNode):

   def __init__(self, value):
      """
        INIT
      :param value: value
      """
      self.value = value

   def CodeGen(self):
      """

      Generates de code
      :return:
      """
      return Constant.real(Type.double(), self.value)

# Expression class for referencing a variable, like "a".
class VariableExpressionNode(ExpressionNode):

   def __init__(self, name):
      self.name = name

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      if self.name in g_named_values:
         return g_llvm_builder.load(g_named_values[self.name], self.name)
      else:
         raise RuntimeError('Unknown variable name: ' + self.name)

# Expression class for a binary operator.
class BinaryOperatorExpressionNode(ExpressionNode):

   def __init__(self, operator, left, right):
      self.operator = operator
      self.left = left
      self.right = right

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      # A special case for '=' because we don't want to emit the LHS as an # expression.
      if self.operator == '=':
         # Assignment requires the LHS to be an identifier.
         if not isinstance(self.left, VariableExpressionNode):
            raise RuntimeError('Destination of "=" must be a variable.')

         # Codegen the RHS.
         value = self.right.CodeGen()

         # Look up the name.
         variable = g_named_values[self.left.name]

         # Store the value and return it.
         g_llvm_builder.store(value, variable)

         return value

   left = self.left.CodeGen()
   right = self.right.CodeGen()

   if self.operator == '+':
      return g_llvm_builder.fadd(left, right, 'addtmp')
   elif self.operator == '-':
      return g_llvm_builder.fsub(left, right, 'subtmp')
   elif self.operator == '*':
      return g_llvm_builder.fmul(left, right, 'multmp')
   elif self.operator == '<':
      result = g_llvm_builder.fcmp(FCMP_ULT, left, right, 'cmptmp')
      # Convert bool 0 or 1 to double 0.0 or 1.0.
      return g_llvm_builder.uitofp(result, Type.double(), 'booltmp')
   else:
      function = g_llvm_module.get_function_named('binary' + self.operator)
      return g_llvm_builder.call(function, [left, right], 'binop')

# Expression class for function calls.
class CallExpressionNode(ExpressionNode):

   def __init__(self, callee, args):
      self.callee = callee
      self.args = args

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      # Look up the name in the global module table.
      callee = g_llvm_module.get_function_named(self.callee)

      # Check for argument mismatch error.
      if len(callee.args) != len(self.args):
         raise RuntimeError('Incorrect number of arguments passed.')

      arg_values = [i.CodeGen() for i in self.args]

      return g_llvm_builder.call(callee, arg_values, 'calltmp')

# Expression class for if/then/else.
class IfExpressionNode(ExpressionNode):

   def __init__(self, condition, then_branch, else_branch):
      self.condition = condition
      self.then_branch = then_branch
      self.else_branch = else_branch

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      condition = self.condition.CodeGen()

      # Convert condition to a bool by comparing equal to 0.0.
      condition_bool = g_llvm_builder.fcmp(
         FCMP_ONE, condition, Constant.real(Type.double(), 0), 'ifcond')

      function = g_llvm_builder.basic_block.function

      # Create blocks for the then and else cases. Insert the 'then' block at the
      # end of the function.
      then_block = function.append_basic_block('then')
      else_block = function.append_basic_block('else')
      merge_block = function.append_basic_block('ifcond')

      g_llvm_builder.cbranch(condition_bool, then_block, else_block)

      # Emit then value.
      g_llvm_builder.position_at_end(then_block)
      then_value = self.then_branch.CodeGen()
      g_llvm_builder.branch(merge_block)

      # Codegen of 'Then' can change the current block; update then_block for the
      # PHI node.
      then_block = g_llvm_builder.basic_block

      # Emit else block.
      g_llvm_builder.position_at_end(else_block)
      else_value = self.else_branch.CodeGen()
      g_llvm_builder.branch(merge_block)

      # Codegen of 'Else' can change the current block, update else_block for the
      # PHI node.
      else_block = g_llvm_builder.basic_block

      # Emit merge block.
      g_llvm_builder.position_at_end(merge_block)
      phi = g_llvm_builder.phi(Type.double(), 'iftmp')
      phi.add_incoming(then_value, then_block)
      phi.add_incoming(else_value, else_block)

      return phi

# Expression class for for/in.
class ForExpressionNode(ExpressionNode):

   def __init__(self, loop_variable, start, end, step, body):
      self.loop_variable = loop_variable
      self.start = start
      self.end = end
      self.step = step
      self.body = body

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      # Output this as:
      #   var = alloca double
      #   ...
      #   start = startexpr
      #   store start -> var
      #   goto loop
      # loop:
      #   ...
      #   bodyexpr
      #   ...
      # loopend:
      #   step = stepexpr
      #   endcond = endexpr
      #
      #   curvar = load var
      #   nextvar = curvar + step
      #   store nextvar -> var
      #   br endcond, loop, endloop
      # outloop:

      function = g_llvm_builder.basic_block.function

      # Create an alloca for the variable in the entry block.
      alloca = CreateEntryBlockAlloca(function, self.loop_variable)

      # Emit the start code first, without 'variable' in scope.
      start_value = self.start.CodeGen()

      # Store the value into the alloca.
      g_llvm_builder.store(start_value, alloca)

      # Make the new basic block for the loop, inserting after current block.
      loop_block = function.append_basic_block('loop')

      # Insert an explicit fall through from the current block to the loop_block.
      g_llvm_builder.branch(loop_block)

      # Start insertion in loop_block.
      g_llvm_builder.position_at_end(loop_block)

      # Within the loop, the variable is defined equal to the alloca.  If it
      # shadows an existing variable, we have to restore it, so save it now.
      old_value = g_named_values.get(self.loop_variable, None)
      g_named_values[self.loop_variable] = alloca

      # Emit the body of the loop.  This, like any other expr, can change the
      # current BB.  Note that we ignore the value computed by the body.
      self.body.CodeGen()

      # Emit the step value.
      if self.step:
         step_value = self.step.CodeGen()
      else:
         # If not specified, use 1.0.
         step_value = Constant.real(Type.double(), 1)

      # Compute the end condition.
      end_condition = self.end.CodeGen()

      # Reload, increment, and restore the alloca.  This handles the case where
      # the body of the loop mutates the variable.
      cur_value = g_llvm_builder.load(alloca, self.loop_variable)
      next_value = g_llvm_builder.fadd(cur_value, step_value, 'nextvar')
      g_llvm_builder.store(next_value, alloca)

      # Convert condition to a bool by comparing equal to 0.0.
      end_condition_bool = g_llvm_builder.fcmp(
         FCMP_ONE, end_condition, Constant.real(Type.double(), 0), 'loopcond')

      # Create the "after loop" block and insert it.
      after_block = function.append_basic_block('afterloop')

      # Insert the conditional branch into the end of loop_block.
      g_llvm_builder.cbranch(end_condition_bool, loop_block, after_block)

      # Any new code will be inserted in after_block.
      g_llvm_builder.position_at_end(after_block)

      # Restore the unshadowed variable.
      if old_value is not None:
         g_named_values[self.loop_variable] = old_value
      else:
         del g_named_values[self.loop_variable]

      # for expr always returns 0.0.
      return Constant.real(Type.double(), 0)

# Expression class for a unary operator.
class UnaryExpressionNode(ExpressionNode):

   def __init__(self, operator, operand):
      self.operator = operator
      self.operand = operand

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      operand = self.operand.CodeGen()
      function = g_llvm_module.get_function_named('unary' + self.operator)
      return g_llvm_builder.call(function, [operand], 'unop')

# Expression class for var/in.
class VarExpressionNode(ExpressionNode):

   def __init__(self, variables, body):
      self.variables = variables
      self.body = body

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      old_bindings = {}
      function = g_llvm_builder.basic_block.function

      # Register all variables and emit their initializer.
      for var_name, var_expression in self.variables.iteritems():
         # Emit the initializer before adding the variable to scope, this prevents
         # the initializer from referencing the variable itself, and permits stuff
         # like this:
         #  var a = 1 in
         #    var a = a in ...   # refers to outer 'a'.
         if var_expression is not None:
            var_value = var_expression.CodeGen()
         else:
            var_value = Constant.real(Type.double(), 0)

         alloca = CreateEntryBlockAlloca(function, var_name)
         g_llvm_builder.store(var_value, alloca)

         # Remember the old variable binding so that we can restore the binding
         # when we unrecurse.
         old_bindings[var_name] = g_named_values.get(var_name, None)

         # Remember this binding.
         g_named_values[var_name] = alloca

      # Codegen the body, now that all vars are in scope.
      body = self.body.CodeGen()

      # Pop all our variables from scope.
      for var_name in self.variables:
         if old_bindings[var_name] is not None:
            g_named_values[var_name] = old_bindings[var_name]
         else:
            del g_named_values[var_name]

      # Return the body computation.
      return body

# This class represents the "prototype" for a function, which captures its name,
# and its argument names (thus implicitly the number of arguments the function
# takes), as well as if it is an operator.
class PrototypeNode(object):

   def __init__(self, name, args, is_operator=False, precedence=0):
      """

      :param name: Name of the function
      :param args: Arguments
      :param is_operator: TODO
      :param precedence:
      """
      self.name = name
      self.args = args
      self.is_operator = is_operator
      self.precedence = precedence

   def IsBinaryOp(self):
      """
        Checks if this is a binary operator or not

      :return: true if this is a binary operator
      """
      return self.is_operator and len(self.args) == 2

   def GetOperatorName(self):
      """
        get the name of the operator

      :return: the name of the operator
      """
      assert self.is_operator
      return self.name[-1]

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      # Make the function type, eg. double(double,double).
      funct_type = Type.function(
         Type.double(), [Type.double()] * len(self.args), False)

      function = Function.new(g_llvm_module, funct_type, self.name)

      # If the name conflicted, there was already something with the same name.
      # If it has a body, don't allow redefinition or reextern.
      if function.name != self.name:
         function.delete()
         function = g_llvm_module.get_function_named(self.name)

         # If the function already has a body, reject this.
         if not function.is_declaration:
            raise RuntimeError('Redefinition of function.')

         # If the function took a different number of args, reject.
         if len(function.args) != len(self.args):
            raise RuntimeError('Redeclaration of a function with different number '
                               'of args.')

   # Set names for all arguments and add them to the variables symbol table.
   for arg, arg_name in zip(function.args, self.args):
      arg.name = arg_name

   return function

   # Create an alloca for each argument and register the argument in the symbol
   # table so that references to it will succeed.
   def CreateArgumentAllocas(self, function):
      for arg_name, arg in zip(self.args, function.args):
         alloca = CreateEntryBlockAlloca(function, arg_name)
         g_llvm_builder.store(arg, alloca)
         g_named_values[arg_name] = alloca

# This class represents a function definition itself.
class FunctionNode(object):

   def __init__(self, prototype, body):
      self.prototype = prototype
      self.body = body

   def CodeGen(self):
            """

      Generates de code
      :return:
      """
      # Clear scope.
      g_named_values.clear()

      # Create a function object.
      function = self.prototype.CodeGen()

      # If this is a binary operator, install its precedence.
      if self.prototype.IsBinaryOp():
         operator = self.prototype.GetOperatorName()
         g_binop_precedence[operator] = self.prototype.precedence

      # Create a new basic block to start insertion into.
      block = function.append_basic_block('entry')
      global g_llvm_builder
      g_llvm_builder = Builder.new(block)

      # Add all arguments to the symbol table and create their allocas.
      self.prototype.CreateArgumentAllocas(function)

      # Finish off the function.
      try:
         return_value = self.body.CodeGen()
         g_llvm_builder.ret(return_value)

         # Validate the generated code, checking for consistency.
         function.verify()

         # Optimize the function.
         g_llvm_pass_manager.run(function)
      except:
         function.delete()
         if self.prototype.IsBinaryOp():
            del g_binop_precedence[self.prototype.GetOperatorName()]
         raise

      return function