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
            print((indent + 1) * sugar + self.left)
        try:
            self.right.printTree(indent + 1)
        except AttributeError:
            print((indent + 1) * sugar + self.right)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print(indent * sugar + self.fun)
        print((indent + 1) * sugar + str(self.args))

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(self.value)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print('ERROR')

    # define printTree for other classes
    # ...
