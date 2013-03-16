__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'

import ply.lex

# Token definitions
# Token defined as functions when an action is needed
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON  = r'\:'
t_NEWLINE = r'\n'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # type is reserved keyword if found in reserved else 'ID'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


# Track line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

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
tokens = ['NUMBER',
          'ID',
          'PLUS',
          'MINUS',
          'TIMES',
          'DIVIDE',
          'LPAREN',
          'RPAREN',
          'COLON',
          'NEWLINE'] + list(reserved.values())

# Compute column.
#    input is the input text string
#    token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column