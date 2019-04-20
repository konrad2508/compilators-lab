from structures import *

from SymbolTable import ScopedSymbolTable, VarSymbol


class NodeVisitor(object):
    def __init__(self):
        self.errors = []

    def any_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = ScopedSymbolTable("global", 1)

    def visit_InstructionsList(self, node: InstructionsList):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Integer(self, node: Integer):
        pass

    def visit_Float(self, node: Float):
        pass

    def visit_String(self, node: String):
        pass

    def visit_Assignment(self, node: Assignment):
        self.visit(node.id)
        self.visit(node.expression)
        op = node.assignment

        if op == "=":
            if isinstance(node.expression, Variable):
                # right hand side should be in scope
                symbol = self.symbol_table.lookup(node.expression.id)
                if symbol:
                    self.symbol_table.insert(VarSymbol(node.id, symbol.type))
                else:
                    self.errors.append("Error - right hand side not in scope {}".format(node.expression))
            elif isinstance(node.expression, (Matrix)):
                symbol = VarSymbol(node.id, ("MATRIX", node.expression.get_shape()))
                self.symbol_table.insert(symbol)
            elif isinstance(node.expression, Integer):
                self.symbol_table.insert(VarSymbol(node.id, ("INTEGER",)))
            elif isinstance(node.expression, Float):
                self.symbol_table.insert(VarSymbol(node.id, ("FLOAT",)))
        else:
            # assuming *= works like = _ .* _ and we type check only on surface
            pass


def visit_Matrix(self, node: Matrix):
    row_length = len(node.rows[0])
    for row in node.rows:
        if len(row) != row_length:
            self.errors.append("Error: inconsistent matrix dimensions - {} and {}".format(len(row), row_length))
        self.visit(row)


def visit_MatrixRow(self, node: MatrixRow):
    for element in node.items:
        is_number_constant = isinstance(element, int) or isinstance(element, float)
        is_number_variable = False
        # check if name is in scope and if name type is number e.g. row looks like [1, 2, x];
        if not (is_number_constant or is_number_variable):
            self.errors.append("Error: matrix element can only contain integer/float elements")


def visit_FuncCall(self, node: FuncCall):
    self.visit(node.params)
    if isinstance(node.params, Variable):
        # check if in scope and integer
        pass
    elif not isinstance(node.params, Integer):
        self.errors.append("Error: argument of reserved function call should be integer")


def visit_Variable(self, node: Variable):
    # add variable with value/type to scope
    pass


def visit_IndicesAssignment(self, node: IndicesAssignment):
    self.visit(node.id)
    self.visit(node.value)
    self.visit(node.items)
    type = self.check_id_type(node.id)
    if type in ():
        pass
    # check if range is valid (node.items)
    # check type of node.value (int or float or variable of that type)
    pass


def visit_BinaryOperation(self, node: BinaryOperation):
    # assuming binary ops can be only performed on non-matrix objects
    # check if types are valid for node.left, node.right
    pass


def visit_LogicalOperation(self, node: LogicalOperation):
    # check if left/right types are legit (e.g. comparable)
    self.visit(node.left)
    self.visit(node.right)
    pass


def visit_MatrixOperation(self, node: MatrixOperation):
    self.visit(node.left)
    self.visit(node.right)
    pass


def visit_TransposeOperation(self, node: TransposeOperation):
    # verify that node.value is a matrix
    pass


def visit_Range(self, node: Range):
    # verify if node.left/right are integers or names in scope
    pass


def visit_PrintInstruction(self, node: PrintInstruction):
    for value in node.values:
        self.visit(value)
    # verify correctness of all node values
    pass


def visit_ForLoop(self, node: ForLoop):
    self.visit(node.enumeration)
    self.visit(node.instructions)
    # it starts to get tricky here with scopes
    pass


def visit_WhileLoop(self, node: WhileLoop):
    self.visit(node.condition)
    self.visit(node.instructions)
    # and here too
    pass


def visit_Enumeration(self, node: Enumeration):
    self.visit(node.range)
    self.visit(node.variable)
    # verify names in scope
    pass


def visit_IfCondition(self, node: IfCondition):
    self.visit(node.condition)
    self.visit(node.instruction)
    self.visit(node.else_branch)
    # verify names in scope
