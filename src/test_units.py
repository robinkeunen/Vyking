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

find_bounds = """
defun find_bounds(f, y):
    x = 1.
    while f(x) < y:
        x = x*2.
    if x == 1:
        lo = 0
    else:
        lo = x/2.
    return lo, x
"""

stringtest = """
st = r'string with \' and " into it'
st2 = r"same here, try ' and this \" "
"""

def lex_test(lexer):
    inputs = list()
    inputs.append(exp1)
    inputs.append(ifStmt)
    inputs.append(slow_inverse)
    inputs.append(find_bounds)
    inputs.append(stringtest)

    extended_print = ('ID', 'INT', 'FLOAT', 'STRING')

    for data in inputs:
        lexer.input(data)
        lexer.lineno = 1
        print data
        for tok in lexer:
            if tok.type == 'NEWLINE':
                print tok.type
            elif tok.type == 'WS':
                print '(' + tok.type + ', ' + str(tok.value) + ')',
            elif tok.type in extended_print:
                print '(' + tok.type + ', ' + str(tok.value) + ')',
            else:
                print tok.type,
        print "\n"



