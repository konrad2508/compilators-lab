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


def p_start(p):
    """start    : EXPRESSION"""


def p_number(p):
    """EXPRESSION   : INT
                    | FLOAT"""


def p_expression_binop(p):
    """EXPRESSION   : EXPRESSION '+' EXPRESSION
                    | EXPRESSION '-' EXPRESSION
                    | EXPRESSION '*' EXPRESSION
                    | EXPRESSION '/' EXPRESSION
                    | ID '+' EXPRESSION
                    | ID '-' EXPRESSION
                    | ID '*' EXPRESSION
                    | ID '/' EXPRESSION
                    | ID '+' ID
                    | ID '-' ID
                    | ID '*' ID
                    | ID '/' ID
                    | ID DOTADD ID
                    | ID DOTSUB ID
                    | ID DOTMUL ID
                    | ID DOTDIV ID"""


def p_expression_rel(p):
    """EXPRESSION   : ID '<' EXPRESSION
                    | ID '>' EXPRESSION
                    | ID GTE EXPRESSION
                    | ID LTE EXPRESSION
                    | ID NEQ EXPRESSION
                    | ID EQ EXPRESSION"""


def p_unary_negation(p):
    """EXPRESSION   : '-' ID"""


def p_matrix_transposition(p):
    """EXPRESSION   : ID TRANSPOSE"""


def p_matrix_init(p):
    """EXPRESSION   : '[' EXPRESSION ']'"""


def p_matrix_fun(p):
    """EXPRESSION   : EYE '(' EXPRESSION ')'
                    | ZEROS '(' EXPRESSION ')'
                    | ONES '(' EXPRESSION ')'"""


def p_assign(p):
    """EXPRESSION   : ID '=' EXPRESSION ';'
                    | ID '=' EXPRESSION
                    | ID '=' INT ';'
                    | EXPRESSION '=' INT ';'
                    | ID ADDASSIGN EXPRESSION ';'
                    | ID SUBASSIGN EXPRESSION ';'
                    | ID MULASSIGN EXPRESSION ';'
                    | ID DIVASSIGN EXPRESSION ';'
                    | ID '=' ID ';'
                    | ID ADDASSIGN ID ';'
                    | ID SUBASSIGN ID ';'
                    | ID MULASSIGN ID ';'
                    | ID DIVASSIGN ID ';'
                    | EXPRESSION '=' EXPRESSION ';'
                    | EXPRESSION ADDASSIGN EXPRESSION ';'
                    | EXPRESSION SUBASSIGN EXPRESSION ';'
                    | EXPRESSION MULASSIGN EXPRESSION ';'
                    | EXPRESSION DIVASSIGN EXPRESSION ';'"""


def p_conditional(p):
    """EXPRESSION   : IF '(' EXPRESSION ')' EXPRESSION
                    | ELSE EXPRESSION"""


def p_loop_bound(p):
    """EXPRESSION   : INT ':' ID
                    | ID ':' ID"""


def p_loop(p):
    """EXPRESSION   : FOR EXPRESSION
                    | WHILE '(' EXPRESSION ')' EXPRESSION"""


def p_flow_control(p):
    """EXPRESSION   : BREAK ';'
                    | CONTINUE ';'
                    | RETURN INT ';'
                    | RETURN EXPRESSION ';'"""


def p_print(p):
    """EXPRESSION   : PRINT STRING ';'
                    | PRINT ID ';'
                    | PRINT ID EXPRESSION ';'"""


def p_complex_expression(p):
    """EXPRESSION   : EXPRESSION EXPRESSION
                    | '{' EXPRESSION '}'
                    | '{' EXPRESSION EXPRESSION '}'"""


def p_id_list(p):
    """EXPRESSION   : ',' ID
                    | ',' ID EXPRESSION"""


def p_number_list(p):
    """EXPRESSION   : INT ',' EXPRESSION
                    | INT ';'"""


def p_array(p):
    """EXPRESSION   : ID '[' EXPRESSION ']'"""


if __name__ == '__main__':
    filename = "example3.m"

    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = yacc.yacc()
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
