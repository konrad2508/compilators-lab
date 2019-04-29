from collections import defaultdict

import AST
from SymbolTable import SymbolTable

types_table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

types = ['int', 'float', 'string', 'matrix', 'vector']

for op in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    types_table[op]['int']['float'] = 'float'
    types_table[op]['float']['int'] = 'float'
    types_table[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['int']['float'] = 'int'
    types_table[op]['float']['int'] = 'int'
    types_table[op]['float']['float'] = 'int'

for op in ['.+', '.-', '.*', './']:
    types_table[op]['vector']['matrix'] = 'matrix'
    types_table[op]['matrix']['vector'] = 'matrix'
    types_table[op]['matrix']['matrix'] = 'matrix'

for op in ['+', '*']:
    types_table[op]['vector']['vector'] = 'vector'

types_table['+']['string']['string'] = 'string'
types_table['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['string']['string'] = 'int'


class NodeVisitor(object):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.errors = []
        self.loop = None

    def get_errors(self):
        return self.errors

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        raise Exception("visit not defined in class " + node.__class__.__name__)


class TypeChecker(NodeVisitor):
    def visit_Start(self, node):
        self.visit(node.rest)

    def visit_Operations(self, node):
        for operation in node.operations:
            self.visit(operation)

    def visit_Assign(self, node):
        type = self.visit(node.right)

        try:
            if type == 'matrix':
                self.visit(node.right.value)
        except AttributeError:
            pass

        if isinstance(node.left, AST.Variable):
            self.table.put(node.left.name, type)

    def visit_For(self, node):
        previousLoop = self.loop
        self.loop = node
        self.visit(node.instruction)
        self.loop = previousLoop

    def visit_While(self, node):
        previousLoop = self.loop
        self.loop = node
        self.visit(node.instruction)
        self.loop = previousLoop

    def visit_Function(self, node):
        if node.fun in ['break', 'continue']:
            if self.loop is None:
                self.errors.append("Error: Loop instruction outside of a loop")
        elif node.fun in ['eye', 'zeros', 'ones']:
            if isinstance(node.args, AST.ValueChain):
                for value in node.args.value_list:
                    try:
                        self.visit(value)
                        value = self.table.get(value.name)
                        if value != 'int':
                            self.errors.append("Error: Function argument must be an integer")
                    except AttributeError:
                        if not isinstance(value, int) and not isinstance(value, AST.IntNum):
                            self.errors.append("Error: Function argument must be an integer")
            elif not isinstance(node.args, int) and not isinstance(node.args, AST.IntNum):
                self.errors.append("Error: Function argument must be an integer")

            return 'matrix'

    def visit_BinExp(self, node):
        nodeLeft = node.left
        nodeRight = node.right
        op = node.op

        if isinstance(nodeLeft, AST.Variable):
            nodeLeft = self.table.get(node.left.name)
        if isinstance(nodeRight, AST.Variable):
            nodeRight = self.table.get(node.right.name)

        if not nodeLeft in types:
            typeLeft = self.visit(nodeLeft)
        else:
            typeLeft = nodeLeft

        if not nodeRight in types:
            typeRight = self.visit(nodeRight)
        else:
            typeRight = nodeRight

        type = types_table[op][typeLeft][typeRight]

        if type is None:
            self.errors.append("Error: Cannot perform {0} operation between {1} and {2}".format(op, typeLeft, typeRight))
        else:
            if (typeLeft == 'matrix' or typeLeft == 'vector') and (typeRight == 'matrix' or typeRight == 'vector'):
                leftSize = self.visit(nodeLeft.value)
                rightSize = self.visit(nodeRight.value)
                if op == '.+' or op == '.-':
                    if leftSize[0] != rightSize[0] or leftSize[1] != rightSize[1]:
                        self.errors.append("Error: Matrices sizes should match")
                elif op == '.*' or op == './':
                    if leftSize[0] != rightSize[1] or leftSize[1] != rightSize[0]:
                        self.errors.append("Error: Matrices sizes should match")
            elif typeLeft == 'vector' and typeRight == 'vector':
                leftSize = self.visit(nodeLeft.value)
                rightSize = self.visit(nodeRight.value)
                if op == '+' or op == '*':
                    if leftSize[0] != rightSize[0] or leftSize[1] != rightSize[1]:
                        self.errors.append("Error: Vectors sizes should match")

        return type

    def visit_Matrix(self, node):
        return 'matrix'

    def visit_MatrixRows(self, node):
        prevLen = -1

        for row in node.array_list:
            newLen = self.visit(row)
            if prevLen == -1:
                prevLen = newLen
            elif prevLen != newLen:
                self.errors.append("Error: Rows length does not match")

        valueList = [len(node.array_list), prevLen]

        return valueList

    def visit_Vector(self, node):
        return 'vector'

    def visit_VectorValues(self, node):
        return len(node.array_list)

    def visit_Variable(self, node):
        symbol = self.table.get(node.name)
        if symbol is None:
            self.errors.append("Error: Undefined variable")

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_StringNum(self, node):
        return 'string'

    def visit_Reference(self, node):
        self.visit(node.var)
        # TODO: check wartosci macierzy ktore jakos bysmy trzymali
