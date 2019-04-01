import os
import sys

import ply.yacc as yacc

import scanner

tokens = scanner.tokens

precedence = (
    ("nonassoc", "IF"),
    ("nonassoc", "ELSE"),
    ("left", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("left", '<', '>', 'LTE', 'GTE', 'NEQ', 'EQ'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_start(p):
    """start    : operation_chain"""


def p_operation_chain(p):
    """operation_chain  : operation
                        | operation operation_chain"""


def p_operation(p):
    """operation    : '{' operation_chain '}'
                    | simple_operation"""


def p_simple_operation(p):
    """simple_operation : assignment
                        | matrix_assignment
                        | basic_function
                        | if_else
                        | for
                        | while"""


def p_assignment_operator(p):
    """assignment_operator  : '='
                            | ADDASSIGN
                            | SUBASSIGN
                            | MULASSIGN
                            | DIVASSIGN"""


def p_assignment(p):
    """assignment   : ID assignment_operator matrix_function '(' INT ')' ';'
                    | ID assignment_operator expression ';'
                    | ID index_chain assignment_operator expression ';'"""


def p_index_chain(p):
    """index_chain  : '[' index ']'"""


def p_index(p):
    """index    : INT
                | INT ',' index"""


def p_matrix_function(p):
    """matrix_function  : ZEROS
                        | EYE
                        | ONES"""


def p_matrix_assignment(p):
    """matrix_assignment    : ID '=' '[' custom_matrix ']' ';'"""


def p_custom_matrix(p):
    """custom_matrix    : value_chain
                        | value_chain ';' custom_matrix"""


def p_basic_function(p):
    """basic_function   : BREAK ';'
                        | CONTINUE ';'
                        | RETURN value ';'
                        | PRINT value_chain ';'"""


def p_value_chain(p):
    """value_chain  : value
                    | value ',' value_chain"""


def p_value(p):
    """value    : STRING
                | INT
                | FLOAT
                | ID
                | ID index_chain"""


def p_if_else(p):
    """if_else  : IF '(' condition ')' operation ELSE operation
                | IF '(' condition ')' operation"""


def p_condition(p):
    """condition    : expression relational expression"""


def p_relational(p):
    """relational   : '>'
                    | '<'
                    | GTE
                    | LTE
                    | NEQ
                    | EQ """


def p_while(p):
    """while    : WHILE '(' condition ')' operation"""


def p_for(p):
    """for  : FOR ID '=' range operation"""


def p_range(p):
    """range    : ID ':' INT
                | INT ':' ID
                | ID ':' ID"""


def p_expression(p):
    """expression   : '(' expression ')'
                    | '-' expression
                    | expression TRANSPOSE
                    | bin_expr
                    | value"""


def p_bin_expr(p):
    """bin_expr     : expression bin_op value
                    | expression bin_op '(' expression ')'"""


def p_bin_op(p):
    """bin_op   : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""


if __name__ == '__main__':
    filename = "example3.m"

    try:
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    if os.path.exists('parser.out'):
        os.remove('parser.out')

    if os.path.exists('parsetab.py'):
        os.remove('parsetab.py')

    parser = yacc.yacc()
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
