from src.test_units import lex_test
from src.b_vyking_lexer import BasicVykingLexer

__author__ = 'Robin Keunen'
__author__ = 'pierrevyncke'


class ListedVykingLexer(BasicVykingLexer):

    new_reserved = {
        'apply': 'APPLY',
        'map': 'MAP',
        'cons': 'CONS',
        'append': 'APPEND',
        'list': 'TY_LIST',
        'head': 'HEAD',
        'tail': 'TAIL',
    }

    reserved = BasicVykingLexer.reserved
    for n, i in new_reserved.items():
        reserved[n] = i

    tokens = BasicVykingLexer.tokens + [
        'LBRACK',
        'RBRACK',
    ] + list(new_reserved.values())

    t_LBRACK = r'\['
    t_RBRACK = r'\]'


addfun = """
defun int add(int a, int b):
   r = a + b
   return r

print(add(1, 2))
"""

chain_add = addfun + """
defun int sum_list(list l):
    if tail(l) == []:
        return head(l)
    else:
        return head(l) + sum_list(tail(l))

ll = [1, 2, 3, 4]
print(sum_list(ll))
"""
