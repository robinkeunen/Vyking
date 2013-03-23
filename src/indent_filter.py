from src.ply import lex
from src.stack import Stack
__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'


class VykingIndentationError(Exception):
    """Exception raised when the indentation level is incorrect

    Attributes:
        lineno -- line at which the exception occurred
        exp_indent -- expected indent level
        read_indent -- indent level read
    """

    def __init__(self, lineno, exp_indent, read_indent):
        self.lineno = lineno
        self.exp_indent = exp_indent
        self.read_indent = read_indent

    def __str__(self):
        if self.read_indent > self.exp_indent:
            return 'Line %i : read indentation is too high : read %i, expected %i' % \
                   {self.lineno, self.read_indent, self.exp_indent}

class IndentFilter():
    """
    Filter between lex and yacc.
    Reads token streams from lexer and generates appropriate INDENT
    and DEDENT tokens
    Additionally, strips useless NEWLINE tokens.
    """

    # Vyking has 3 indentation states.
    # - no colon hence no need to indent
    # - COLON was read, next rule must be a single line statement
    #   or a block statement
    # - NEWLINE was read after a colon, user must indent
    _NO_INDENT = 0
    _MAY_INDENT = 1 # COLON was read
    _MUST_INDENT = 2 # COLON and NEWLINE were read

    def __init__(self, lexer):
        """
        Args:
         lexer must be an iterator of token
        """
        self.state = IndentFilter._NO_INDENT
        self.lexer = lexer
        self.indent_level = Stack()

    def __iter__(self):
        return self

    def need_DEDENT(self, token):
        """Returns True if DEDENT is needed"""
        if token.value > self.indent_level.read():
            raise VykingIndentationError(token.lineno,
                                         self.indent_level.read(),
                                         token.value)
        elif token.value == self.indent_level.read():
            return False
        else:
            self.indent_level.pop()
            return True

    def _new_token(self, type, lineno):
        """Returns new token

        Args:
            type -- token type
            lineno -- line number of token
        """
        tok = lex.LexToken()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        return tok

    def DEDENT(self, lineno):
        """Returns DEDENT token"""
        return self._new_token("DEDENT", lineno)

    def INDENT(self, lineno):
        """Returns INDENT token"""
        return self._new_token("INDENT", lineno)

    def next(self):
        for token in self.lexer:
            if self.state == IndentFilter._NO_INDENT:
                if token.type == 'COLON':
                    self.state = IndentFilter._MAY_INDENT
                    yield token
                elif token.type == "WS":
                    while self.need_DEDENT(token):
                        yield self.DEDENT(token.lineno - 1)
                else:
                    yield token
            elif self.state == IndentFilter._MAY_INDENT:
                pass
            else: # MUST_INDENT
                pass


