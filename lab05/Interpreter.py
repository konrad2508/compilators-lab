import sys

import AST
from utils import recursive_map
from Memory import *
from Exceptions import *
from visit import *

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        raise Exception('Not implemented Interpreter.visit for %s' % node.__class__.__name__)

    @when(AST.Start)
    def visit(self, node):
        self.visit(node.rest)

    @when(AST.Operations)
    def visit(self, node):
        for operation in node.operations:
            self.visit(operation)

    @when(AST.ScopedOperations)
    def visit(self, node):
        self.memory.push(Memory('Scope'))

        for operation in node.operations:
            self.visit(operation)

        self.memory.pop()

    @when(AST.BinExp)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        # classical operations
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right

        # element-wise operations
        elif node.op == '.+':
            if isinstance(right, int):
                return recursive_map(lambda x: x + right, left)
            else:
                dotted = []
                for (left_x, right_x) in zip(left, right):
                    to_add = []
                    try:
                        for (left_y, right_y) in zip(left_x, right_x):
                            to_add.append(left_y + right_y)
                        dotted.append(to_add)
                    except TypeError:
                        for (left_y, right_y) in zip([left_x], [right_x]):
                            to_add.append(left_y + right_y)
                        dotted.append(to_add if len(to_add) > 1 else to_add[0])
                return dotted
        elif node.op == '.-':
            if isinstance(right, int):
                return recursive_map(lambda x: x - right, left)
            else:
                dotted = []
                for (left_x, right_x) in zip(left, right):
                    to_add = []
                    try:
                        for (left_y, right_y) in zip(left_x, right_x):
                            to_add.append(left_y - right_y)
                        dotted.append(to_add)
                    except TypeError:
                        for (left_y, right_y) in zip([left_x], [right_x]):
                            to_add.append(left_y - right_y)
                        dotted.append(to_add if len(to_add) > 1 else to_add[0])
                return dotted
        elif node.op == '.*':
            if isinstance(right, int):
                return recursive_map(lambda x: x * right, left)
            else:
                dotted = []
                for (left_x, right_x) in zip(left, right):
                    to_add = []
                    try:
                        for (left_y, right_y) in zip(left_x, right_x):
                            to_add.append(left_y * right_y)
                        dotted.append(to_add)
                    except TypeError:
                        for (left_y, right_y) in zip([left_x], [right_x]):
                            to_add.append(left_y * right_y)
                        dotted.append(to_add if len(to_add) > 1 else to_add[0])
                return dotted
        elif node.op == './':
            if isinstance(right, int):
                return recursive_map(lambda x: x / right, left)
            else:
                dotted = []
                for (left_x, right_x) in zip(left, right):
                    to_add = []
                    try:
                        for (left_y, right_y) in zip(left_x, right_x):
                            to_add.append(left_y / right_y)
                        dotted.append(to_add)
                    except TypeError:
                        for (left_y, right_y) in zip([left_x], [right_x]):
                            to_add.append(left_y / right_y)
                        dotted.append(to_add if len(to_add) > 1 else to_add[0])
                return dotted

    @when(AST.UniExp)
    def visit(self, node):
        op = node.op
        operand = self.visit(node.value)

        if op == '-':
            if isinstance(operand, list):
                return recursive_map(lambda x: -x, operand)
            else:
                return -operand

        elif op == "'":
            return list(map(list, zip(*operand)))

    @when(AST.Assign)
    def visit(self, node):
        if node.op == '=':
            left = node.left.name
            right = self.visit(node.right)
            if self.memory.get(left) is not None:
                self.memory.set(left, right)
            else:
                self.memory.insert(left, right)
        else:
            left_name = node.left.name
            left_val = self.visit(node.left)
            right = self.visit(node.right)
            if node.op == '+=':
                new_val = left_val + right
            elif node.op == '-=':
                new_val = left_val - right
            elif node.op == '*=':
                new_val = left_val * right
            elif node.op == '/=':
                new_val = left_val / right
            self.memory.set(left_name, new_val)

    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.Function)
    def visit(self, node):
        # normal functions
        if node.fun == 'print':
            for arg in self.visit(node.args):
                print(arg, end=' ')
            print()

        # matrix functions
        elif node.fun == 'zeros':
            args = self.visit(node.args)
            if len(args) == 1:
                dim = args[0]
                to_ret = []
                for _ in range(0, dim):
                    to_add = [0] * dim
                    to_ret.append(to_add)
                return to_ret
            else:
                dim_x = args[0]
                dim_y = args[1]
                to_ret = []
                for _ in range(0, dim_x):
                    to_add = [0] * dim_y
                    to_ret.append(to_add)
                return to_ret

        elif node.fun == 'ones':
            args = self.visit(node.args)
            if len(args) == 1:
                dim = args[0]
                to_ret = []
                for _ in range(0, dim):
                    to_add = [1] * dim
                    to_ret.append(to_add)
                return to_ret
            else:
                dim_x = args[0]
                dim_y = args[1]
                to_ret = []
                for _ in range(0, dim_x):
                    to_add = [1] * dim_y
                    to_ret.append(to_add)
                return to_ret
        elif node.fun == 'eye':
            args = self.visit(node.args)
            if len(args) == 1:
                dim = args[0]
                to_ret = []
                for i in range(0, dim):
                    to_add = [0] * dim
                    to_add[i] = 1
                    to_ret.append(to_add)
                return to_ret
            else:
                dim_x = args[0]
                dim_y = args[1]
                to_ret = []
                for i in range(0, dim_x):
                    to_add = [0] * dim_y
                    if i < dim_y:
                        to_add[i] = 1
                    to_ret.append(to_add)
                return to_ret

        # control flow functions
        elif node.fun == 'break':
            raise BreakException()
        elif node.fun == 'continue':
            raise ContinueException()
        elif node.fun == 'return':
            raise ReturnValueException(self.visit(node.args))

    @when(AST.ValueChain)
    def visit(self, node):
        return [self.visit(arg) for arg in node.value_list]

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.StringNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.Vector)
    def visit(self, node):
        return self.visit(node.value)

    @when(AST.VectorValues)
    def visit(self, node):
        visited_list = list(map(self.visit, node.array_list))
        return visited_list

    @when(AST.Matrix)
    def visit(self, node):
        return self.visit(node.value)

    @when(AST.MatrixRows)
    def visit(self, node):
        return list(map(self.visit, node.array_list))

    @when(AST.IfElse)
    def visit(self, node):
        if self.visit(node.condition):
            self.memory.push(Memory('IfThenScope'))
            self.visit(node.then)
            self.memory.pop()
        elif node.else_then is not None:
            self.memory.push(Memory('IfElseScope'))
            self.visit(node.else_then)
            self.memory.pop()

    @when(AST.Condition)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == '>':
            return left > right
        elif node.op == '>=':
            return left >= right
        elif node.op == '<':
            return left < right
        elif node.op == '<=':
            return left <= right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right

    @when(AST.While)
    def visit(self, node):
        while self.visit(node.condition):
            try:
                self.memory.push(Memory('WhileScope'))
                self.visit(node.instruction)
                self.memory.pop()
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.For)
    def visit(self, node):
        self.memory.push(Memory('ForScope'))
        r = self.visit(node.range)
        self.memory.insert(node.var, -1)

        if r[0] > r[1]:
            step = -1
        else:
            step = 1

        for i in range(r[0], r[1], step):
            try:
                self.memory.set(node.var, i)
                self.visit(node.instruction)
            except BreakException:
                break
            except ContinueException:
                pass

        self.memory.pop()

    @when(AST.Range)
    def visit(self, node):
        if isinstance(node.start, int):
            start = node.start
        else:
            start = self.memory.get(node.start)

        if isinstance(node.end, int):
            end = node.end
        else:
            end = self.memory.get(node.end)

        return start, end

    @when(AST.Reference)
    def visit(self, node):
        v = self.visit(node.var)
        for i in self.visit(node.ind):
            v = v[i]
        return v

    @when(AST.IndexChain)
    def visit(self, node):
        return self.visit(node.values)

    @when(AST.Index)
    def visit(self, node):
        for i in node.index_list:
            yield i
