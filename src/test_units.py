__author__ = 'Robin Keunen'

exp1 = "x = 3 + 42 * (s - t)" \
       ""

exp2 = """
s = 2
t = 3
x = 3 + 42 * (s - t)
"""

dangling_else = """
if a == b:
    a = a + 1
    if a == 2:
        print(x)
    else:
        a = b + 6
        dothis(b+6)
else:
    return func(x, y)
"""

elifStmt = """
if a == b:
    a = a + 1
    return a
elif a > 2:
    if robin < genie:
         return yay
    lo = b/2
elif a == 3:
    return b
else:
    return end
"""

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
    return f_1
    """

inputs = list()
inputs.append(exp1)
inputs.append(exp2)
inputs.append(dangling_else)
inputs.append(elifStmt)
inputs.append(find_bounds)
inputs.append(stringtest)
inputs.append(slow_inverse)


def lex_test(lexer, test_index = -1):

    extended_print = ('ID', 'INT', 'FLOAT', 'STRING', 'WS')

    if test_index == -1:
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
    else:
        data = inputs[test_index]
        lexer.input(data)
        lexer.lineno = 1
        print '"', data, '"'

        for tok in lexer:
            if tok.type == 'NEWLINE':
                print tok.type
            elif tok.type in extended_print:
                print '(' + tok.type + ', ' + str(tok.value) + ')',
            else:
                print tok.type,
        print '\n'

def parse_test(parser, test_index = -1):
    print("dummy")

