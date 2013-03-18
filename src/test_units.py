__author__ = 'Robin Keunen'

exp1 = "x = 3 + 42 * (s - t)"
ifStmt = """
if a == b:
    a = a + 1
    return a"""

def lex_test(lexer):
    inputs = list()
    inputs.append(exp1)
    inputs.append(ifStmt)

    for data in inputs:
        lexer.input(data)
        print data
        for tok in lexer:
            if tok.type == 'NEWLINE':
                print tok.type
            else:
                print '(' + tok.type + ', ' + str(tok.value) + ')',
        print "\n"



