from src.test_units import lex_test
from .b_vyking_lexer import BasicVykingLexer
__author__ = 'Robin Keunen'
__author__ = 'pierrevyncke'


class ListedVykingLexer(BasicVykingLexer):

    reserved = {
        'if':     'IF',
        'elif':   'ELIF',
        'else':   'ELSE',
        'while':  'WHILE',
        'and':    'AND',
        'or':     'OR',
        'not':    'NOT',
        'defun':  'DEFUN',
        'return': 'RETURN',
        'is': 'IS',
        'for': 'FOR',
        'apply': 'APPLY',
        'map': 'MAP',
        'cons': 'CONS',
        'append': 'APPEND',
        'list': 'LIST',
        'head': 'HEAD',
        'tail': 'TAIL',
        'in': 'IN'
    }

lexer = ListedVykingLexer()
lex_test(lexer)