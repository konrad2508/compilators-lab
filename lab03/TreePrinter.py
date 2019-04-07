from __future__ import print_function

import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


sugar = '|' + 2 * ' '


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Start)
    def printTree(self, indent=0):
        self.rest.printTree()

    @addToClass(AST.Operations)
    def printTree(self, indent=0):
        for i in range(len(self.operations)):
            self.operations[i].printTree(indent)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print(indent * sugar + self.op)
        try:
            self.left.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.left))
        try:
            self.right.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.right))

    @addToClass(AST.ArrayAssign)
    def printTree(self, indent=0):
        print(indent * sugar + self.op)
        try:
            self.left.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.left))
        try:
            self.array.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.array))
        try:
            self.right.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.right))

    @addToClass(AST.IndexChain)
    def printTree(self, indent=0):
        self.index_list.printTree()

    @addToClass(AST.ValueChain)
    def printTree(self, indent=0):
        for i in range(len(self.index_list)):
            try:
                self.args.printTree(indent)
            except AttributeError:
                print((indent) * sugar + str(self.index_list[i]))

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print(indent * sugar + self.fun)
        if self.args is not None:
            try:
                self.args.printTree(indent + 1)
            except AttributeError:
                print((indent + 1) * sugar + str(self.args))


    @addToClass(AST.BinExp)
    def printTree(self, indent=0):
        print(indent * sugar + self.op)
        try:
            self.left.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.left))
        try:
            self.right.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.right))

    @addToClass(AST.UniExp)
    def printTree(self, indent=0):
        print(indent * sugar + self.op)
        try:
            self.value.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.value))

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(indent * sugar + 'FOR')
        try:
            self.var.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.var))

        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ValueChain)
    def printTree(self, indent=0):
        for i in range(len(self.value_list)):
            try:
                self.args.printTree(indent)
            except AttributeError:
                print((indent) * sugar + str(self.value_list[i]))

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(indent * sugar + 'RANGE')
        try:
            self.start.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.start))
        try:
            self.end.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + str(self.end))

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(str(self.value))

    @addToClass(AST.StringNum)
    def printTree(self, indent=0):
        print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(self.value)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print('ERROR')
