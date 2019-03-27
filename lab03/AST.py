class Node(object):
    pass


# values
class Values(Node):
    pass


class IntNum(Values):
    def __init__(self, value):
        self.value = value


class FloatNum(Values):
    def __init__(self, value):
        self.value = value


class String(Values):
    def __init__(self, value):
        self.value = value


class Id(Values):
    def __init__(self, name):
        self.name = name


# operators
class Operator(Node):
    pass


class BinOperator(Operator):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class RelOperator(Operator):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


# assignments
class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


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

class ForInstruction(Instruction):
    def __init__(self, assignment, instr):
        self.assignment = assignment
        self.instr = instr

class WhileInstruction(Instruction):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr

# break, continue
class FlowControl(Node):
    def __init__(self, instr):
        self.instr = instr


# print, return and matrix functions
class Function(Node):
    pass

class SystemFunction(Function):
    def __init__(self, instr, arg):
        self.instr = instr
        self.arg = arg

class MatrixFunction(Function):
    def __init__(self, instr, arg):
        self.instr = instr
        self.arg = arg


# compound instructions
class CompoundInstruction(Node):
    def __init__(self):
        raise Exception("Not implemented")

# array stuff
class ArrayStuff(Node):
    def __init__(self):
        raise Exception("Not implemented")


class Error(Node):
    def __init__(self):
        pass
