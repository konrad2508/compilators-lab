from __future__ import print_function

import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def printValue(value, indent=0):
    if isinstance(value, AST.Node):
        value.printTree(indent)
    else:
        try:
            print(indent * sugar + value)
        except TypeError:
            print(indent * sugar + str(value))


sugar = '|' + 2 * ' '


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Start)
    def printTree(self, indent=0):
        printValue(self.rest)

    @addToClass(AST.Operations)
    def printTree(self, indent=0):
        for i in range(len(self.operations)):
            printValue(self.operations[i], indent)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        printValue(self.op, indent)
        printValue(self.left, indent + 1)
        printValue(self.right, indent + 1)

    @addToClass(AST.ArrayAssign)
    def printTree(self, indent=0):
        printValue(self.op, indent)
        printValue(self.left, indent + 1)
        printValue(self.array, indent + 1)
        printValue(self.right, indent + 1)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        printValue('REF', indent)
        printValue(self.var, indent + 1)
        printValue(self.ind, indent + 1)

    # TODO indentation
    @addToClass(AST.IndexChain)
    def printTree(self, indent=0):
        printValue(self.values, indent)

    @addToClass(AST.Index)
    def printTree(self, indent=0):
        for i in range(len(self.index_list)):
            printValue(self.index_list[i], indent)

    @addToClass(AST.ValueChain)
    def printTree(self, indent=0):
        for i in range(len(self.index_list)):
            printValue(self.index_list[i], indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        printValue('VECTOR', indent)
        printValue(self.value, indent + 1)

    @addToClass(AST.VectorValues)
    def printTree(self, indent=0):
        for i in range(len(self.array_list)):
            printValue(self.array_list[i], indent)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        printValue('MATRIX', indent)
        printValue(self.value, indent + 1)

    @addToClass(AST.MatrixRows)
    def printTree(self, indent=0):
        for i in range(len(self.array_list)):
            printValue('ROW', indent)
            printValue(self.array_list[i], indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        printValue(self.fun, indent)
        printValue(self.args, indent + 1)

    @addToClass(AST.BinExp)
    def printTree(self, indent=0):
        printValue(self.op, indent)
        printValue(self.left, indent + 1)
        printValue(self.right, indent + 1)

    @addToClass(AST.UniExp)
    def printTree(self, indent=0):
        if self.op == "'":
            printValue('TRANSPOSE', indent)
        else:
            printValue('NEG', indent)
        printValue(self.value, indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        printValue('FOR', indent)
        printValue(self.var, indent + 1)
        printValue(self.range, indent + 1)
        printValue(self.instruction, indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        printValue(self.op, indent)
        printValue(self.left, indent + 1)
        printValue(self.right, indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        printValue('IF', indent)
        printValue(self.condition, indent + 1)
        printValue('THEN', indent)
        printValue(self.then, indent + 1)
        if self.else_then is not None:
            printValue('ELSE', indent)
            printValue(self.else_then, indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        printValue('WHILE', indent)
        printValue(self.condition, indent + 1)
        printValue(self.instruction, indent + 1)

    @addToClass(AST.ValueChain)
    def printTree(self, indent=0):
        for i in range(len(self.value_list)):
            printValue(self.value_list[i], indent)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        printValue('RANGE', indent)
        printValue(self.start, indent + 1)
        printValue(self.end, indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        printValue(self.value, indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        printValue(self.value, indent)

    @addToClass(AST.StringNum)
    def printTree(self, indent=0):
        printValue(self.value, indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        printValue(self.name, indent)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        printValue('ERROR')
