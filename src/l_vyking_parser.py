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
from src.l_vyking_lexer import ListedVykingLexer

from src.b_vyking_parser import BasicVykingParser, Parser
from src.test_units import inputs


class ListedVykingParser(BasicVykingParser):

    def __init__(self, **kw):
        """
        Parser initializer
        :param kw: keyword arguments
        """
        mylexer = IndentFilter(ListedVykingLexer())
        # FIXME this is very ugly
        super().__init__(lexer=mylexer,
                         start="vyking_input",
                         **kw)
        self.tokens = self.lexer.tokens
        print(self.tokens)


    def p_list_functions(self, p):
        """list_functions : cons_fun
                          | append_fun
                          | pair_fun
                          | head_fun
                          | tail_fun
                          | map_fun
                          | list"""
        p[0] = p[1]

    def p_list(self, p):
        'list: LBRACK args RBRACK'
        args = p[2]
        pair = ast.Pair(args[-1], None)
        args.reverse()
        for i in args[1:]:
            pair = ast.Pair(i, pair)
        p[0] = pair

    def p_cons_fun(self, p):
        """cons_fun : CONS LPAREN clause COMMA pair RPAREN
                     | atom PLUS pair"""
        if len(p) == 7:
            p[0] = ast.Cons(p[3], p[5])
        else:
            p[0] = ast.Cons(p[1], p[3])

    def p_append_fun(self, p):
        """append_fun : APPEND LPAREN pair pair RPAREN
                       | pair PLUS pair"""
        #immutable?
        if len(p) == 6:
            p[0] = ast.Append(p[3], p[4])
        else:
            p[0] = ast.Append(p[1], p[3])

    def p_pair_fun(self, p):
        'pair_fun : LIST LPAREN args RPAREN'

    def p_head_fun(self, p):
        'head_fun : HEAD LPAREN pair RPAREN'
        p[0] = ast.Head(p[3])

    def p_tail_fun(self, p):
        'tail_fun : TAIL LPAREN pair RPAREN'
        p[0] = ast.Tail(p[3])

    def p_map_fun(self, p):
        'map_fun : MAP LAPREN id COMMA pair RPAREN'

if __name__ == '__main__':
    # logger object
    logging.basicConfig(
        level=logging.DEBUG,
        filename="parselog.txt",
        filemode="w",
        format="%(message)s"
    )
    log = logging.getLogger()


    # get test case and print
    data = inputs["fundef"]

    parser = ListedVykingParser(debug=log)
