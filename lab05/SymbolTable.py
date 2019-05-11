class Symbol(object):
    pass


class SimpleSymbol(Symbol):
    def __init__(self, type):
        self.type = type


class MatrixSymbol(Symbol):
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y


class SymbolTable(object):
    def __init__(self, parent, name):
        self.symbols = {}
        self.parent = parent
        self.name = name
        pass

    def put(self, name, type):
        self.symbols[name] = type

    def get(self, name):
        try:
            s = self.symbols[name]
            return s
        except KeyError:
            return None

    def remove(self, name):
        del self.symbols[name]

    def getGlobal(self, name):
        s = self.get(name)
        if s is None:
            if self.parent is not None:
                return self.parent.getGlobal(name)
            else:
                return None
        else:
            return s

    def getParentScope(self):
        return self.parent
