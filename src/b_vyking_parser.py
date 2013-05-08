# -----------------------------------------------------------------------------
# b_vyking_parser.py
# Parser for a subset of the vyking language (list free)
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
        # Get arguments
        """
        Parser initializer
        :param lexer: lexer used to tokenize the input
        :param start: start symbol of the grammar
        :param kw: keyword arguments
        """
        self.debug = kw.get('debug', 0)
        self.names = {}
        self.start = start
        # file name for the parse tables
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
            # get token iterator
            self.tokens = self.lexer.tokens

        # Initialise the parser
        self.parser = yacc.yacc(module=self,
                                debug=self.debug,
                                debugfile=self.debugfile,
                                tabmodule=self.tabmodule,
                                start=self.start,
        )

    def parse(self, input=None, lexer=None, debug=0, tracking=0, tokenfunc=None):
        """
        Parses the input
        :param input: string of the data to parse
        :param lexer: lexer to user for the parsing, defaults
               to the one specified on initialization
        :param debug: True to get debugging messages in stdout.
                      Can also receive a logging object to get more precise behaviour
        :param tracking: True to ask the parser to follow line numbers.
        :param tokenfunc: tokenize function
        :return:
        """
        if lexer is None:
            return self.parser.parse(input=input, lexer=self.lexer,
                                     debug=debug, tracking=tracking, tokenfunc=tokenfunc)
        else:
            return self.parser.parse(input=input, debug=debug,
                                     tracking=tracking, tokenfunc=tokenfunc)


