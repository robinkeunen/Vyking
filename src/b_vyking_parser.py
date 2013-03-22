__author__ = 'Robin Keunen'

import ply.yacc as yacc
from b_vyking_lexer import BasicVykingLexer


class BasicVykingLexer:

    def __init__(self):
        self.parser = yacc.yacc()

    def test(self, input):


    # Grammar rules

    def p_funcall(self, p):
        '''funcall : id LPARENT args RPARENT
                    | list_fun'''
        if p[2] == '(':
            # Premier cas
        else:
            # Second cas

    def p_fundef(self, p):
        'fundef : DEFUN id parameters COLON block'
        # bla bla bla



    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]

    def p_term_div(self, p):
        'term : term DIVIDE factor'
        p[0] = p[1] / p[3]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(self, p):
        'factor : number'
        p[0] = p[1]

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_number_int(self, p):
        'number : INT'
        p[0] = p[1]

    def p_number_float(self, p):
        'number : FLOAT'
        p[0] = p[1]


    # Error rule for syntax errors.
    def p_error(self, p):
        print 'Syntax error in input!'
