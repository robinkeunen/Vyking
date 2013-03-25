from src.b_vyking_lexer import BasicVykingLexer
from src.ply import lex
from src.ply.debug_tools import trace
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
        self.indent_level = Stack()
        self.indent_level.push(0)  # Initial level
        self.state = 0  # NO_INDENT level

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
        # Vyking has 3 indentation states.
        # - no colon hence no need to indent
        # - COLON was read, next rule must be a single line statement
        #   or a block statement
        # - NEWLINE was read after a colon, user must indent
        NO_INDENT = 0
        MAY_INDENT = 1 # COLON was read
        MUST_INDENT = 2 # COLON and NEWLINE were read

        self.state = NO_INDENT
        for token in self.lexer:
            if self.state == NO_INDENT:
                if token.type == "COLON":
                    self.state = MAY_INDENT
                    yield token
                elif token.type == "WS":
                    while self.need_DEDENT(token):
                        yield self.DEDENT(token.lineno - 1)
                else:
                    yield token
            elif self.state == MAY_INDENT:
                if token.type == "NEWLINE":
                    self.state = MUST_INDENT
                else:
                    self.state = NO_INDENT
                yield token
            else:  # MUST_INDENT
                if token.type == "WS":
                    if token.value > self.indent_level.read():
                        # Store new indentation level
                        self.indent_level.push(token.value)
                        self.state = NO_INDENT
                        yield self.INDENT(token.lineno)
                    else:
                        raise VykingIndentationError(token.lineno,
                                                     self.indent_level.read() + 1,
                                                     self.indent_level.read())
                else:
                    raise VykingSyntaxError(token.lineno,
                                            self.indent_level.read() + 1,
                                            self.indent_level.read())

        # Yield DEDENTs at end of file
        while self.indent_level.pop() != 0:
            yield self.DEDENT(self.lexer.lexer.lineno)
        raise StopIteration
    
    def pretty_print_token(self, token):
        """Pretty prints token on stdout
        
        Args:
            token -- LexToken to print
            
        """
        extended_print = ('ID', 'INT', 'FLOAT', 'STRING')
        next_line_tokens = ['NEWLINE', 'INDENT', 'DEDENT']

        if token.type in next_line_tokens:
            print token.type + '\n',
            print token.lineno + 1, self.indent_level.read() * ' ',
        elif token.type in extended_print:
            print '(' + token.type + ', ' + str(token.value) + ')',
        else:
            print token.type,

    def print_input(self, data):
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
                self.lexer.input(data)
                self.lexer.lexer.lineno = 1  # init line numbering
                self.indent_level.push(0)  # init stack
                self.print_input(data)

                for token in self.next():  # should work with for token in self
                    self.pretty_print_token(token)
                print '\n'
        else:
            data = inputs[test_index]
            self.lexer.input(data)
            self.lexer.lexer.lineno = 1
            self.print_input(data)

            for token in self.next():  # should work with for token in self
                self.pretty_print_token(token)
            print '\n'


if __name__ == "__main__":
    lexer = BasicVykingLexer()
    indent_filter = IndentFilter(lexer)
    indent_filter.filter_test()

