import re

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
    ("left", 'DOTMUL', 'DOTDIV'),
    ('nonassoc', 'TRANSPOSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_start(p):
    """start    : operation_chain"""
    p[0] = AST.Start(p[1])


def p_operation_chain(p):
    """operation_chain  : operation operation_chain
                        | """
    if len(p) > 1:
        to_add = [p[1]]
        if p[2] is not None:
            to_add += p[2].operations
        p[0] = AST.Operations(to_add)


def p_operation(p):
    """operation    : '{' operation_chain '}'
                    | simple_operation"""

    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_simple_operation(p):
    """simple_operation : assignment
                        | basic_function
                        | if_else
                        | for
                        | while"""
    p[0] = AST.Operations([p[1]])


def p_assignment_operator(p):
    """assignment_operator  : '='
                            | ADDASSIGN
                            | SUBASSIGN
                            | MULASSIGN
                            | DIVASSIGN"""
    p[0] = p[1]


def p_assignment(p):
    """assignment   : assignment_left assignment_operator matrix_fun ';'
                    | assignment_left assignment_operator expression ';'
                    | assignment_left assignment_operator vector ';'
                    | assignment_left assignment_operator matrix ';'"""
    p[0] = AST.Assign(p[1], p[2], p[3])


def p_assignment_left(p):
    """assignment_left  : ID index_chain
                        | ID"""

    if len(p) > 2:
        p[0] = AST.Reference(p[1], p[2])
    else:
        p[0] = p[1]


def p_matrix_fun(p):
    """matrix_fun   : matrix_function '(' INT ')'"""
    p[0] = AST.Function(p[1], p[3])


def p_index_chain(p):
    """index_chain  : '[' index ']'"""
    p[0] = AST.IndexChain(p[2])


def p_index(p):
    """index    : INT ',' index
                | INT"""
    if len(p) > 2:
        to_add = [p[1]]
        if p[3] is not None:
            to_add += p[3].index_list
        p[0] = AST.Index(to_add)
    elif len(p) == 2:
        to_add = [p[1]]
        p[0] = AST.Index(to_add)


def p_matrix_function(p):
    """matrix_function  : ZEROS
                        | EYE
                        | ONES"""
    p[0] = p[1]


def p_vector(p):
    """vector    : '[' object_chain ']'"""
    p[0] = AST.VectorChain(p[2])


def p_object_chain(p):
    """object_chain     : object ',' object_chain
                        | object"""
    to_add = [p[1]]
    if len(p) > 2:
        if p[3] is not None:
            to_add += p[3].array_list
        p[0] = AST.Vector(to_add)
    elif len(p) == 2:
        p[0] = AST.Vector(to_add)


def p_custom_matrix(p):
    """matrix   : '[' object_chain object_chains ']'"""

    to_add = [p[2]]
    if p[3] is not None:
        to_add += p[3].array_list
    mat = AST.Matrix(to_add)
    p[0] = AST.MatrixChain(mat)


def p_object_chains(p):
    """object_chains    : ';' object_chain object_chains
                        | ';' object_chain"""
    to_add = [p[2]]
    if len(p) > 3:
        if p[3] is not None:
            to_add += p[3].array_list
    p[0] = AST.Matrix(to_add)


# def p_custom_matrix(p):
#     """matrix   : '[' matrix_row_chain ']'"""
#     p[0] = AST.MatrixChain(p[2])
#
#
# def p_matrix_row_chain(p):
#     """matrix_row_chain : object_chain ';' matrix_row_chain
#                         | object_chain"""
#     if len(p) > 2:
#         to_add = [p[1]]
#         if p[3] is not None:
#             to_add += p[3].array_list
#         p[0] = AST.Vector(to_add)
#     elif len(p) == 2:
#         to_add = [p[1]]
#         p[0] = AST.Vector(to_add)

# add matrix
def p_object(p):
    """object   : STRING
                | INT
                | FLOAT
                | assignment_left
                | vector
                | matrix"""
    p[0] = p[1]


def p_basic_function(p):
    """basic_function   : BREAK ';'
                        | CONTINUE ';'
                        | RETURN value ';'
                        | PRINT value_chain ';'"""
    if p[2] == ';':
        p[0] = AST.Function(p[1], None)
    else:
        p[0] = AST.Function(p[1], p[2])


def p_value_chain(p):
    """value_chain  : value ',' value_chain
                    | value"""
    if len(p) > 2:
        to_add = [p[1]]
        if p[3] is not None:
            to_add += p[3].value_list
        p[0] = AST.ValueChain(to_add)
    elif len(p) == 2:
        to_add = [p[1]]
        p[0] = AST.ValueChain(to_add)


def p_value(p):
    """value    : STRING
                | INT
                | FLOAT
                | ID
                | ID index_chain"""
    try:
        int(p[1])
        p[0] = AST.IntNum(p[1])
    except ValueError:
        try:
            float(p[1])
            p[0] = AST.FloatNum(p[1])
        except ValueError:
            pattern = re.compile("^[a-zA-Z]+$")
            if pattern.match(p[1]):
                p[0] = AST.Variable(p[1])
            else:
                p[0] = AST.StringNum(p[1])


def p_if_else(p):
    """if_else  : IF '(' condition ')' operation ELSE operation
                | IF '(' condition ')' operation %prec IFX"""
    if len(p) > 6:
        p[0] = AST.IfElse(p[3], p[5], p[7])
    else:
        p[0] = AST.IfElse(p[3], p[5], None)


def p_condition(p):
    """condition    : expression relational expression"""
    p[0] = AST.Condition(p[1], p[2], p[3])


def p_relational(p):
    """relational   : '>'
                    | '<'
                    | GTE
                    | LTE
                    | NEQ
                    | EQ """
    p[0] = p[1]


def p_while(p):
    """while    : WHILE '(' condition ')' operation"""
    p[0] = AST.While(p[3], p[5])


def p_for(p):
    """for  : FOR ID '=' range operation"""
    p[0] = AST.For(p[2], p[4], p[5])


def p_range(p):
    """range    : ID ':' INT
                | INT ':' ID
                | ID ':' ID
                | INT ':' INT"""
    p[0] = AST.Range(p[1], p[3])


def p_expression(p):
    """expression   : '(' expression ')'
                    | bin_expr
                    | un_expr
                    | value"""
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_un_expr(p):
    """un_expr  : '-' expression
                | expression TRANSPOSE"""
    if p[1] == '-':
        p[0] = AST.UniExp(p[1], p[2])
    else:
        p[0] = AST.UniExp(p[2], p[1])


def p_bin_expr(p):
    """bin_expr : expression bin_op value"""
    p[0] = AST.BinExp(p[1], p[2], p[3])


def p_bin_op(p):
    """bin_op   : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""
    p[0] = p[1]
