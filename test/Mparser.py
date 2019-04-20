#!/usr/bin/python

import scanner
import ply.yacc as yacc

from structures import (Assignment,
                        BinaryOperation,
                        Enumeration,
                        ForLoop,
                        FuncCall,
                        IfCondition,
                        InstructionsList,
                        LogicalOperation,
                        Matrix,
                        MatrixOperation,
                        MatrixRow,
                        IndicesAssignment,
                        PrintInstruction,
                        Range,
                        TransposeOperation,
                        Variable,
                        WhileLoop,
                        Integer,
                        Float,
                        String)

tokens = scanner.tokens

precedence = (
    ("nonassoc",
     'LEQ', 'GEQ', 'EQ', 'NEQ', '<', '>',
     '=', 'ADDASSIGN', 'SUBASSIGN', 'DIVASSIGN', 'MULASSIGN'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'DOTADD', 'DOTDIV', 'DOTMUL', 'DOTSUB'),
    ("left", "'"),
    ("right", 'UMINUS'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(
            p.lineno, scanner.find_column(p), p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """
    program : instructions_opt
    """
    p[0] = p[1]


def p_instructions_opt(p):
    """
    instructions_opt : instructions
                     |
    """
    if len(p) >= 2:
        p[0] = p[1]


def p_instructions(p):
    """
    instructions : instructions instruction
                 | instruction
    """
    if len(p) >= 3:
        p[0] = (p[1] or InstructionsList([])) + \
               InstructionsList(instructions=[p[2]])
    else:
        p[0] = InstructionsList([p[1]])


def p_instruction(p):
    """
    instruction : ID assign expression ';'
                | ID '[' indices_range ']' '=' term ';'
                | for_loop
                | while_loop
                | if_condition
                | simple_instruction ';'
                | print ';'
    """
    if len(p) in {2, 3}:
        p[0] = p[1]
    elif p.slice[2].type == 'assign':
        p[0] = Assignment(id=p[1], assignment=p[2], expression=p[3])
    elif p[2] == '[' and p[4] == ']':
        p[0] = IndicesAssignment(id=p[1], items=p[3], value=p[6])


def p_expression(p):
    """
    expression : binary_expression
               | '(' expression ')'
               | logical_expression
               | matrix_expression
               | expression "'"
               | term
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(' and p[3] == ')':
        p[0] = p[2]
    elif len(p) == 4 and p.slice[2].type == 'logical_expression':
        p[0] = LogicalOperation(operator=p[2], left=p[1], right=p[3])
    elif len(p) == 3:
        p[0] = TransposeOperation(value=p[1])


def p_term(p):
    """
    term  : INT
          | FLOAT
          | ID
          | matrix
          | reserved_func_call
          | range
          | STRING
    range : int_or_id ':' int_or_id
    """
    if p.slice[1].type in {"reserved_func_call", "matrix"}:
        p[0] = p[1]
    elif p.slice[1].type == "STRING":
        p[0] = String(p[1])
    elif p.slice[0].type == 'range':
        p[0] = Range(left=p[1], right=p[3])
    else:
        try:
            if int(p[1]) == float(p[1]):
                p[0] = Integer(p[1])
            else:
                p[0] = Float(p[1])
        except (ValueError, TypeError) as e:
            p[0] = Variable(id=p[1])


def p_matrix(p):
    """
    matrix : '[' matrix_rows ']'
    """
    p[0] = Matrix(p[2])


def p_matrix_rows(p):
    """
    matrix_rows : matrix_row
                | matrix_rows ';' matrix_row
    """
    if len(p) >= 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_matrix_row(p):
    """
    matrix_row : term
               | matrix_row ',' term
    """
    if len(p) >= 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = MatrixRow(items=[p[1]])


def p_func_call(p):
    """
    reserved_func_call : func_name '(' term ')'
    """
    p[0] = FuncCall(name=p[1], params=p[3])


def p_bin_op(p):
    """
    binary_expression    : expression '+' expression
                         | expression '-' expression
                         | expression '/' expression
                         | expression '*' expression
    matrix_expression    : expression DOTADD expression
                         | expression DOTDIV expression
                         | expression DOTMUL expression
                         | expression DOTSUB expression
    logical_expression   : expression '<' expression
                         | expression '>' expression
                         | expression LEQ expression
                         | expression NEQ expression
                         | expression GEQ expression
                         | expression EQ expression
    """
    if p.slice[0].type == 'binary_expression':
        p[0] = BinaryOperation(operator=p[2], left=p[1], right=p[3])
    elif p.slice[0].type == 'matrix_expression':
        p[0] = MatrixOperation(operator=p[2], left=p[1], right=p[3])
    elif p.slice[0].type == 'logical_expression':
        p[0] = LogicalOperation(operator=p[2], left=p[1], right=p[3])


def p_multi_type(p):
    """
    assign             : '='
                       | ADDASSIGN
                       | SUBASSIGN
                       | DIVASSIGN
                       | MULASSIGN
    func_name          : EYE
                       | ONES
                       | ZEROS
    simple_instruction : BREAK
                       | RETURN
                       | CONTINUE
    """
    p[0] = p[1]


def p_print(p):
    """
    print : PRINT csv
    csv   : csv ',' term
          | term
    """
    if p.slice[0].type == 'print':
        p[0] = PrintInstruction(values=p[2])
    elif len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = (*p[1], p[3])


def p_indices_range(p):
    """
    indices_range : int_or_id ',' int_or_id
                  | int_or_id
    int_or_id     : INT
                  | ID
    """
    if len(p) >= 4:
        p[0] = [p[1]] + [p[3]]
    else:
        if p.slice[1].type == "INT":
            p[0] = Integer(p[1])
        else:
            p[0] = Variable(p[1])


def p_expression_uminus(p):
    """
    expression : '-' expression %prec UMINUS
    """
    p[0] = -p[2]


def p_while_loop(p):
    """
    while_loop : WHILE '(' logical_expression ')' '{' instructions_opt '}'
    """
    p[0] = WhileLoop(condition=p[3], instructions=p[6])


def p_for_loop(p):
    """
    for_loop : FOR enumeration '{' instructions_opt '}'
    """
    p[0] = ForLoop(enumeration=p[2], instructions=p[4])


def p_enumeration(p):
    """
    enumeration : ID '=' range
    """
    p[0] = Enumeration(variable=p[1], range=p[3])


def p_if_condition(p):
    """
    if_condition : IF '(' logical_expression ')' instruction else
    else         : ELSE instruction
                 |
    """
    if p.slice[0].type == 'if_condition':
        p[0] = IfCondition(condition=p[3], instruction=p[5], else_branch=p[6])
    elif len(p) == 3:
        p[0] = p[2]


parser = yacc.yacc()