import sys
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = (
             'WHITESPACE', 'COMMENT', 'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN',
             'DIVASSIGN',
             'LTE', 'GTE', 'NEQ', 'EQ', 'ID', 'FLOAT', 'INT', 'STRING'
         ) + tuple(reserved.values())

literals = ['+', '-', '*', '/', '=', '<', '>', '(', ')', '[', ']', '{', '}', ':', ';', "'", ',']
operators = ['.+', '.-', '.*', './', '+=', '-=', '*=', '/=', '<=', '>=', '!=', '==']
t_ignore = '\t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.charno = 1


def t_WHITESPACE(t):
    r'\s+'
    lexer.charno += len(str(t.value))


def t_COMMENT(t):
    r'\#.*'
    # do nothing


def t_DOTADD(t):
    r'\.\+'
    return t


def t_DOTSUB(t):
    r'\.-'
    return t


def t_DOTMUL(t):
    r'\.\*'
    return t


def t_DOTDIV(t):
    r'\./'
    return t


def t_ADDASSIGN(t):
    r'\+='
    return t


def t_SUBASSIGN(t):
    r'-='
    return t


def t_MULASSIGN(t):
    r'\*='
    return t


def t_DIVASSIGN(t):
    r'/='
    return t


def t_LTE(t):
    r'<='
    return t


def t_GTE(t):
    r'>='
    return t


def t_NEQ(t):
    r'!='
    return t


def t_EQ(t):
    r'=='
    return t


def t_PLUS(t):
    r'\+'
    t.type = '+'
    return t


def t_MINUS(t):
    r'-'
    t.type = '-'
    return t


def t_MUL(t):
    r'\*'
    t.type = '*'
    return t


def t_DIV(t):
    r'/'
    t.type = '/'
    return t


def t_EQUAL(t):
    r'='
    t.type = '='
    return t


def t_LESS(t):
    r'<'
    t.type = '<'
    return t


def t_GREATER(t):
    r'>'
    t.type = '>'
    return t


def t_LPAREN(t):
    r'\('
    t.type = '('
    return t


def t_RPAREN(t):
    r'\)'
    t.type = ')'
    return t


def t_LSQPAREN(t):
    r'\['
    t.type = '['
    return t


def t_RSQPAREN(t):
    r'\]'
    t.type = ']'
    return t


def t_LCPAREN(t):
    r'\{'
    t.type = '{'
    return t


def t_RCPAREN(t):
    r'\}'
    t.type = '}'
    return t


def t_RANGE(t):
    r':'
    t.type = ':'
    return t


def t_TRANSPOS(t):
    r"'"
    t.type = "'"
    return t


def t_COMMA(t):
    r'\,'
    t.type = ','
    return t


def t_SEMICOLON(t):
    r';'
    t.type = ';'
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOAT(t):
    r'(\d*\.\d+E\d+|\d*\.\d+|\d+\.\d*)'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"(.*)"'
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print("Error starting at character '" + str(t.value[0]) + "' at line: " + str(t.lexer.lineno))
    t.lexer.skip(1)


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else 'example_full.txt'
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = lex.lex()
    lexer.charno = 1
    fh = open(filename, "r")
    lexer.input(fh.read())
    for token in lexer:
        print("(%d, %d): %s(%s)" % (token.lineno, lexer.charno, token.type, token.value))
        lexer.charno += len(str(token.value))
