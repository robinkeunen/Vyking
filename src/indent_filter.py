__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'


class IndentFilter():
    """
    Filter between lex and yacc.
    Reads token streams from lexer and generates appropriate DEDENT.
    Additionally, strips useless NEWLINE tokens.
    """

    