class BasicVykingParser(Parser):
    """
    Parser for a parser of a list-free Vyking
    """
    #precedence rules
    precedence = (
        #('nonassoc', 'unmatched_if'),
        #('nonassoc', 'ELSE'),
        #('nonassoc', 'ELIF'),
        ('left', 'AND', 'OR'),
        ('right', 'NOT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('nonassoc', 'LPAREN', 'RPAREN'),
        ('right', 'UMINUS')  # unary minus operator
    )

    # operation dictionary, allows for simpler rules definition.
    operations = {
        'or':  lambda l, r, li, le: ast.Clause(l, 'OR', r, li, le),
        'and': lambda l, r, li, le: ast.Clause(l, 'AND', r, li, le),
        '==':  lambda l, r, li, le: ast.Clause(l, 'EQ', r, li, le),
        '!=':  lambda l, r, li, le: ast.Clause(l, 'NEQ', r, li, le),
        '<':   lambda l, r, li, le: ast.Clause(l, 'LT', r, li, le),
        '>':   lambda l, r, li, le: ast.Clause(l, 'GT', r, li, le),
        '<=':  lambda l, r, li, le: ast.Clause(l, 'LEQ', r, li, le),
        '>=':  lambda l, r, li, le: ast.Clause(l, 'GEQ', r, li, le),
        '+':   lambda l, r, li, le: ast.Expression(l, 'PLUS', r, li, le),
        '-':   lambda l, r, li, le: ast.Expression(l, 'MINUS', r, li, le),
        '*':   lambda l, r, li, le: ast.Expression(l, 'TIMES', r, li, le),
        '/':   lambda l, r, li, le: ast.Expression(l, 'DIVIDE', r, li, le),
        '%':   lambda l, r, li, le: ast.Expression(l, 'MOD', r, li, le),
    }

    def __init__(self, **kw):
        """
        Parser initializer
        :param kw: keyword arguments
        """
        mylexer = IndentFilter(BasicVykingLexer())
        #super(BasicVykingParser, self).__init__(lexer=mylexer,
        super().__init__(lexer=mylexer,
                         start="vyking_input",
                         **kw)
        self.tokens = self.lexer.tokens

    # empty rule
    def p_empty(self, p):
        'empty :'
        pass

    def p_vyking_input(self, p):
        'vyking_input : statement_sequence ENDMARKER'
        p[0] = ast.Statement_sequence(p[1], p.lineno(1), p.lexpos(1))

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
                         | print NEWLINE
                         | name_declaration NEWLINE
                         | extern_declaration NEWLINE
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
            p[0] = ast.Assignment(ast.ID(p[1], p.lineno(1), p.lexpos(1)),
                                  p[3], p.lineno(2), p.lexpos(2))
        elif p[2] == '+=':
            p[0] = ast.Assignment(ast.ID(p[1], p.lineno(1), p.lexpos(1)),
                                  ast.Expression(p[1], "PLUS", p[3], p.lineno(3), p.lexpos(3)),
                                  p.lineno(2), p.lexpos(2))
        elif p[2] == '-=':
            p[0] = ast.Assignment(ast.ID(p[1], p.lineno(1), p.lexpos(1)),
                                  ast.Expression(p[1], "MINUS", p[3], p.lineno(3), p.lexpos(3)),
                                  p.lineno(2), p.lexpos(2))

    def p_return_statement(self, p):
        'return_statement : RETURN expression'
        p[0] = ast.Return(p[2], p.lineno(2), p.lexpos(2))

    def p_funcall(self, p):
        """
        funcall : ID LPAREN args RPAREN
                | ID LPAREN RPAREN
        """
        if len(p) == 5:
            p[0] = ast.Funcall(ast.ID(p[1], p.lineno(1), p.lexpos(1)),
                               p.lineno(0), p.lexpos(0),
                               args=p[3])
        else:
            p[0] = ast.Funcall(ast.ID(p[1], p.lineno(2), p.lexpos(2)),
                               p.lineno(0), p.lexpos(0))

    def p_print(self, p):
        """
        print : PRINT LPAREN expression RPAREN
              | PRINT LPAREN RPAREN
        """
        if len(p) == 5:
            p[0] = ast.Print(p[3], p.lineno(1), p.lexpos(1))
        else:
            p[0] = ast.Print(None, p.lineno(1), p.lexpos(1))

    def p_prototype(self, p):
        """
        prototype : Vtype ID LPAREN typed_params RPAREN
        """
        p[0] = ast.Prototype(p[1],
                             ast.ID(p[2], p.lineno(2), p.lexpos(2)),
                             p[4],
                             p.lineno(1), p.lexpos(1))

    def p_typed_params(self, p):
        """
        typed_params : typed_params COMMA ty_param
                     | ty_param
        """
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_ty_param(self, p):
        """
        ty_param : Vtype ID
        """
        p[0] = (p[1], ast.ID(p[2], p.lineno(2), p.lexpos(2)))

    def p_Vtype(self, p):
        """
        Vtype : TY_INT
              | TY_FLOAT
              | TY_STRING
              | TY_FUNC
              | TY_VOID
              | TY_RT
        """
        p[0] = p[1]

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
        p[0] = ast.If(p[2], p[4], p.lineno(1), p.lexpos(1), if_closure=p[5])

    def p_if_closure(self, p):
        """
        if_closure : elif_statement
                   | ELSE COLON suite
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.Else(p[3], p.lineno(1), p.lexpos(1))

    def p_if_closure_empty(self, p):
        'if_closure : empty'  # %prec unmatched_if'
        p[0] = p[1]

    def p_elif_statement(self, p):
        'elif_statement : ELIF clause COLON suite if_closure'
        p[0] = ast.Elif(p[2], p[4], p.lineno(1), p.lexpos(1), if_closure=p[5])

    def p_while_statement(self, p):
        'while_statement : WHILE clause COLON suite'
        p[0] = ast.While(p[2], p[4], p.lineno(1), p.lexpos(1))

    def p_fundef(self, p):
        'fundef : DEFUN prototype COLON suite'
        p[0] = ast.Fundef(p[2],
                          p[4],
                          p.lineno(1),
                          p.lexpos(1))

    def p_name_declaration(self, p):
        'name_declaration : ID'
        p[0] = ast.Declaration(
            ast.ID(p[1], p.lineno(1), p.lexpos(1)),
            p.lineno(1), p.lexpos(1))

    def p_extern_declaration(self, p):
        """
        extern_declaration : EXTERN prototype
        """
        p[0] = ast.Fundef(p[2], None, p.lineno(1), p.lexpos(1))

    # def p_parameters(self, p):
    #     """
    #     parameters : parameters COMMA ID
    #                | ID
    #     """
    #     if len(p) == 4:
    #         p[0] = p[1] + [ast.ID(p[3], p.lineno(3), p.lexpos(3))]
    #     else:
    #         p[0] = [ast.ID(p[1], p.lineno(1), p.lexpos(1))]

    def p_suite(self, p):
        """
        suite : simple_statement
              | NEWLINE INDENT statement_sequence DEDENT
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.Statement_sequence(p[3], p.lineno(3), p.lexpos(3))

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
            p[0] = ast.Clause(None, "NOT", p[2], p.lineno(1), p.lexpos(1))
        elif p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = self.operations[p[2]](p[1], p[3], p.lineno(2), p.lexpos(2))

    def p_clause_exp(self, p):
        'clause : expression'
        p[0] = p[1]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression MOD expression
        """
        # get function in operation dictionnary
        p[0] = self.operations[p[2]](p[1], p[3], p.lineno(2), p.lexpos(2))

    # unary minus
    def p_expression_uminus(self, p):
        'expression : MINUS expression %prec UMINUS'
        p[0] = ast.Expression(None, 'UMINUS', p[2], p.lineno(2), p.lexpos(2))

    def p_expression_numeric(self, p):
        'expression : numeric'
        p[0] = p[1]

    def p_numeric_int(self, p):
        'numeric : INT'
        p[0] = ast.Vinteger(p[1], p.lineno(1), p.lexpos(1))

    def p_numeric_float(self, p):
        'numeric : FLOAT'
        p[0] = ast.Vfloat(p[1], p.lineno(1), p.lexpos(1))

    def p_expression_id(self, p):
        'expression : ID'
        p[0] = ast.ID(p[1], p.lineno(1), p.lexpos(1))

    def p_expression_string(self, p):
        'expression : STRING'
        p[0] = ast.Vstring(p[1], p.lineno(1), p.lexpos(1))

    def p_expression_funcall(self, p):
        'expression : funcall'
        p[0] = p[1]

    def p_expression_boolean(self, p):
        'expression : BOOLEAN'
        p[0] = ast.Vboolean(p[1], p.lineno(1), p.lexpos(1))

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
            print('line %d: Syntax error when reading %s ' % (p.lineno, str(p)))

    # helper function
    def new_token(self, token_type, lineno):
        """Returns new token

        :param token_type: token type
        :param lineno: line number of token
        """
        tok = lex.LexToken()
        tok.type = token_type
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = self.lexer.get_lexpos()
        return tok

# Usage
if __name__ == "__main__":
    import src.draw_tree

    all = False
    if all:
        for item, data in inputs.items():
            for lino, line in enumerate(data.splitlines()):
                print("%d: %s" % (lino, line))
            print()

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
            if result is not None:
                tree = result.make_tree_graph()
                tree.write("./trees/" + item, format="png")
            print(result)
    else:
        data = inputs["dangling_else"]
        for lino, line in enumerate(data.splitlines()):
            print("%d: %s" % (lino, line))
        print()

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
        if result is not None:
            tree = result.make_tree_graph()
            tree.write("./trees/tree", format="png")
        print(result)



