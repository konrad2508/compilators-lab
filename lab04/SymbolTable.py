class Symbol(object):
    pass


class VariableSymbol(Symbol):
    def __init__(self, type, value):
        self.type = type
        self.type = value


class SymbolTable(object):
    def __init__(self, parent, name):
        self.symbols = {}
        self.parent = parent
        self.name = name
        pass

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        try:
            s = self.symbols[name]
            return s
        except KeyError:
            return None

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
