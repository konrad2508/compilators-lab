from __future__ import print_function

import AST

indent_char = '| '


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.value
        return res + "\n"

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.value
        return res + "\n"

    @addToClass(AST.String)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.value
        return res + "\n"

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.name
        return res + "\n"

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        res = indent * indent_char + "=\n"
        res += indent_char * (indent + 1) + self.var + "\n"
        res += self.expr.printTree(indent + 1) if isinstance(self.expr, (AST.Expression, AST.Const)) \
            else indent_char * (indent + 1) + self.expr
        return res

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body
