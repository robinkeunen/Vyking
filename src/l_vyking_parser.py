# -----------------------------------------------------------------------------
# b_vyking_parser.py
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

import logging
import sys
import src.ast as ast
import ply.lex as lex
import ply.yacc as yacc
from src.indent_filter import IndentFilter
from src.test_units import inputs
from src.b_vyking_lexer import BasicVykingLexer

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

from .b_vyking_lexer import BasicVykingLexer
from .b_vyking_parser import BasicVykingParser

class ListVykingParser(BasicVykingParser):

     def p_pair_fun(self, p):
         """pair_fun : cons_fun
                     | append_fun
                     | pair_fun
                     | head_fun
                     | tail_fun
                     | map_fun"""
         
    def p_list(self, p):
        '[args]'
    
    def p_cons_fun(self, p):
         """cons_fun : CONS LPAREN clause COMMA pair RPAREN
                     | atom PLUS pair"""
         if len(7):
             p[0] = ast.Pair(p[3], p[5])
         else:
             p[0] = ast.Pair(p[1], p[3])

    def p_append_fun(self, p):
         """append_fun : APPEND LPAREN pair pair RPAREN
                       | pair PLUS pair"""
         if len(6):
             temp = p[3)]
             while temp.tail

     def p_pair_fun(self, p):
         'pair_fun : LIST LPAREN args RPAREN'

     def p_head_fun(self, p):
         'head_fun : HEAD LPAREN pair RPAREN'
         p[0] = p[3].head

     def p_tail_fun(self, p):
         'tail_fun : TAIL LPAREN pair RPAREN'
         p[0] = p[3].tail

     def p_map_fun(self, p):
         'map_fun : MAP LAPREN id COMMA pair RPAREN'