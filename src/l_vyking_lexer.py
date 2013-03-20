from src.test_units import lex_test
from b_vyking_lexer import BasicVykingLexer
__author__ = 'Robin Keunen'
__author__ = 'pierrevyncke'


class ListedVykingLexer(BasicVykingLexer):
    """ ce coup-ci, c'est bon je crois :)
    """

lexer = ListedVykingLexer()
lex_test(lexer)