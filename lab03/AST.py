class Node(object):
    def __str__(self):
        return self.printTree()


class Empty(Node):
    def __init__(self):
        pass


class Start(Node):
    def __init__(self):
        pass

class OperationChain(Node):
    def __init__(self):
        self.operation_list = []

    def append_value(self, op):
        self.operation_list.append(op)


class Operation(Node):
    def __init__(self, operation):
        self.operation = operation

class SimpleOp(Node):
    def __init__(self, operation):
        self.operation = operation


class AssignOp(Node):
    def __init__(self, value):
        self.value = value


# assignments
class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class IndexChain(Node):
    def __init__(self, value):
        self.value = value


class Index(Node):
    def __init__(self, value):
        self.value = value


# print, return and matrix functions
class Function(Node):
    pass


class MatrixFunction(Function):
    def __init__(self, instr, arg):
        self.instr = instr
        self.arg = arg


# class MatrixAssign

class SystemFunction(Function):
    def __init__(self, instr, arg):
        self.instr = instr
        self.arg = arg


# break, continue
class FlowControl(Node):
    def __init__(self, instr):
        self.instr = instr


class ValueChain(Node):
    def __init__(self):
        self.value_list = []

    def append_value(self, value):
        self.value_list.append(value)


# Constants
class Value(Node):
    def __init__(self, value):
        self.value = value


class Int(Value):
    def __init__(self, value):
        self.value = value


class Float(Value):
    def __init__(self, value):
        self.value = value


class String(Value):
    def __init__(self, value):
        self.value = value


class Id(Value):
    def __init__(self, name):
        self.name = name


# instructions
class Instruction(Node):
    pass


class IfInstruction(Instruction):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class ElseInstruction(Instruction):
    def __init__(self, instr):
        self.instr = instr


class Condition(Instruction):
    def __init__(self, left, instr, right):
        self.left = left
        self.instr = instr
        self.right = right


class Relational(Value):
    def __init__(self, value):
        self.value = value


class WhileInstruction(Instruction):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class ForInstruction(Instruction):
    def __init__(self, assignment, instr):
        self.assignment = assignment
        self.instr = instr


class Range(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


# Expressions
class Expression(Node):
    def __init__(self):
        pass


class ParenExpr(Expression):
    def __init__(self, expr):
        self.expression = expr


class BinExpr(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class BinOp(Value):
    def __init__(self, value):
        self.value = value
