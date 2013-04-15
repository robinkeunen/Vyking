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




class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    precedence = ()


    def __init__(self, lexer=None, start=None, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        self.start = start
        dbg_filename = self.__class__.__name__
        self.debugfile = dbg_filename + ".dbg"
        self.tabmodule = dbg_filename + "_" + "parsetab"
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
                                tabmodule=self.tabmodule,
                                start=self.start
                                )

    def run(self):
        while 1:
            try:
                s = raw_input('input > ')
            except EOFError:
                break
            if not s: continue
            self.parse(s)

    def parse(self, input=None, lexer=None, debug=0, tracking=0, tokenfunc=None):
        if lexer is None:
            return self.parser.parse(input=input, lexer=self.lexer,
                                     debug=debug, tracking=tracking, tokenfunc=tokenfunc)
        else:
            return self.parser.parse(input=input, debug=debug,
                                     tracking=tracking, tokenfunc=tokenfunc)


class BasicVykingParser(Parser):
    precedence = (
        ('nonassoc', 'unmatched_if'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'ELIF'),
        ('left', 'AND', 'OR'),
        ('nonassoc', 'NOT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right', 'UMINUS')  # unary minus operator
    )

    def __init__(self, **kw):
        mylexer = IndentFilter(BasicVykingLexer())
        super(BasicVykingParser, self).__init__(lexer=mylexer,
                                                start="vyking_input",
                                                **kw)
        self.tokens = self.lexer.tokens


    def p_empty(self, p):
        'empty :'
        pass


    def p_vyking_input(self, p):
        'vyking_input : statement_sequence ENDMARKER'
        p[0] = ast.Statement_sequence(p[1])


    def p_statement_sequence(self, p):
        """
        statement_sequence : statement statement_sequence
                           | statement
        """
        # tuple of the statements
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_statement(self, p):
        """
        statement : simple_statement
                  | compound_statement
        """
        p[0] = p[1]


    def p_simple_statement(self, p):
        """
        simple_statement : assignment NEWLINE
                         | return_statement NEWLINE
                         | funcall NEWLINE
        """
        p[0] = p[1]


    def p_compound_statement(self, p):
        """
        compound_statement : if_statement
                           | while_statement
                           | fundef
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : ID ASSIGN clause
                   | ID INC expression
                   | ID DEC expression
        """
        if p[2] == '=':
            p[0] = ast.Assignment(p[1], p[3])
        elif p[2] == '+=':
            p[0] = ast.Assignment(p[1], ast.Expression(p[1], "PLUS", p[3]))
        elif p[2] == '-=':
            p[0] = ast.Assignment(p[1], ast.Expression(p[1], "MINUS", p[3]))


    def p_return_statement(self, p):
        'return_statement : RETURN expression'
        p[0] = ast.Return(p[2])


    def p_funcall(self, p):
        """
        funcall : ID LPAREN args RPAREN
                | ID LPAREN RPAREN
        """
        if len(p) == 5:
            p[0] = ast.Funcall(ast.ID(p[1]), p[3])
        else:
            p[0] = ast.Funcall(ast.ID(p[1]))


    def p_args(self, p):
        """
        args : args COMMA clause
             | clause
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]


    def p_if_statement(self, p):
        """
        if_statement : IF clause COLON suite if_closure
        """
        p[0] = ast.If(p[2], p[4], p[5])


    def p_if_closure(self, p):
        """
        if_closure : elif_statement %prec ELIF
                   | ELSE COLON suite
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.Else(p[3])


    def p_if_closure_empty(self, p):
        'if_closure : empty %prec unmatched_if'
        p[0] = p[1]


    def p_elif_statement(self, p):
        'elif_statement : ELIF clause COLON suite if_closure'
        p[0] = ast.Elif(p[2], p[4], p[5])


    def p_while_statement(self, p):
        'while_statement : WHILE clause COLON suite'
        p[0] = ast.While(p[2], p[4])


    def p_fundef(self, p):
        'fundef : DEFUN ID LPAREN parameters RPAREN COLON suite'
        p[0] = ast.Fundef(ast.ID(p[2]), p[7], p[4])

    # resynchronization attempt
    def p_fundef_error(self, p):
        'fundef : DEFUN ID error parameters RPAREN COLON suite'
        sys.stderr.write("line%d: expected opening parentheses, attempting to fix...")
        p[0] = ast.Fundef(ast.ID(p[2]), p[7], p[4])

    def p_parameters(self, p):
        """
        parameters : parameters COMMA ID
                   | ID
        """
        if len(p) == 4:
            p[0] = p[1] + [ast.ID(p[3])]
        else:
            p[0] = [ast.ID(p[1])]


    def p_suite(self, p):
        """
        suite : simple_statement
              | NEWLINE INDENT statement_sequence DEDENT
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.Statement_sequence(p[3])


    def p_clause(self, p):
        """
        clause : NOT clause
             | LPAREN clause RPAREN
             | clause OR clause
             | clause AND clause
             | expression EQ expression
             | expression NEQ expression
             | expression LT expression
             | expression GT expression
             | expression GEQ expression
             | expression LEQ expression
        """
        if len(p) == 3:
            p[0] = ast.Clause(None, "NOT", p[2])
        elif p[1] == '(':
            p[0] = p[2]
        elif p[2] == 'or':
            p[0] = ast.Clause(p[1], "OR", p[3])
        elif p[2] == 'and':
            p[0] = ast.Clause(p[1], "AND", p[3])
        elif p[2] == '==':
            p[0] = ast.Clause(p[1], "EQ", p[3])
        elif p[2] == '!=':
            p[0] = ast.Clause(p[1], "NEQ", p[3])
        elif p[2] == '<':
            p[0] = ast.Clause(p[1], "LT", p[3])
        elif p[2] == '>':
            p[0] = ast.Clause(p[1], "GT", p[3])
        elif p[2] == '<=':
            p[0] = ast.Clause(p[1], "LEQ", p[3])
        elif p[2] == '>=':
            p[0] = ast.Clause(p[1], "GEQ", p[3])


    def p_clause_exp(self, p):
        'clause : expression'
        p[0] = p[1]


    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression MOD expression
        """
        #print [repr(p[i]) for i in range(0,4)]
        if p[2] == '+':
            p[0] = ast.Expression(p[1], 'PLUS', p[3])
        elif p[2] == '-':
            p[0] = ast.Expression(p[1], 'MINUS', p[3])
        elif p[2] == '*':
            p[0] = ast.Expression(p[1], 'TIMES', p[3])
        elif p[2] == '/':
            p[0] = ast.Expression(p[1], 'DIVIDE', p[3])
        elif p[2] == '%':
            p[0] = ast.Expression(p[1], 'MOD', p[3])


    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = ast.Expression(None, 'UMINUS', p[2])

    def p_expression_numeric(self, p):
        'expression : numeric'
        p[0] = p[1]


    def p_numeric_int(self, p):
        'numeric : INT'
        p[0] = ast.Vinteger(p[1])


    def p_numeric_float(self, p):
        'numeric : FLOAT'
        p[0] = ast.Vfloat(p[1])


    def p_expression_id(self, p):
        'expression : ID'
        p[0] = ast.ID(p[1])


    def p_expression_string(self, p):
        'expression : STRING'
        p[0] = ast.Vstring(p[1])


    def p_expression_funcall(self, p):
        'expression : funcall'
        p[0] = p[1]

    def p_expression_boolean(self, p):
        'expression : BOOLEAN'
        p[0] = ast.Vboolean(p[1])

    # Error rule for syntax errors.
    def p_error(self, p):
        if p is None:
            print("fix for missing line")
            self.parser.errok()
            return self.new_token("ENDMARKER", self.lexer.get_lineno())

        elif p.type == "ENDMARKER":
            print("line %d: Missing new line at end of file." % p.lineno)
            p.lexer.lookahead = p
            self.parser.errok()
            return self.new_token("NEWLINE", p.lineno)
        else:
            print('line %d: Syntax error when reading %s ' % (p.lineno, str(self, p)))

    # helper function
    def new_token(self, token_type, lineno):
        """Returns new token

        Args:
            type -- token type
            lineno -- line number of token
        """
        tok = lex.LexToken()
        tok.type = token_type
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = self.lexer.get_lexpos()
        return tok


# Usage
if __name__ == "__main__":
    data = inputs["find_bounds"]
    print(data)
    # logger object
    logging.basicConfig(
        level=logging.DEBUG,
        filename="parselog.txt",
        filemode="w",
        format="%(message)s"
    )
    log = logging.getLogger()

    parser = BasicVykingParser(debug=log)
    result = parser.parse(data, debug=log)
    print(result)



