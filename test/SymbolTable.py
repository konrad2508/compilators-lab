from collections import OrderedDict


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class ForLoopSymbol(Symbol):
    def __init__(self):
        super(ForLoopSymbol, self).__init__("FORLOOP")

    def __str__(self):
        return '<FORLOOP>'

    __repr__ = __str__


class WhileLoopSymbol(Symbol):
    def __init__(self):
        super(WhileLoopSymbol, self).__init__("WHILELOOP")

    def __str__(self):
        return '<WHILELOOP>'

    __repr__ = __str__


class IfConditionSymbol(Symbol):
    def __init__(self):
        super(IfConditionSymbol, self).__init__("IfCondition")

    def __str__(self):
        return '<IFCONDITION>'

    __repr__ = __str__


class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def __str__(self):
        # fancy tostr
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Enclosing scope',
                 self.enclosing_scope.scope_name if self.enclosing_scope else None
                 )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def insert(self, symbol):
        print('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print('Lookup: %s. (Scope name: %s)' % (name, self.scope_name))
        # 'symbol' is either an instance of the Symbol class or None
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

        return None
