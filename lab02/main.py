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
    """operation    : operation operation
                    | simple_operation"""


def p_simple_operation(p):
    """simple_operation : assignment
                        | matrix_assignment
                        | spec_function
                        | if_flow
                        | for_flow
                        | while_flow"""


def p_assignment_op(p):
    """assignment_op    : '='
                        | ADDASSIGN
                        | SUBASSIGN
                        | MULASSIGN
                        | DIVASSIGN"""


def p_assignment(p):
    """assignment   : ID assignment_op assignment_expression
                    | ID element assignment_op expression"""


def p_element(p):
    """element  : '[' index ']'"""


def p_index(p):
    """index    : INT
                | INT ',' index"""


def p_assignment_expression(p):
    """assignment_expression    : matrix_func '(' INT ')' ';'
                                | expression"""


def p_matrix_func(p):
    """matrix_func  : ZEROS
                    | EYE
                    | ONES"""


def p_simple_val(p):
    """simple_val   : INT
                    | FLOAT"""


def p_matrix_assignment(p):
    """matrix_assignment    : ID '=' '[' custom_matrix ']' ';'"""


def p_custom_matrix(p):
    """custom_matrix    : matrix_row
                        | matrix_row additional_matrix_row"""


def p_additional_matrix_row(p):
    """additional_matrix_row    : additional_matrix_row additional_matrix_row
                                | ';' matrix_row"""


def p_matrix_row(p):
    """matrix_row   : simple_val
                    | simple_val additional_simple_val"""


def p_additional_simple_val(p):
    """additional_simple_val    : additional_simple_val additional_simple_val
                                | ',' simple_val"""


def p_spec_function(p):
    """spec_function    : BREAK ';'
                        | CONTINUE ';'
                        | RETURN extended_val ';'
                        | PRINT extended_val ';'"""


def p_extended_val(p):
    """extended_val : STRING
                    | val"""


def p_val(p):
    """val  : ID
            | ID element
            | simple_val"""


def p_if_flow(p):
    """if_flow  : IF '(' condition ')' next_op
                | IF '(' condition ')' next_op ELSE next_op"""
                # | IF '(' condition ')' next_op elseif_flow"""

# the fuck is wrong with this nigga
# def p_elseif_flow(p):
#     """elseif_flow  : elseif_flow elseif_flow
#                     | ELSE IF '(' condition ')' next_op"""


def p_condition_val(p):
    """condition    : simple_val '>' simple_val
                    | simple_val '<' simple_val
                    | simple_val GTE simple_val
                    | simple_val LTE simple_val
                    | simple_val NEQ simple_val
                    | simple_val EQ simple_val"""


def p_condition_id(p):
    """condition    : ID '>' simple_val
                    | ID '<' simple_val
                    | ID GTE simple_val
                    | ID LTE simple_val
                    | ID NEQ simple_val
                    | ID EQ simple_val"""



def p_next_op(p):
    """next_op  : simple_operation
                | '{' operation '}'"""


def p_while_flow(p):
    """while_flow   : WHILE '(' condition ')' next_op"""


def p_for_flow(p):
    """for_flow : FOR ID '=' range next_op"""


def p_range(p):
    """range    : INT ':' INT
                | INT ':' ID
                | ID ':' ID"""


