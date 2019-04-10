import AST


# typ['+']['int']['float'] = 'float'
class NodeVisitor(object):

    def __init__(self):
        self.errors = []

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

    def visit_BinExp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        args = [node.left, node.right]

        if any(isinstance(e, AST.Vector) for e in args):
            print("AHHHHHH")

    def visit_Vector(self, node):
        pass

    def visit_IntNum(self, node):
        pass

    def visit_Variable(self, node):
        pass
