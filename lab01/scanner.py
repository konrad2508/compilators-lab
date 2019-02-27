import ply.lex as lex

# TODO kolejnosc operatorow, numer znaku oraz ogarniecie dupy z mainem

tokens = ('COMMENT',
          'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'LTE', 'GTE',
          'NEQ',
          'EQ', 'IF', 'ELSE', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'RETURN', 'EYE', 'ZEROS', 'ONES', 'PRINT',
          'ID', 'INT', 'FLOAT', 'STRING'
          )

literals = "+-*/=<>()[]{}:',;"
t_ignore = '  \t'


def t_COMMENT(t):
    r'\#.*'


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


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_FOR(t):
    r'for'
    return t


def t_WHILE(t):
    r'while'
    return t


def t_BREAK(t):
    r'break'
    return t


def t_CONTINUE(t):
    r'continue'
    return t


def t_RETURN(t):
    r'return'
    return t


def t_EYE(t):
    r'eye'
    return t


def t_ZEROS(t):
    r'zeros'
    return t


def t_ONES(t):
    r'ones'
    return t


def t_PRINT(t):
    r'print'
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
    fh = open('ex2.txt', "r")
    lexer.input(fh.read())
    for token in lexer:
        print("line %d: %s(%s)" % (token.lineno, token.type, token.value))
