# -----------------------------------------------------------------------------
# indent_filter.py
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

from src.b_vyking_lexer import BasicVykingLexer
from src.ply import lex
from src.stack import Stack
from src.test_units import inputs

__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'


class VykingSyntaxError(Exception):
    pass


class VykingIndentationError(VykingSyntaxError):
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
        self.printer_state = BOL

    def __str__(self):
        if self.read_indent > self.exp_indent:
            return 'Line %i : read indentation is too high : read %i, expected %i' % \
                   {self.lineno, self.read_indent, self.exp_indent}
        elif self.read_indent < self.exp_indent:
            return 'Line %i : expected indentation block : read %i' % \
                {self.lineno, self.read_indent}


class IndentFilter():
    """Filter between lex and yacc.

    Reads token streams from lexer and generates appropriate INDENT
    and DEDENT tokens.
    """

    def __init__(self, lexer):
        """
        Args:
         lexer must be an iterator of token
        """
        self.lexer = lexer
        # Get token list and update it
        self.tokens = self.lexer.tokens # __class__.tokens
        self.tokens.append('INDENT')
        self.tokens.append('DEDENT')
        self.tokens.remove('WS')
        self.indent_level = Stack()
        self.indent_level.push(0)  # Initial level
        self.state = 0  # NO_INDENT level
        # token lookahead
        self.lookahead = None
        self.printer_state = 1

    def __iter__(self):
        """Implemented as a generator object.

        Automatically return an iterator object (technically, a generator object)
        supplying the __iter__() and next() methods.

        """
        return self

    def next(self):
        while True:
            token = self.token()
            if token is None:
                break
            else:
                return token
        raise StopIteration

    def input(self, data):
        self.lexer.lexer.lineno = 1
        self.lexer.input(data)
        self.indent_level.push(0)  # init stack

    def token(self):
        """Returns next token from filtered lexer"""
        # Vyking has 3 indentation states.
        # - no colon hence no need to indent
        # - COLON was read, next rule must be a single line statement
        #   or a block statement
        # - NEWLINE was read after a colon, user must indent
        NO_INDENT = 0
        MAY_INDENT = 1  # COLON was read
        MUST_INDENT = 2  # COLON and NEWLINE were read
        NEED_DEDENT = 3  # WS level is lower than top of stack level
        END_OF_INPUT = 4  # close blocks with DEDENTS

        if self.lookahead is None:
            token = self.lexer.token()
            if token is None:  # end of input
                self.state = END_OF_INPUT
        else:
            token = self.lookahead

        if self.state == NO_INDENT:
            if token.type == "COLON":
                self.state = MAY_INDENT
                return token
            elif token.type == "WS":
                il = self.indent_level.read()
                if token.value > il:
                    raise VykingIndentationError(token.lineno,
                                                 self.indent_level.read() + 1,
                                                 self.indent_level.read())
                elif token.value < il:
                    self.state = NEED_DEDENT
                    self.lookahead = token
                    return self.token()
                else:  # same indentation level
                    return self.token()
            else:
                return token
        elif self.state == MAY_INDENT:
            if token.type == "NEWLINE":
                self.state = MUST_INDENT
            else:
                self.state = NO_INDENT
            return token
        elif self.state == MUST_INDENT:
            if token.type == "WS":
                il = self.indent_level.read()
                if token.value > il:
                    # store new indentation level
                    self.indent_level.push(token.value)
                    self.state = NO_INDENT
                    return self._INDENT(token.lineno)
                else:
                    raise VykingIndentationError(token.lineno,
                                                 self.indent_level.read() + 1,
                                                 self.indent_level.read())
            else:
                raise VykingSyntaxError(token.lineno,
                                        self.indent_level.read() + 1,
                                        self.indent_level.read())
        elif self.state == NEED_DEDENT:
            assert token.type == "WS"
            il = self.indent_level.read()
            if token.value == il:
                self.state = NO_INDENT
                self.lookahead = None
                return self.token()
            elif token.value < il:
                self.indent_level.pop()
                return self._DEDENT(token.lineno)
            else:  # level is not matching stack level
                raise VykingIndentationError(token.lineno,
                                         self.indent_level.read(),
                                         token.value)

        else:  # self.state == END_OF_INPUT
            if self.indent_level.pop() != 0:
                return self._DEDENT(-1)
            else:
                self.state = NO_INDENT
                return None

    def _new_token(self, token_type, lineno):
        """Returns new token

        Args:
            type -- token type
            lineno -- line number of token
        """
        tok = lex.LexToken()
        tok.type = token_type
        tok.value = None
        tok.lineno = lineno
        return tok

    def _DEDENT(self, lineno):
        """Returns DEDENT token"""
        return self._new_token("DEDENT", lineno)

    def _INDENT(self, lineno):
        """Returns INDENT token"""
        return self._new_token("INDENT", lineno)

    def _pretty_print_token(self, token):
        """Pretty prints token on stdout

        Args:
            token -- LexToken to print

        """
        INLINE = 0
        BOL = 1
        extended_print = ('ID', 'INT', 'FLOAT', 'STRING')
        next_line_tokens = ('NEWLINE', 'INDENT', 'DEDENT')

        if self.printer_state == BOL:
            self.printer_state = INLINE
            print str(token.lineno) + " " + self.indent_level.read() * ' ',

        if token.type in next_line_tokens:
            print token.type + '\n',
            self.printer_state = BOL
        elif token.type in extended_print:
            print '(' + token.type + ', ' + str(token.value) + ')',
        else:
            print token.type,

    def _print_input(self, data):
        lineno = 1
        for line in data.split('\n'):
            print lineno, line
            lineno += 1
        print '\n'

    def filter_test(self, test_index=-1):
        """Test the filter on inputs defined in test_units.py

        Args:
            test_id -- index of the program sample to test the filter on
                       test on all inputs if test_id is -1 (default)

        """
        if test_index == -1:
            for data in inputs:
                self.input(data)
                self._print_input(data)
                self.printer_state = 1
                for token in self:
                    self._pretty_print_token(token)
                print '\n'
        else:
            data = inputs[test_index]
            self.input(data)
            self.lexer.lexer.lineno = 1
            self._print_input(data)

            for token in self:
                self._pretty_print_token(token)
            print '\n'


if __name__ == "__main__":
    lexer = BasicVykingLexer(debug=1)
    indent_filter = IndentFilter(lexer)
    indent_filter.filter_test(0)
    indent_filter.input("3-2")
    for t in indent_filter:
        print t
    #indent_filter.filter_test()