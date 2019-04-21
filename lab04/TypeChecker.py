import AST


class NodeVisitor(object):
    def __init__(self):
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
        self.visit(node.left)
        self.visit(node.right)

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
                    if not isinstance(value, int) and not isinstance(value, AST.IntNum):
                        self.errors.append("Error: Function argument must be an integer")
            elif not isinstance(node.args, int) and not isinstance(node.args, AST.IntNum):
                self.errors.append("Error: Function argument must be an integer")

    def visit_BinExp(self, node):
        typeLeft = node.left
        typeRight = node.right
        op = node.op

        normalOps = ['+', '-', '*', '/']
        matrixOps = ['.+', '.-', '.*', './']

        if isinstance(typeLeft, AST.IntNum) or isinstance(typeLeft, AST.FloatNum):
            if not isinstance(typeRight, AST.IntNum) or not isinstance(typeRight, AST.FloatNum):
                self.errors.append("Error: Wrong types of arguments")
            elif op in matrixOps:
                self.errors.append("Error: Wrong operator type")
        elif isinstance(typeLeft, AST.StringNum):
            if not isinstance(typeRight, AST.Variable):
                self.errors.append("Error: Wrong types of arguments")
            elif not op == '-' or not op == '+':
                self.errors.append("Error: Wrong operator type")
        elif isinstance(typeLeft, AST.StringNum):
            if not isinstance(typeRight, AST.StringNum):
                self.errors.append("Error: Wrong types of arguments")
            elif not op == '-' or not op == '+':
                self.errors.append("Error: Wrong operator type")
        elif isinstance(typeLeft, AST.Vector):
            if not isinstance(typeRight, AST.Vector):
                self.errors.append("Error: Wrong types of arguments")
            elif op in normalOps:
                self.errors.append("Error: Wrong operator type")
        elif isinstance(typeLeft, AST.Matrix):
            if not isinstance(typeRight, AST.Matrix):
                self.errors.append("Error: Wrong types of arguments")
            elif op in normalOps:
                self.errors.append("Error: Wrong operator type")
            elif isinstance(typeRight, AST.Matrix):
                leftSize = self.visit(typeLeft)
                rightSize = self.visit(typeRight)

                if op == '.+' or op == '.-':
                    if leftSize[0] != rightSize[0] or leftSize[1] != rightSize[1]:
                        self.errors.append("Error: Matrices sizes should match")
                else:
                    if leftSize[0] != rightSize[1] or leftSize[1] != rightSize[0]:
                        self.errors.append("Error: Matrices sizes should match")

    def visit_Matrix(self, node):
        return self.visit(node.value)

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

    # TODO: MHM YEAYEA
    def visit_Vector(self, node):
        pass

    def visit_VectorValues(self, node):
        return len(node.array_list)

    def visit_Variable(self, node):
        pass

    def visit_IntNum(self, node):
        pass
