import os
import sys

import ply.yacc as yacc

import AST
import scanner

tokens = scanner.tokens

precedence = (
    ("nonassoc", "IFX"),
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
    # p[0] = AST.Start()


def p_operation_chain(p):
    """operation_chain  : operation operation_chain
                        | """
    # if len(p) == 3:
    #     p[1].operation_list.append(p[2])
    #     p[0] = p[1]
    # else:
    #     p[0] = AST.OperationChain()


def p_operation(p):
    """operation    : '{' operation_chain '}'
                    | simple_operation"""
    # if len(p) == 2:
    #     p[0] = AST.Operation(p[1])
    # else:
    #     p[0] = AST.Operation(p[2])


def p_simple_operation(p):
    """simple_operation : assignment
                        | matrix_assignment
                        | basic_function
                        | if_else
                        | for
                        | while"""
    # p[0] = AST.SimpleOp(p[1])


def p_assignment_operator(p):
    """assignment_operator  : '='
                            | ADDASSIGN
                            | SUBASSIGN
                            | MULASSIGN
                            | DIVASSIGN"""
    # p[0] = p[1]


def p_assignment(p):
    """assignment   : ID assignment_operator matrix_function '(' INT ')' ';'
                    | ID assignment_operator expression ';'
                    | ID index_chain assignment_operator expression ';'"""


def p_index_chain(p):
    """index_chain  : '[' index ']'"""


def p_index(p):
    """index    : INT ',' index
                | """


def p_matrix_function(p):
    """matrix_function  : ZEROS
                        | EYE
                        | ONES"""


def p_matrix_assignment(p):
    """matrix_assignment    : ID '=' '[' custom_matrix ']' ';'"""


def p_custom_matrix(p):
    """custom_matrix    : value_chain ';' custom_matrix
                        | """


def p_basic_function(p):
    """basic_function   : BREAK ';'
                        | CONTINUE ';'
                        | RETURN value ';'
                        | PRINT value_chain ';'
                        | PRINT value ';'"""


def p_value_chain(p):
    """value_chain  : value ',' value_chain
                    | """


# TODO do something about the index chain (and ID?)
def p_value(p):
    """value    : STRING
                | INT
                | FLOAT
                | ID
                | ID index_chain"""
    # try:
    #     int(p[1])
    #     p[0] = AST.Int(p[1])
    # except ValueError:
    #     try:
    #         float(p[1])
    #         p[0] = AST.Float(p[1])
    #     except ValueError:
    #         if " " in p:
    #             p[0] = AST.String(p[1])
    #         else:
    #             p[0] = AST.Id(p[1])


def p_if_else(p):
    """if_else  : IF '(' condition ')' operation ELSE operation
                | IF '(' condition ')' operation %prec IFX"""


def p_condition(p):
    """condition    : expression relational expression"""
    # p[0] = AST.Condition(p[1], p[2], p[3])


def p_relational(p):
    """relational   : '>'
                    | '<'
                    | GTE
                    | LTE
                    | NEQ
                    | EQ """
    # p[0] = p[1]


def p_while(p):
    """while    : WHILE '(' condition ')' operation"""
    # p[0] = AST.WhileInstruction(p[3], p[5])


# TODO export ID = range to assignments
def p_for(p):
    """for  : FOR ID '=' range operation"""
    # p[0] = AST.ForInstruction(p[2], p[3])


def p_range(p):
    """range    : ID ':' INT
                | INT ':' ID
                | ID ':' ID
                | INT ':' INT"""
    # p[0] = AST.Range(p[1], p[3])


def p_expression(p):
    """expression   : '(' expression ')'
                    | '-' expression
                    | expression TRANSPOSE
                    | bin_expr
                    | value"""


def p_bin_expr(p):
    """bin_expr : expression bin_op value"""
    # p[0] = AST.BinExpr(p[1], p[2], p[3])


def p_bin_op(p):
    """bin_op   : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""
    # p[0] = p[1]


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
