import sys
import ply.yacc as yacc
import scanner
import os

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
    """start    : operation"""


def p_dupcio(p):
    """operation : operation operation
                | simple_operation
                | if_flow
                | for_flow
                | while_flow"""

def p_simple_operation(p):
    """simple_operation : assignment
                        | matrix_assignment
                        | spec_function"""

def p_assignment(p):
    """assignment   : ID '=' assignment_expression ';'
                    | ID element '=' expression ';'"""

def p_element(p):
    """element  : '[' index ']"""

def p_index(p):
    """index    : INT
                | INT ',' index"""

def p_assignment_expression(p):
    """assignment_expression    : matrix_func '(' INT ')'
                                | expression"""

def p_val(p):
    """val  : INT
            | FLOAT"""

def p_matrix_assignment(p):
    """matrix_assignment    : ID '=' '[' matrix_row ']' ';'"""

def p_matrix_row(p):
    """matrix_row   : matrix_row ';' matrix_row
                    | matrix_el"""

def p_matrix_el(p):
    """matrix_el    : val ',' val
                    | val"""

def p_spec_function(p):
    """spec_function    : BREAK ';'
                        | CONTINUE ';'
                        | RETURN simple_val ';'
                        | PRINT '(' simple_val ')' ';'"""

def p_simple_val(p):
    """simple_val   : ID
                    | ID element
                    | val"""
    # add STRING here?

def p_if_flow(p):
    """if_flow  : IF '(' condition ')' next_op"""

def p_condition_val(p):
    """condition    : val '>' val
                    | val '<' val
                    | val GTE val
                    | val LTE val
                    | val NEQ val
                    | val EQ val"""

def p_condition_id(p):
    """condition    : ID '>' val
                    | ID '<' val
                    | ID GTE val
                    | ID LTE val
                    | ID NEQ val
                    | ID EQ val"""

def p_next_op(p):
    """next_op  : simple_operation
                | '{' operation '}'"""

def p_while_flow(p):
    """while_flow   : WHILE '(' condition ')' next_op"""

def p_for_flow(p):
    """for_flow : FOR ID '=' range next_op"""

def p_range(p):
    """range    : INT ':' INT
                | INT ':' ID"""

def p_bin_op(p):
    """bin_op   : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""

# WIP
def p_expression(p):
    """expression   : """

def p_simple_expression(p):
    """simple_expression    : """
# WIP ENDS

# UNCHARTED TERRITORIES BORDER
def p_expression_binop(p):
    """EXPRESSION   : EXPRESSION '+' EXPRESSION ';'
                    | EXPRESSION '-' EXPRESSION ';'
                    | EXPRESSION '*' EXPRESSION ';'
                    | EXPRESSION '/' EXPRESSION ';'"""


def p_mixed_binop(p):
    """EXPRESSION   : ID '+' EXPRESSION ';'
                    | ID '-' EXPRESSION ';'
                    | ID '*' EXPRESSION ';'
                    | ID '/' EXPRESSION ';'"""


def p_id_binop(p):
    """EXPRESSION   : ID '+' ID ';'
                    | ID '-' ID ';'
                    | ID '*' ID ';'
                    | ID '/' ID ';'
                    | ID DOTADD ID ';'
                    | ID DOTSUB ID ';'
                    | ID DOTMUL ID ';'
                    | ID DOTDIV ID ';'"""


def p_mixed_rel(p):
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


def p_mixed_assign(p):
    """EXPRESSION   : ID '=' EXPRESSION ';'
                    | ID '=' EXPRESSION
                    | ID '=' INT ';'
                    | EXPRESSION '=' INT ';'
                    | ID ADDASSIGN EXPRESSION ';'
                    | ID SUBASSIGN EXPRESSION ';'
                    | ID MULASSIGN EXPRESSION ';'
                    | ID DIVASSIGN EXPRESSION ';'"""


def p_expression_assign(p):
    """EXPRESSION   : EXPRESSION '=' EXPRESSION ';'
                    | EXPRESSION ADDASSIGN EXPRESSION ';'
                    | EXPRESSION SUBASSIGN EXPRESSION ';'
                    | EXPRESSION MULASSIGN EXPRESSION ';'
                    | EXPRESSION DIVASSIGN EXPRESSION ';'"""


def p_id_assign(p):
    """EXPRESSION   : ID '=' ID ';'
                    | ID ADDASSIGN ID ';'
                    | ID SUBASSIGN ID ';'
                    | ID MULASSIGN ID ';'
                    | ID DIVASSIGN ID ';'"""


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
# UNCHARTED TERRITORIES BORDER

if __name__ == '__main__':
    filename = "example1.m"

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
