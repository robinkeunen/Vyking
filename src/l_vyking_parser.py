# -----------------------------------------------------------------------------
# b_vyking_parser.py
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

import logging
import sys
import ast
import os
import ply.lex as lex
import ply.yacc as yacc
from src.indent_filter import IndentFilter
from src.test_units import inputs

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

from .b_vyking_lexer import BasicVykingLexer
from .b_vyking_parser import BasicVykingParser

class ListVykingParser(BasicVykingParser):

     def p_list_fun(self, p):
         """list_fun : cons_fun
                     | append_fun
                     | list_fun
                     | head_fun
                     | tail_fun
                     | map_fun"""

     def p_cons_fun(self, p):
         """cons_fun : CONS LPAREN clause list RPAREN
                     | atom PLUS list"""

     def p_append_fun(self, p):
         """append_fun : APPEND LPAREN list list RPAREN
                       | list PLUS list"""

     def p_list_fun(self, p):
         'list_fun : LIST LPAREN args RPAREN'

     def p_head_fun(self, p):
         'head_fun : HEAD LPAREN list RPAREN'

     def p_tail_fun(self, p):
         'tail_fun : TAIL LPAREN list RPAREN'

     def p_map_fun(self, p):
         'map_fun : MAP LAPREN id COMMA list RPAREN'