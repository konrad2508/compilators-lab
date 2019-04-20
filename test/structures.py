import attr


class Node:
    pass


@attr.s
class InstructionsList(Node):
    instructions = attr.ib(default=attr.Factory(list))

    def __add__(self, other):
        self.instructions += other.instructions
        return self


@attr.s
class Integer(Node):
    value = attr.ib()


@attr.s
class String(Node):
    value = attr.ib()


@attr.s
class Float(Node):
    value = attr.ib()


@attr.s
class Assignment(Node):
    id = attr.ib()
    assignment = attr.ib()
    expression = attr.ib()


@attr.s
class Matrix(Node):
    rows = attr.ib()

    def get_shape(self):
        return len(self.rows), len(self.rows[0])


@attr.s
class MatrixRow(Node):
    items = attr.ib()

    def __add__(self, other):
        self.items += other
        return self


@attr.s
class FuncCall(Node):
    name = attr.ib()
    params = attr.ib()


@attr.s
class Variable(Node):
    id = attr.ib()
    inverted = attr.ib(default=False)

    def __neg__(self):
        self.inverted = not self.inverted
        return self


@attr.s
class IndicesAssignment(Node):
    id = attr.ib()
    items = attr.ib()
    value = attr.ib()

    def __add__(self, newitems):
        self.range += newitems
        return self


@attr.s
class BinaryOperation(Node):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s
class LogicalOperation(Node):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s
class MatrixOperation(Node):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s
class TransposeOperation(Node):
    value = attr.ib()


@attr.s
class Range(Node):
    left = attr.ib()
    right = attr.ib()


@attr.s
class PrintInstruction(Node):
    values = attr.ib()


@attr.s
class ForLoop(Node):
    enumeration = attr.ib()
    instructions = attr.ib()


@attr.s
class WhileLoop(Node):
    condition = attr.ib()
    instructions = attr.ib()


@attr.s
class Enumeration(Node):
    variable = attr.ib()
    range = attr.ib()


@attr.s
class IfCondition(Node):
    condition = attr.ib()
    instruction = attr.ib()
    else_branch = attr.ib(default=None)