def p_bin_op(p):
    """bin_op   : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""


def p_un_op(p):
    """un_op    : '-'"""


def p_expression(p):
    """expression   : simple_expression ';'"""


def p_simple_expression(p):
    """simple_expression    : simple_expression bin_op simple_expression
                            | un_op simple_expression
                            | simple_expression TRANSPOSE
                            | '(' simple_expression ')'
                            | val"""


# UNCHARTED TERRITORIES BORDER
# def p_expression_binop(p):
#     """EXPRESSION   : EXPRESSION '+' EXPRESSION ';'
#                     | EXPRESSION '-' EXPRESSION ';'
#                     | EXPRESSION '*' EXPRESSION ';'
#                     | EXPRESSION '/' EXPRESSION ';'"""
#
#
# def p_mixed_binop(p):
#     """EXPRESSION   : ID '+' EXPRESSION ';'
#                     | ID '-' EXPRESSION ';'
#                     | ID '*' EXPRESSION ';'
#                     | ID '/' EXPRESSION ';'"""
#
#
# def p_id_binop(p):
#     """EXPRESSION   : ID '+' ID ';'
#                     | ID '-' ID ';'
#                     | ID '*' ID ';'
#                     | ID '/' ID ';'
#                     | ID DOTADD ID ';'
#                     | ID DOTSUB ID ';'
#                     | ID DOTMUL ID ';'
#                     | ID DOTDIV ID ';'"""
#
#
# def p_mixed_rel(p):
#     """EXPRESSION   : ID '<' EXPRESSION
#                     | ID '>' EXPRESSION
#                     | ID GTE EXPRESSION
#                     | ID LTE EXPRESSION
#                     | ID NEQ EXPRESSION
#                     | ID EQ EXPRESSION"""
#
#
# def p_unary_negation(p):
#     """EXPRESSION   : '-' ID"""
#
#
# def p_matrix_transposition(p):
#     """EXPRESSION   : ID TRANSPOSE"""
#
#
# def p_matrix_init(p):
#     """EXPRESSION   : '[' EXPRESSION ']'"""
#
#
# def p_matrix_fun(p):
#     """EXPRESSION   : EYE '(' EXPRESSION ')'
#                     | ZEROS '(' EXPRESSION ')'
#                     | ONES '(' EXPRESSION ')'"""
#
#
# def p_mixed_assign(p):
#     """EXPRESSION   : ID '=' EXPRESSION ';'
#                     | ID '=' EXPRESSION
#                     | ID '=' INT ';'
#                     | EXPRESSION '=' INT ';'
#                     | ID ADDASSIGN EXPRESSION ';'
#                     | ID SUBASSIGN EXPRESSION ';'
#                     | ID MULASSIGN EXPRESSION ';'
#                     | ID DIVASSIGN EXPRESSION ';'"""
#
#
# def p_expression_assign(p):
#     """EXPRESSION   : EXPRESSION '=' EXPRESSION ';'
#                     | EXPRESSION ADDASSIGN EXPRESSION ';'
#                     | EXPRESSION SUBASSIGN EXPRESSION ';'
#                     | EXPRESSION MULASSIGN EXPRESSION ';'
#                     | EXPRESSION DIVASSIGN EXPRESSION ';'"""
#
#
# def p_id_assign(p):
#     """EXPRESSION   : ID '=' ID ';'
#                     | ID ADDASSIGN ID ';'
#                     | ID SUBASSIGN ID ';'
#                     | ID MULASSIGN ID ';'
#                     | ID DIVASSIGN ID ';'"""
#
#
# def p_conditional(p):
#     """EXPRESSION   : IF '(' EXPRESSION ')' EXPRESSION
#                     | ELSE EXPRESSION"""
#
#
# def p_loop_bound(p):
#     """EXPRESSION   : INT ':' ID
#                     | ID ':' ID"""
#
#
# def p_loop(p):
#     """EXPRESSION   : FOR EXPRESSION
#                     | WHILE '(' EXPRESSION ')' EXPRESSION"""
#
#
# def p_flow_control(p):
#     """EXPRESSION   : BREAK ';'
#                     | CONTINUE ';'
#                     | RETURN INT ';'
#                     | RETURN EXPRESSION ';'"""
#
#
# def p_print(p):
#     """EXPRESSION   : PRINT STRING ';'
#                     | PRINT ID ';'
#                     | PRINT ID EXPRESSION ';'"""
#
#
# def p_complex_expression(p):
#     """EXPRESSION   : EXPRESSION EXPRESSION
#                     | '{' EXPRESSION '}'
#                     | '{' EXPRESSION EXPRESSION '}'"""
#
#
# def p_id_list(p):
#     """EXPRESSION   : ',' ID
#                     | ',' ID EXPRESSION"""
#
#
# def p_number_list(p):
#     """EXPRESSION   : INT ',' EXPRESSION
#                     | INT ';'"""
#
#
# def p_array(p):
#     """EXPRESSION   : ID '[' EXPRESSION ']'"""
# UNCHARTED TERRITORIES BORDER

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
