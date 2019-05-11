import sys

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
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '.+':
            raise Exception('Not implemented!')
        elif node.op == '.-':
            raise Exception('Not implemented!')
        elif node.op == '.*':
            raise Exception('Not implemented!')
        elif node.op == './':
            raise Exception('Not implemented!')

        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assign)
    def visit(self, node):
        if node.op == '=':
            left = node.left.name
            right = self.visit(node.right)
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
                print(arg)

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

    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
