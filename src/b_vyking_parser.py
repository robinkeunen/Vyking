# -----------------------------------------------------------------------------
# b_vyking_parser.py
# authors : Robin Keunen, Pierre Vyncke
# -----------------------------------------------------------------------------

import sys
from src.indent_filter import IndentFilter

sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex
import ply.yacc as yacc
import os

from b_vyking_lexer import BasicVykingLexer

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    precedence = ()


    def __init__(self, lexer=None, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        if lexer is None:
            self.tokens = ()
            self.lexer = lex.lex(module=self, debug=self.debug)
        else:
            self.lexer = lexer
            self.tokens = self.lexer.tokens


        self.parser = yacc.yacc(module=self,
                                debug=self.debug,
                                debugfile=self.debugfile,
                                tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            if not s: continue
            self.parse(s)

    def parse(self,input=None, lexer=None, debug=0, tracking=0, tokenfunc=None):
        if lexer is None:
            self.parser.parse(input=input, lexer=self.lexer,
                              debug=debug, tracking=tracking, tokenfunc=tokenfunc)
        else:
            self.parser.parse(input=input, debug=debug,
                              tracking=tracking, tokenfunc=tokenfunc)


class BasicVykingParser(Parser):

    def __init__(self, **kw):
        mylexer = IndentFilter(BasicVykingLexer())
        super(BasicVykingParser, self).__init__(lexer=mylexer, **kw)
        #self.lexer = IndentFilter(BasicVykingLexer())
        self.tokens = self.lexer.tokens

# Grammar rules

    #def p_empty(self, p):
    #     'empty :'
    #     pass

    # def p_file_input(self, p):
    #     """file_input : NEWLINE ENDMARKER
    #                   | statement ENDMARKER"""
    #
    # def p_statement(self, p):
    #     """statement : funcall NEWLINE
    #                  | if_stat NEWLINE
    #                  | while_stat NEWLINE
    #                  | for_stat NEWLINE
    #                  | let_stat NEWLINE
    #                  | return_stat NEWLINE
    #                  | funcdef_stat NEWLINE
    #                  | import_stat NEWLINE"""
    #
    # def p_funcall(self, p):
    #     """funcall : id LPARENT args RPARENT
    #                | id LPARENT RPARENT
    #                | list_fun"""
    #     #if p[2] == '(':
    #     #else:
    #
    # def p_fundef(self, p):
    #     'fundef : DEFUN id parameters COLON block'
    #
    # def p_if_stat(self, p):
    #     """if_stat : IF test COLON block elif_stat
    #                | IF test COLON block elif_stat ELSE COLON block"""
    #
    # def p_elif_stat(self, p):
    #     """elif_stat : ELIF test COLON block
    #                  | empty"""
    #
    # def p_while_stat(self, p):
    #     'while_stat : WHILE test COLON block'
    #
    # # def p_for_stat(self, p):
    # #     'for_stat : FOR id IN list COLON block'
    #
    # def p_let_stat(self, p):
    #     """let_stat : id ASSIGN object
    #                 | id ASSIGN exp"""
    #
    # def p_return_stat(self, p):
    #     """return_stat : RETURN exp
    #                    | RETURN list"""
    #

    #
    # def p_exp(self, p):
    #     'exp : add_exp'
    #     p[0] = p[1]
    #
    # def p_add_exp(self, p):
    #     'add_exp : mul_exp add_exp_aux'
    #
    # def p_add_exp_aux(self, p):
    #     """add_exp_aux : PLUS mul_exp
    #                    | MINUS mul_exp
    #                    | empty"""
    #
    # def p_mul_exp(self, p):
    #     'mul_exp : atom mul_exp_aux'
    #
    # def p_mul_exp_aux(self, p):
    #     """mul_exp_aux : TIMES atom
    #                    | DIVIDE atom
    #                    | '%' atom
    #                    | empty"""
    #
    # def p_atom(self, p):
    #     """atom : id
    #             | int
    #             | float
    #             | 'None'
    #             | bool
    #             | funcall"""
    #
    # def p_block(self, p):
    #     """block : statement
    #              | NEWLINE INDENT stat_aux DEDENT"""
    #
    # def p_stat_aux(self, p):
    #     """stat_aux : statement stat_aux
    #                 | empty"""
    #
    # def p_test(self, p):
    #     'test : xor_test'
    #
    # def p_xor_test(self, p):
    #     'xor_test : or_test xor_aux'
    #
    # def p_xor_aux(self, p):
    #     """xor_aux : '|' or_test xor_aux
    #                | empty"""
    #
    # def p_or_test(self, p):
    #     'or_test : and_test or_aux'
    #
    # def p_or_aux(self, p):
    #     """or_aux : OR and_test or_aux
    #               | empty"""
    #
    # def p_and_test(self, p):
    #     'and_test : not_test and_aux'
    #
    # def p_and_aux(self, p):
    #     """and_aux : AND not_test and_aux
    #                | empty"""
    #
    # def p_not_test(self, p):
    #     """not_test : NOT not_test
    #                 | identity
    #                 | atom"""
    #
    # def p_identity(self, p):
    #     """identity : comparison
    #                 | comparison EQ atom"""
    #
    # def p_comparison(self, p):
    #     """comparison : exp
    #                   | exp comp_op exp"""
    #
    # def p_parameters(self, p):
    #     """parameters : LPAREN RPAREN
    #                   | LPAREN ids RPAREN"""
    #
    # def p_ids(self, p):
    #     """ids : id COMMA ids
    #            | id"""
    #
    # def p_args(self, p):
    #     """args : arg COMMA args
    #             | arg"""
    #
    # def p_arg(self, p):
    #     """arg : id
    #            | funcall
    #            | exp"""
    #
    # def p_list(self, p):
    #     """list : '[' list_aux object ']'
    #             | '[' ']'
    #             | list_fun"""
    #
    # def p_list_aux(self, p):
    #     """list_aux : object COMMA list_aux
    #                 | empty"""
    #
    # def p_object(self, p):
    #     """object : INT
    #               | FLOAT
    #               | char
    #               | BOOLEAN
    #               | STRING
    #               | list
    #               | id"""
    #
    # def p_char(self, p):
    #     """char : letter
    #             | digit
    #             | ' '"""


    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = ('+', p[1], p[3])

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = ('-', p[1], p[3])

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = ('*', p[1], p[3])

    def p_term_div(self, p):
        'term : term DIVIDE factor'
        p[0] = ('/', p[1], p[3])

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_int(self, p):
        'factor : INT'
        p[0] = ('INT', p[1])

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    # Error rule for syntax errors.
    def p_error(self, p):
        print 'Syntax error in input! ' + str(p)


# Usage
if __name__ == "__main__":

    parser = BasicVykingParser()
    print
    result = parser.parse("3+2", tracking=0, debug=1)
    print
    print result


