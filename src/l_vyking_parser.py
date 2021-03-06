# -----------------------------------------------------------------------------
# l_vyking_parser.py
# Parser for the full vyking language (with lists)
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

import logging

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
        super().__init__(lexer=mylexer,
                         start="vyking_input",
                         **kw)
        self.tokens = self.lexer.tokens

    def p_Vtype(self, p):
        """
        Vtype : TY_INT
              | TY_FLOAT
              | TY_STRING
              | TY_FUNC
              | TY_VOID
              | TY_RT
              | TY_LIST
        """
        typemap = {
            'int': 'TY_INT',
            'float': 'TY_FLOAT',
            'string': 'TY_STRING',
            'func': 'TY_FUNC',
            'void': 'TY_VOID',
            'list': 'TY_LIST',
            'runtime_type': 'TY_RT',
        }
        p[0] = typemap[p[1]]

    def p_expression_funcall(self, p):
        """expression : funcall
                      | list_functions"""
        p[0] = p[1]

    def p_list_functions(self, p):
        """list_functions : cons_fun
                          | append_fun
                          | head_fun
                          | tail_fun
                          | map_fun
                          | apply_fun
                          | list"""
        p[0] = p[1]

    def p_pair(self, p):
        'pair : clause'
        p[0] = p[1]

    def p_list(self, p):
        """list : LBRACK args RBRACK
                | LBRACK RBRACK"""
        if len(p) == 4:
            args = p[2]
            pair = ast.Pair(args[-1], None, p.lineno(1), p.lexpos(1))
            args.reverse()
            for i in args[1:]:
                pair = ast.Pair(i, pair, p.lineno(1), p.lexpos(1))
            p[0] = pair
        else:
            p[0] = ast.Pair(None, None, p.lineno(1), p.lexpos(1))

    def p_cons_fun(self, p):
        'cons_fun : CONS LPAREN clause COMMA pair RPAREN'
        if len(p) == 7:
            p[0] = ast.Cons(p[3], p[5], p.lineno(1), p.lexpos(1))
        else:
            p[0] = ast.Cons(p[1], p[3], p.lineno(1), p.lexpos(1))

    def p_append_fun(self, p):
        """append_fun : APPEND LPAREN pair pair RPAREN
                       | pair PLUS pair"""
        #immutable?
        if len(p) == 6:
            p[0] = ast.Append(p[3], p[4], p.lineno(1), p.lexpos(1))
        else:
            p[0] = ast.Append(p[1], p[3], p.lineno(1), p.lexpos(1))

    def p_head_fun(self, p):
        'head_fun : HEAD LPAREN pair RPAREN'
        p[0] = ast.Head(p[3], p.lineno(1), p.lexpos(1))

    def p_tail_fun(self, p):
        'tail_fun : TAIL LPAREN pair RPAREN'
        p[0] = ast.Tail(p[3], p.lineno(1), p.lexpos(1))

    def p_map_fun(self, p):
        'map_fun : MAP LPAREN ID COMMA pair RPAREN'
        p[0] = ast.Map(p[3], p[5], p.lineno(1), p.lexpos(1))

    def p_apply_fun(self, p):
        'apply_fun : APPLY LPAREN ID COMMA pair RPAREN'
        p[0] = ast.Apply(p[3], p[5], p.lineno(1), p.lexpos(1))


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
    data = inputs["n_ary"]
    for i, line in enumerate(data.splitlines()):
        print("%2d: %s" % (i, line))

    parser = ListedVykingParser(debug=log)

    ast = parser.parse(data, debug=log)

    print(ast)
