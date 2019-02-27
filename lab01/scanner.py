import ply.lex as lex

# TODO kolejnosc operatorow, numer znaku oraz ogarniecie dupy z mainem

tokens = (
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'LTE', 'GTE', 'NEQ',
    'EQ', 'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN', 'EYE', 'ZEROS', 'ONES', 'PRINT',
    'ID', 'INT', 'FLOAT', 'STRING'
)

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LTE = r'<='
t_GTE = r'>='
t_NEQ = r'!='
t_EQ = r'=='
t_IF = r'if'
t_ELSE = r'else'
t_FOR = r'for'
t_WHILE = r'while'
t_BREAK = r'break'
t_CONTINUE = r'continue'
t_RETURN = r'return'
t_EYE = r'eye'
t_ZEROS = r'zeros'
t_ONES = r'ones'
t_PRINT = r'print'

literals = "+-*/=<>()[]{}:',;"
t_ignore = '  \t'


def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'\d*\.d+'
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'\S'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


if __name__ == '__main__':
    lexer = lex.lex()
    fh = open('example_full.txt', "r")
    lexer.input(fh.read())
    for token in lexer:
        print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
