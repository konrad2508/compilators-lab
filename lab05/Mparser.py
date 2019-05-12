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
    ('nonassoc', 'TRANSPOSE'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


# Program start

def p_start(p):
    """start    : operation_chain"""
    p[0] = AST.Start(p[1], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Recursive operations

def p_operation_chain(p):
    """operation_chain  : operation operation_chain
                        | """
    if len(p) > 1:
        to_add = [p[1]]
        if p[2] is not None:
            to_add += p[2].operations
        p[0] = AST.Operations(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Operation block or operation

def p_operation(p):
    """operation    : '{' operation_chain '}'
                    | simple_operation"""
    if len(p) > 2:
        p[0] = AST.ScopedOperations([p[2]], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = p[1]


def p_simple_operation(p):
    """simple_operation : assignment
                        | basic_function
                        | if_else
                        | for
                        | while"""
    p[0] = AST.Operations([p[1]], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Assignment operators

def p_assignment_operator(p):
    """assignment_operator  : '='
                            | ADDASSIGN
                            | SUBASSIGN
                            | MULASSIGN
                            | DIVASSIGN"""
    p[0] = p[1]


# All types of assignments

def p_assignment(p):
    """assignment   : element assignment_operator matrix_fun ';'
                    | element assignment_operator expression ';'
                    | element assignment_operator vector
                    | element assignment_operator matrix
                    | element assignment_operator ID index_chain"""
    p[0] = AST.Assign(p[1], p[2], p[3], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Either a variable or an element from a vector/matrix

def p_element(p):
    """element  : ID index_chain
                | ID"""

    left = AST.Variable(p[1])
    if len(p) > 2:
        p[0] = AST.Reference(left, p[2], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = left


# Matrix functions like ZEROS, ...

def p_matrix_fun(p):
    """matrix_fun   : matrix_function '(' value_chain ')'"""
    p[0] = AST.Function(p[1], p[3], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Matrix function type

def p_matrix_function(p):
    """matrix_function  : ZEROS
                        | EYE
                        | ONES"""
    p[0] = p[1]


# Index of the vector/matrix

def p_index_chain(p):
    """index_chain  : '[' index ']'"""
    p[0] = AST.IndexChain(p[2], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Index as a list of integers

def p_index(p):
    """index    : INT ',' index
                | INT"""
    if len(p) > 2:
        to_add = [p[1]]
        if p[3] is not None:
            to_add += p[3].index_list
        p[0] = AST.Index(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    elif len(p) == 2:
        to_add = [p[1]]
        p[0] = AST.Index(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Vector and matrix

def p_vector(p):
    """vector    : '[' object_chain ']'"""
    p[0] = AST.Vector(p[2], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Vector as a 1D list of objects

def p_object_chain(p):
    """object_chain     : object ',' object_chain
                        | object"""
    to_add = [p[1]]
    if len(p) > 2:
        if p[3] is not None:
            to_add += p[3].array_list
        p[0] = AST.VectorValues(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    elif len(p) == 2:
        p[0] = AST.VectorValues(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Matrix as a multidimensional list of objects (at least 2D)

def p_custom_matrix(p):
    """matrix   : '[' object_chain object_chains ']'"""

    to_add = [p[2]]
    if p[3] is not None:
        to_add += p[3].array_list
    mat = AST.MatrixRows(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    p[0] = AST.Matrix(mat, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


def p_object_chains(p):
    """object_chains    : ';' object_chain object_chains
                        | ';' object_chain"""
    to_add = [p[2]]
    if len(p) > 3:
        if p[3] is not None:
            to_add += p[3].array_list
    p[0] = AST.MatrixRows(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Possible objects

def p_object(p):
    """object   : value
                | vector
                | matrix"""
    p[0] = p[1]


# Flow control functions

def p_basic_function(p):
    """basic_function   : BREAK ';'
                        | CONTINUE ';'
                        | RETURN expression ';'
                        | PRINT value_chain ';'"""
    if p[2] == ';':
        p[0] = AST.Function(p[1], None, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = AST.Function(p[1], p[2], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# List of print variables

def p_value_chain(p):
    """value_chain  : value ',' value_chain
                    | value"""
    if len(p) > 2:
        to_add = [p[1]]
        if p[3] is not None:
            to_add += p[3].value_list
        p[0] = AST.ValueChain(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    elif len(p) == 2:
        to_add = [p[1]]
        p[0] = AST.ValueChain(to_add, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Simple values

def p_value(p):
    """value    : STRING
                | INT
                | FLOAT
                | element"""
    if isinstance(p[1], int):
        p[0] = AST.IntNum(p[1], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    elif isinstance(p[1], float):
        p[0] = AST.FloatNum(p[1], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    elif isinstance(p[1], str):
        p[0] = AST.StringNum(p[1], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = p[1]


# If else flow

def p_if_else(p):
    """if_else  : IF '(' condition ')' operation ELSE operation
                | IF '(' condition ')' operation %prec IFX"""
    if len(p) > 6:
        p[0] = AST.IfElse(p[3], p[5], p[7], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = AST.IfElse(p[3], p[5], None, line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Condition operation

def p_condition(p):
    """condition    : expression relational expression"""
    p[0] = AST.Condition(p[1], p[2], p[3], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Relational operators

def p_relational(p):
    """relational   : '>'
                    | '<'
                    | GTE
                    | LTE
                    | NEQ
                    | EQ """
    p[0] = p[1]


# Loops

def p_while(p):
    """while    : WHILE '(' condition ')' operation"""
    p[0] = AST.While(p[3], p[5], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


def p_for(p):
    """for  : FOR ID '=' range operation"""
    p[0] = AST.For(p[2], p[4], p[5], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# For loop range

def p_range(p):
    """range    : ID ':' INT
                | INT ':' ID
                | ID ':' ID
                | INT ':' INT"""
    p[0] = AST.Range(p[1], p[3], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Types of operations

def p_expression(p):
    """expression   : '(' expression ')'
                    | bin_expr
                    | un_expr
                    | object"""
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_un_expr(p):
    """un_expr  : '-' expression
                | expression TRANSPOSE"""
    if p[1] == '-':
        p[0] = AST.UniExp(p[1], p[2], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))
    else:
        p[0] = AST.UniExp(p[2], p[1], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


def p_bin_expr(p):
    """bin_expr : expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression
                | expression DOTADD expression
                | expression DOTSUB expression
                | expression DOTMUL expression
                | expression DOTDIV expression"""
    p[0] = AST.BinExp(p[1], p[2], p[3], line=scanner.find_tok_line(p), column=scanner.find_tok_column(p))


# Binary operators

# def p_bin_op(p):
#     """bin_op   : '+'
#                 | '-'
#                 | '*'
#                 | '/'
#                 | DOTADD
#                 | DOTSUB
#                 | DOTMUL
#                 | DOTDIV"""
#     p[0] = p[1]
