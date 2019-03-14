import sys
import ply.yacc as yacc
import scanner

tokens = scanner.tokens

precedence = (
    ("left", '+', '-'),
    ("left", '*', '/'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_expression_binop(p):
    """EXPRESSION   : EXPRESSION '+' EXPRESSION
                    | EXPRESSION '-' EXPRESSION
                    | EXPRESSION '*' EXPRESSION
                    | EXPRESSION '/' EXPRESSION
                    | EXPRESSION DOTADD EXPRESSION
                    | EXPRESSION DOTSUB EXPRESSION
                    | EXPRESSION DOTMUL EXPRESSION
                    | EXPRESSION DOTDIV EXPRESSION"""


def p_expression_rel(p):
    """EXPRESSION   : EXPRESSION '<' EXPRESSION
                    | EXPRESSION '>' EXPRESSION
                    | EXPRESSION GTE EXPRESSION
                    | EXPRESSION LTE EXPRESSION
                    | EXPRESSION NEQ EXPRESSION
                    | EXPRESSION EQ EXPRESSION"""


def p_unary_negation(p):
    """EXPRESSION   : '-' EXPRESSION"""


def p_matrix_transposition(p):
    """"""


# damn I dunno man
def p_matrix_init(p):
    """EXPRESSION   : '[' EXPRESSION ']'"""


def p_matrix_fun(p):
    """EXPRESSION   : EYE '(' EXPRESSION ')'
                    | ZEROS '(' EXPRESSION ')'
                    | ONES '(' EXPRESSION ')'"""


def p_assign(p):
    """EXPRESSION   : EXPRESSION '=' EXPRESSION
                    | EXPRESSION ADDASSIGN EXPRESSION
                    | EXPRESSION SUBASSIGN EXPRESSION
                    | EXPRESSION MULASSIGN EXPRESSION
                    | EXPRESSION DIVASSIGN EXPRESSION"""


def p_conditional(p):
    """EXPRESSION   : IF '(' ID EXPRESSION INT ')' EXPRESSION
                    | IF '(' ID EXPRESSION INT ')' '{' EXPRESSION '}'"""


def p_loop(p):
    """EXPRESSION   : FOR ID '=' INT ':' ID EXPRESSION
                    | FOR ID '=' INT ':' ID '{' EXPRESSION '}'
                    | WHILE '(' ID EXPRESSION INT ')' EXPRESSION
                    | WHILE '(' ID EXPRESSION INT ')' '{' EXPRESSION '}'"""


def p_flow_control(p):
    """EXPRESSION   : BREAK
                    | CONTINUE
                    | RETURN EXPRESSION"""


def p_print(p):
    """EXPRESSION   : PRINT STRING"""


def p_complex_expression(p):
    """EXPRESSION   : '{' EXPRESSION '}'"""


# I dunno man
def p_array(p):
    """EXPRESSION   : '[' INT ',' INT ']'"""


if __name__ == '__main__':
    filename = "example1.m"

    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = yacc.yacc()
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
