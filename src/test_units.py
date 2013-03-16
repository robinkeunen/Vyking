__author__ = 'Robin Keunen'


def lex_test(lexer):
    inputs = list()
    inputs.append("x = 3 + 42 * (s - t)")
    inputs.append("""if a == b:
    a = a + 1
    return a""")

    for data in inputs:
        lexer.input(data)
        print data
        for tok in lexer:
            if tok.type == 'INDENT':
                print '\n(' + tok.type + ', ' + str(tok.value) + ')',
            else:
                print '(' + tok.type + ', ' + str(tok.value) + ')',
        print "\n"



