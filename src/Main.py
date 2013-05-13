__author__ = 'Robin Keunen'

from src.test_units import inputs
import logging

from src.b_vyking_parser import BasicVykingParser

# add methods to abstract syntax tree

import src.type_checking
import src.code_generation

welcome = """
Hi,

Welcome to the vyking compiler.
Would you like to
 1. load a file to compile,
 2. compile one of the test units (cf test_units.py) ?

>> """

action = """
Would you like to :
 1. print the abstract syntax tree
 2. type_check the code
 3. generate llvm code (broken) ?

>> """

def main():

    data = ''

    # while True:
    #     w = input(welcome)
    #     if w == '1':
    #         name = input('Enter filename: ')
    #         with open('name', 'r') as input_file:
    #             for line in input_file:
    #                 data += line
    #     elif w == '2':
    #         print('Choose from the list :')
    #         for i, tu in enumerate(inputs.keys()):
    #             print(' ', tu)
    #         test = input('>> ')
    #         try:
    #             data = inputs[test]
    #         except KeyError:
    #             print('unknown test unit')
    #             continue
    #         break
    #     else:
    #         print("choose 1 or 2")

    # logger object
    logging.basicConfig(
        level=logging.DEBUG,
        filename="parselog.txt",
        filemode="w",
        format="%(message)s"
    )
    log = logging.getLogger()

    # get test case and print
    data = inputs["dangling_else"]

    for lino, line in enumerate(data.splitlines()):
        print("%2d: %s" % (lino, line))
    print()

    parser = BasicVykingParser(debug=log)
    ast = parser.parse(data, debug=log)

    while True:
        #a = input(action)
        a = '3'
        if a == '1':
            print(ast)
            break
        elif a == '2':
            ast.type_check(entry_point=True)
            break
        elif a == '3':
            ast.type_check(entry_point=True)
            print()
            ast.generate_code()
            # Print out all of the generated code.
            print(src.code_generation.g_llvm_module)
            break
        else:
            print("choose 1, 2 or 3")

if __name__ == '__main__':
   main()