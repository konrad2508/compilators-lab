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
                    | EXPRESSION '/' EXPRESSION"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_rel(p):
    """EXPRESSION   : EXPRESSION '<' EXPRESSION
                    | EXPRESSION '>' EXPRESSION
                    | EXPRESSION '*' EXPRESSION
                    | EXPRESSION '/' EXPRESSION"""


def p_unary_negation(p):
    """"""


def p_matrix_transposition(p):
    """"""


def p_matrix_init(p):
    """"""


def p_matrix_fun(p):
    """"""


def p_assign(p):
    """"""


def p_conditional(p):
    """"""


def p_loop(p):
    """"""


def p_flow_control(p):
    """"""


def p_print(p):
    """"""


def p_complex_expression(p):
    """"""


def p_array(p):
    """"""


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
