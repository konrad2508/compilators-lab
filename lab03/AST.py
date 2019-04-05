class Node(object):
    pass


# IF-ELSE DONE
# FOR DONE
# WHILE DONE
# BREAK, CONTINUE done
# EYE, ZEROS, ONES, PRINT, RETURN DONE
# DOTADD etc DONE
# ADDASSIGN etc DONE
# LTE GTE etc DONE
# ID DONE
# FLOAT DONE
# INT DONE
# STRING DONE
# TRANSPOSE ???


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class StringNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Condition(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class BinExp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Function(Node):
    def __init__(self, fun, args):
        self.fun = fun
        self.args = args


class Flow(Node):
    def __init__(self, op):
        self.op = op


class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class For(Node):
    def __init__(self, range, instruction):
        self.range = range
        self.instruction = instruction


class IfElse(Node):
    def __init__(self, condition, if_instruction, else_instruction):
        self.condition = condition
        self.if_instruction = if_instruction
        self.else_instruction = else_instruction


class Error(Node):
    def __init__(self):
        pass
