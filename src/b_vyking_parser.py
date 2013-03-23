__author__ = 'Robin Keunen'

import ply.yacc as yacc
from b_vyking_lexer import BasicVykingLexer


class BasicVykingLexer:

    def __init__(self):
        self.parser = yacc.yacc()

    def test(self, input):


    # Grammar rules

    def p_empty(self, p):
        'empty :'
        pass

    def p_file_input(self, p):
        """file_input : NEWLINE ENDMARKER
                      | statement ENDMARKER"""

    def p_statement(self, p):
        """statement : funcall NEWLINE
                     | if_stat NEWLINE
                     | while_stat NEWLINE
                     | for_stat NEWLINE
                     | let_stat NEWLINE
                     | return_stat NEWLINE
                     | funcdef_stat NEWLINE
                     | import_stat NEWLINE"""

    def p_funcall(self, p):
        """funcall : id LPARENT args RPARENT
                   | id LPARENT RPARENT
                   | list_fun"""
        #if p[2] == '(':
        #else:

    def p_fundef(self, p):
        'fundef : DEFUN id parameters COLON block'

    def p_if_stat(self, p):
        """if_stat : IF test COLON block elif_stat
                   | IF test COLON block elif_stat ELSE COLON block"""

    def p_elif_stat(self, p):
        """elif_stat : ELIF test COLON block
                     | empty"""

    def p_while_stat(self, p):
        'while_stat : WHILE test COLON block'

    def p_for_stat(self, p):
        'for_stat : FOR id IN list COLON block'

    def p_let_stat(self, p):
        """let_stat : id ASSIGN object
                    | id ASSIGN exp"""

    def p_return_stat(self, p):
        """return_stat : RETURN exp
                       | RETURN list"""

    def p_import_stat(self, p):
        'FROM id IMPORT name'

    def p_list_fun(self, p):
        """list_fun : cons_fun
                    | append_fun
                    | list_fun
                    | head_fun
                    | tail_fun
                    | map_fun"""

    def p_cons_fun(self, p):
        """cons_fun : CONS LPAREN list RPAREN
                    | atom PLUS list"""

    def p_append_fun(self, p):
        """append_fun : APPEND LPAREN list RPAREN
                      | list PLUS list"""

    def p_list_fun(self, p):
        'list_fun : LIST LPAREN list RPAREN'

    def p_head_fun(self, p):
        'head_fun : HEAD LPAREN list RPAREN'

    def p_tail_fun(self, p):
        'tail_fun : TAIL LPAREN list RPAREN'

    def p_map_fun(self, p):
        'map_fun : MAP LAPREN id COMMA list RPAREN'

    def p_exp(self, p):
        'exp : add_exp'
        p[0] = p[1]

    def p_add_exp(self, p):
        'add_exp : mul_exp add_exp_aux'

    def p_add_exp_aux(self, p):
        """add_exp_aux : PLUS mul_exp
                       | MINUS mul_exp
                       | empty"""

    def p_mul_exp(self, p):
        'mul_exp : atom mul_exp_aux'

    def p_mul_exp_aux(self, p):
        """mul_exp_aux : TIMES atom
                       | DIVIDE atom
                       | '%' atom
                       | empty"""

    def p_atom(self, p):
        """atom : id
                | int
                | float
                | 'None'
                | bool
                | funcall"""

    def p_block(self, p):
        """block : statement
                 | NEWLINE INDENT stat_aux DEDENT"""

    def p_stat_aux(self, p):
        """stat_aux : statement stat_aux
                    | empty"""

    def p_test(self, p):
        'test : xor_test'

    def p_xor_test(self, p):
        'xor_test : or_test xor_aux'

    def p_xor_aux(self, p):
        """xor_aux : '|' or_test xor_aux
                   | empty"""

    def p_or_test(self, p):
        'or_test : and_test or_aux'

    def p_or_aux(self, p):
        """or_aux : OR and_test or_aux
                  | empty"""

    def p_and_test(self, p):
        'and_test : not_test and_aux'

    def p_and_aux(self, p):
        """and_aux : AND not_test and_aux
                   | empty"""

    def p_not_test(self, p):
        """not_test : NOT not_test
                    | identity
                    | atom"""

    def p_identity(self, p):
        """identity : comparison
                    | comparison EQ atom"""

    def p_comparison(self, p):
        """comparison : exp
                      | exp comp_op exp"""

    def p_parameters(self, p):
        """parameters : LPAREN RPAREN
                      | LPAREN ids RPAREN"""

    def p_ids(self, p):
        """ids : id COMMA ids
               | id"""

    def p_args(self, p):
        """args : arg COMMA args
                | arg"""

    def p_arg(self, p):
        """arg : id
               | funcall
               | exp"""

    def p_list(self, p):
        """list : '[' list_aux object ']'
                | '[' ']'
                | list_fun"""

    def p_list_aux(self, p):
        """list_aux : object COMMA list_aux
                    | empty"""

    def p_object(self, p):
        """object : INT
                  | FLOAT
                  | char
                  | BOOLEAN
                  | STRING
                  | list
                  | id"""

    def p_char(self, p):
        """char : letter
                | digit
                | ' '"""








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


    # Error rule for syntax errors.
    def p_error(self, p):
        print 'Syntax error in input!'
