__author__ = 'Robin Keunen'

exp1 = "x = 3 + 42 * (s - t)"
ifStmt = """
if a == b:
    a = a + 1
    return a"""

slow_inverse = """
defun slow_inverse(f, delta=1/128.):
    defun f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        if (f(x)-y < y-f(x-delta)):
            return x
        else:
            return x-delta
    return f_1 """

def lex_test(lexer):
    inputs = list()
    inputs.append(exp1)
    inputs.append(ifStmt)
    inputs.append(slow_inverse)

    extended_print = ('ID', 'INT', 'FLOAT')

    for data in inputs:
        lexer.input(data)
        lexer.lineno = 1
        print data
        for tok in lexer:
            if tok.type == 'NEWLINE':
                print tok.type
            elif tok.type == 'INDENT':
                print '(' + tok.type + ', ' + str(tok.value) + ')',
            elif tok.type in extended_print:
                print '(' + tok.type + ', ' + str(tok.value) + ')',
            else:
                print tok.type,
        print "\n"



