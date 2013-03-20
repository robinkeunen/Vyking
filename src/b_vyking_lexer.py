__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'

import ply.lex as lex
from test_units import lex_test
from ply.lex import TOKEN

class BasicVykingLexer:
    """
    Lexer for the Basic Vyking language.
    Basic Viking is a subset of the whole language.
    Lists are not incorporated.
    """

    # basic regex
    number = r'([\+-]?[1-9][0-9]*|0)'
    exponent = r'((e|E)' + number + r')'


    # Reserved keywords
    reserved = {
        'if':     'IF',
        'elif':   'ELIF',
        'else':   'ELSE',
        'while':  'WHILE',
        'and':    'AND',
        'or':     'OR',
        'not':    'NOT',
        'defun':  'DEFUN',
        'return': 'RETURN'
    }


    # Token list
    tokens = ['ID',
              'INT',
              'FLOAT',
              'STRING',
              'PLUS',
              'INC',
              'MINUS',
              'DEC',
              'TIMES',
              'DIVIDE',
              'ASSIGN',
              'LPAREN',
              'RPAREN',
              'COLON',
              'NEWLINE',
              'EQ',
              'LOWER',
              'GREATER',
              'LEQ',
              'GEQ',
              'NEQ',
              'INDENT',
              'COMMA'] + list(reserved.values())


    # Token definitions
    # Token defined as functions when an action is needed
    # Evaluation order :
    #  functions in order of definition
    #  definitions in decreasing regex length
    t_PLUS   = r'\+'
    t_INC    = r'\+='
    t_MINUS  = r'-'
    t_DEC    = r'-='
    t_TIMES  = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COLON  = r'\:'
    t_EQ     = r'=='
    t_LOWER  = r'<'
    t_GREATER = r'>'
    t_LEQ    = r'<='
    t_GEQ    = r'>='
    t_NEQ    = r'!='
    t_COMMA  = r','


    # Ignores whitespaces in lines
    t_ignore_WHITESPACE = r'\s+'


    # states (default is 'INITIAL')
    states = (
        # bol triggered by NEWLINE at beginning of line
        # inclusive states add rules over current state
        ('bol', 'exclusive'),
    )


    def __init__(self):
        self.lexer = lex.lex(module=self)


    def __iter__(self):
        return self.lexer


    def next(self):
        for tok in self.lexer.token():
            yield tok
        raise StopIteration


    def input(self, data):
        self.lexer.input(data)


    def t_begin_bol(self, t):
        r'start_bol'
        #print 'begin bol'
        t.lexer.begin('bol') # starts bol state


    def t_bol_end(self, t):
        r'end_bol'
        #print 'end bol'
        t.lexer.begin('INITIAL') # back to initial state


    @TOKEN(number + r'\.\d*' + exponent + r'?')
    def t_FLOAT(self, t):
        t.value = float(t.value)
        return t


    @TOKEN(number)
    def t_INT(self, t):
        t.value = int(t.value)
        return t


    def t_BOOLEAN(self, t):
        r'(True | False)'
        t.value = bool(t.value)
        return t


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # type is reserved keyword if found in reserved else 'ID'
        t.type = self.reserved.get(t.value, 'ID')
        return t


    def t_COMMENT(self, t):
        r'\#.*'
        pass
        # No return value. Token discarded


    # Track line number
    def t_NEWLINE(self, t):
        r'(\n|\n\r|\r\n)'
        t.lexer.lineno += 1
        self.t_begin_bol(t)
        return t


    def t_STRING(self, t):
        r'(\'.*\'|".*")'
        return t


    # Only active in bol state
    def t_bol_INDENT(self, t):
        r'\s+'
        t.value = len(t.value)
        self.t_bol_end(t)
        return t


    def t_bol_NEWLINE(self, t):
        r'(\n|\n\r|\r\n)'
        t.lexer.lineno += 1
        return t


    # Exits bol state if character is not a whitespace
    def t_bol_exit(self, t):
        r'.'
        self.lexer.lexpos -= 1 # rewind one character
        self.t_bol_end(t)
        t.type = 'INDENT'
        t.value = 0
        return t


    # Compute column.
    #    input is the input text string
    #    token is a token instance
    def find_column(self, token):
        last_cr = lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column


    # Error handling rule
    # Print offending character and skip
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)


    def t_bol_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)




#lexer = BasicVykingLexer()

#lex_test(lexer)

