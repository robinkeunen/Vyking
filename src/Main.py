__author__ = 'Robin Keunen'

from src.test_units import inputs
import logging

from src.b_vyking_parser import BasicVykingParser
# add methods to abstract syntax tree
import src.draw_tree
import src.code_generation

from llvm.passes import FunctionPassManager

from llvm.passes import(PASS_PROMOTE_MEMORY_TO_REGISTER,
                        PASS_INSTRUCTION_COMBINING,
                        PASS_REASSOCIATE,
                        PASS_GVN,
                        PASS_CFG_SIMPLIFICATION)


def main():
   # # Set up the optimizer pipeline. Start with registering info about how the
   # # target lays out data structures.
   # g_llvm_pass_manager.add(g_llvm_executor.target_data)
   # # Promote allocas to registers.
   # g_llvm_pass_manager.add(PASS_PROMOTE_MEMORY_TO_REGISTER)
   # # Do simple "peephole" optimizations and bit-twiddling optzns.
   # g_llvm_pass_manager.add(PASS_INSTRUCTION_COMBINING)
   # # Reassociate expressions.
   # g_llvm_pass_manager.add(PASS_REASSOCIATE)
   # # Eliminate Common SubExpressions.
   # g_llvm_pass_manager.add(PASS_GVN)
   # # Simplify the control flow graph (deleting unreachable blocks, etc).
   # g_llvm_pass_manager.add(PASS_CFG_SIMPLIFICATION)
   #
   # g_llvm_pass_manager.initialize()

   # get test case and print
    data = inputs["exp2"]
    for lino, line in enumerate(data.splitlines()):
        print("%d: %s" % (lino, line))
    print()


    # logger object
    logging.basicConfig(
        level=logging.DEBUG,
        filename="parselog.txt",
        filemode="w",
        format="%(message)s"
    )
    log = logging.getLogger()


    parser = BasicVykingParser(debug=log)
    ast = parser.parse(data, debug=log)

    dot_tree = ast.make_tree_graph()
    dot_tree.write("./tree", format="png")

    print(ast)
    print(ast.generate_code())

    # Print out all of the generated code.
    print('', src.code_generation.g_llvm_module)

if __name__ == '__main__':
   main()