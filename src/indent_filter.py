# -----------------------------------------------------------------------------
# indent_filter.py
# Filter between the lexer and the parser.
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

from src.b_vyking_lexer import BasicVykingLexer
from src.ply import lex
from src.stack import Stack
from src.test_units import inputs


class VykingSyntaxError(Exception):
    pass


class VykingIndentationError(VykingSyntaxError):
    """Exception raised when the indentation level is incorrect

    Attributes:
        lineno -- line at which the exception occurred
        exp_indent -- expected indent level
        read_indent -- indent level read
    """

    def __init__(self, lineno, message):
        """
        Exception initializer.
        :param lineno: line number at which exception occured
        :param message: cause of the indentation error
        """
        self.lineno = lineno
        self.message = message

    def __str__(self):
        return "\n\tline %d: %s" % (self.lineno, self.message)


class IndentFilter():
    """Filter between lex and yacc.

    Reads token streams from lexer and generates appropriate INDENT
    and DEDENT tokens.

    Adds ENDMARKER at the end of the input
    """

    def __init__(self, lexer):
        """
        Filter initilizer
        :param lexer: lexer must be an iterator returning tokens
        """
        self.lexer = lexer
        # Get token list and update it
        self.tokens = self.lexer.tokens  # __class__.tokens
        self.tokens.append('INDENT')
        self.tokens.append('DEDENT')
        self.tokens.remove('WS')

    def __iter__(self):
        """Implemented as a generator object.

        Automatically return an iterator object (technically, a generator object)
        supplying the __iter__() and next() methods.

        """
        return self.filter_tokens()

    def __next__(self):
        while True:
            token = self.token()
            if token is None:
                break
            else:
                return token
        raise StopIteration

    def input(self, data):
        """
        Feeds data to the lexer and initialises the filter.
        :param data: String of data to lex and filter
        """
        self.lexer.lexer.lineno = 1
        self.lexer.input(data)
        # make iterator from generator
        self.filtered_stream = iter(self.filter_tokens())
        # printer params
        self.printer_state = 1
        self.level = 0

    def token(self):
        """
        :return: next filtered token
        """
        try:
            return next(self.filtered_stream)
        except StopIteration:
            return None

    def filter_tokens(self):
        """
        Requests tokens from the lexer and adds INDENT and DEDENT
        to the stream where relevant.

        :return: filtered token
        :raise: VykingIndentationError
        """
        # Vyking has 3 indentation states.
        # - no colon hence no need to indent
        # - COLON was read, next rule must be a single line statement
        #   or a block statement
        # - NEWLINE was read after a colon, user must indent
        BOF = 0  # Beginnig of file
        NO_INDENT = 1
        MAY_INDENT = 2  # COLON was read
        MUST_INDENT = 3  # COLON and NEWLINE were read

        # Stack storing indentation levels met
        levels = Stack()
        levels.push(0)

        state = BOF

        # helper function
        def need_DEDENT(token):
            """Returns True if DEDENT is needed"""
            if token.value > levels.read():
                raise VykingIndentationError(token.lineno,
                                             "indentation level is too high.\n"
                                             " \tHint: check for missing colon or mismatch in indentation level.")
            else:
                return token.value < levels.read()

        for token in self.lexer:
            # ignore NEWLINEs at beginning of input
            if state == BOF:
                if token.type == "NEWLINE":
                    continue
                else:
                    state = NO_INDENT

            if state == NO_INDENT:
                if token.type == "COLON":
                    state = MAY_INDENT
                    yield token
                elif token.type == "WS":
                    while need_DEDENT(token):
                        levels.pop()
                        yield self._DEDENT(token.lineno - 1)
                else:
                    yield token

            elif state == MAY_INDENT:
                if token.type == "NEWLINE":
                    state = MUST_INDENT
                else:
                    state = NO_INDENT
                yield token

            else:  # MUST_INDENT
                if token.type == "WS" and token.value > levels.read():
                    # Store new indentation level
                    levels.push(token.value)
                    state = NO_INDENT
                    yield self._INDENT(token.lineno)
                else:
                    raise VykingIndentationError(token.lineno,
                                                 "Expected indentation")

        # Yield DEDENTs at end of input
        while levels.pop() != 0:
            yield self._DEDENT(self.get_lineno())

        #yield self._new_token("ENDMARKER", self.get_lineno())
        yield None

    def _new_token(self, token_type, lineno):
        """Returns new token

        :param token_type: type of token requested
        :param lineno: line number of the token
        """
        tok = lex.LexToken()
        tok.type = token_type
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = self.get_lexpos()
        return tok

    def _DEDENT(self, lineno):
        """Returns DEDENT token"""
        return self._new_token("DEDENT", lineno)

    def _INDENT(self, lineno):
        """Returns INDENT token"""
        return self._new_token("INDENT", lineno)

    def _pretty_print_token(self, token):
        """Pretty prints token on stdout

        :param token: LexToken to print
        """
        INLINE = 0
        BOL = 1
        extended_print = ('ID', 'INT', 'FLOAT', 'STRING')
        next_line_tokens = ('NEWLINE', 'INDENT', 'DEDENT')

        if self.printer_state == BOL:
            self.printer_state = INLINE

            print(str(token.lineno) + self.level * "   ", end=' ')

        if token is None:
            pass
        elif token.type in next_line_tokens:
            if token.type == "INDENT":
                self.level += 1
            elif token.type == "DEDENT":
                self.level -= 1

            print(token.type + '\n', end=' ')
            self.printer_state = BOL
        elif token.type in extended_print:
            print('(' + token.type + ', ' + str(token.value) + ')', end=' ')
        else:
            print(token.type, end=' ')

    def _print_input(self, data):
        """Prints data on stdout"""
        lineno = 1
        for line in data.split('\n'):
            print(lineno, line)
            lineno += 1
        print('\n')

    def get_lexpos(self):
        """Returns the lexing position of the lexer"""
        return self.lexer.get_lexpos()

    def get_lineno(self):
        """Returns the line number of the lexer"""
        return self.lexer.get_lineno()

    def filter_test(self, test_index=-1):
        """Test the filter on inputs defined in test_units.py

        :param test_index: index of the program sample to test the filter on
          test on all inputs if test_id is -1 (default)
        """
        if test_index == -1:
            for data in inputs:
                self.input(data)
                self.lexer.lexer.lineno = 1
                self._print_input(data)

                for token in self.filtered_stream:
                    self._pretty_print_token(token)
                print('\n')

        else:
            data = inputs[test_index]
            self.input(data)
            self.lexer.lexer.lineno = 1
            self._print_input(data)

            for token in self.filtered_stream:
                self._pretty_print_token(token)
            print('\n')


if __name__ == "__main__":
    lexer = BasicVykingLexer(debug=0)
    indent_filter = IndentFilter(lexer)
    indent_filter.filter_test()
