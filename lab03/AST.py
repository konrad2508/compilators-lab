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
# ARRAY DONE
# MATRIX DONE
# PRINT DONE
# TRANSPOSE ???

class Start(Node):
    def __init__(self, rest):
        self.rest = rest


class Operations(Node):
    def __init__(self, operations):
        self.operations = operations

    def __add__(self, other):
        print('add : ' + str(len(self.operations)))
        self.operations.extend(other.operations)
        print('after : ' + str(len(self.operations)))


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


class ArrayAssign(Node):
    def __init__(self, left, array, op, right):
        self.left = left
        self.array = array
        self.op = op
        self.right = right


class BinExp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UniExp(Node):
    def __init__(self, op, value):
        self.op = op
        self.value = value


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


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class For(Node):
    def __init__(self, var, range, instruction):
        self.var = var
        self.range = range
        self.instruction = instruction


class IfElse(Node):
    def __init__(self, condition, then, else_then):
        self.condition = condition
        self.then = then
        self.else_then = else_then


class Index(Node):
    def __init__(self, index_list):
        self.index_list = index_list

    def __add__(self, other):
        print('add : ' + str(len(self.index_list)))
        self.index_list.extend(other.index_list)
        print('after : ' + str(len(self.index_list)))


class Reference(Node):
    def __init__(self, var, ind):
        self.var = var
        self.ind = ind


class IndexChain(Node):
    def __init__(self, values):
        self.values = values


class ValueChain(Node):
    def __init__(self, value_list):
        self.value_list = value_list

    def __add__(self, other):
        print('add : ' + str(len(self.value_list)))
        self.value_list.extend(other.value_list)
        print('after : ' + str(len(self.value_list)))


class MatrixChain(Node):
    def __init__(self, value):
        self.value = value


class Matrix(Node):
    def __init__(self, array_list):
        self.array_list = array_list

    def __add__(self, other):
        print('add : ' + str(len(self.array_list)))
        self.array_list.extend(other.array_list)
        print('after : ' + str(len(self.array_list)))


class Error(Node):
    def __init__(self):
        pass
