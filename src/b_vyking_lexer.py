__author__ = 'Robin Keunen'
__author__ = 'Pierre Vyncke'

import ply.lex as lex
import test_units
from ply.lex import TOKEN

# basic regex
number = r'([\+-][1-9]\d*)|0'
exponent = r'(e|E)' + number

# Token definitions
# Token defined as functions when an action is needed
# Evaluation order :
#  functions in order of definition
#  definitions in decreasing regex length
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON  = r'\:'
t_NEWLINE = r'\n'
t_EQ = r'=='
t_LOWER = r'<'
t_GREATER = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='


@TOKEN(number + r'\.\d*' + exponent + r'?')
def t_FLOAT(t):
    t.value = float(t.value)
    return t


@TOKEN(number)
def t_INT(t):
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'(True | False)'
    t.value = bool(t.value)
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

t_ignore_whitespace = r'\s'

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
tokens = ['ID',
          'INT',
          'FLOAT',
          'PLUS',
          'MINUS',
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
          'NEQ'] + list(reserved.values())

# Compute column.
#    input is the input text string
#    token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# Error handling rule
# Print offending character and skip
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()
lex.input(test_units.exp1)

for tok in lexer:
    print tok