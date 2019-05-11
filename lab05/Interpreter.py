import sys
import numpy
import itertools

import AST
import SymbolTable

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
        if node.fun == 'print':
            for arg in self.visit(node.args):
                print(arg, end=' ')
            print()

    @when(AST.ValueChain)
    def visit(self, node):
        return [self.visit(arg) for arg in node.value_list]

    @when(AST.IntNum)
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
            self.memory.push(Memory('IfElseScope'))
            self.visit(node.instruction)
            self.memory.pop()


    # @when(AST.While)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r
