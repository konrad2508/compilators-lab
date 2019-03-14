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
             'DIVASSIGN', 'LTE', 'GTE', 'NEQ', 'EQ', 'ID', 'FLOAT', 'INT', 'STRING', 'TRANSPOSE'
         ) + tuple(reserved.values())

literals = ['+', '-', '*', '/', '=', '<', '>', '(', ')', '[', ']', '{', '}', ':', ';', ',']
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
t_TRANSPOSE = r"'"


def t_ID(t):
    # capture strings starting with letter or underscore
    r'[a-zA-Z_]\w*'

    # check if a reserved keyword was not caught instead
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOAT(t):
    # capture floats from python, i.e. numbers in format 6.1, 6., .6 or 60.52E2
    r'\d+\.\d*([eE]\d+)?|\d*\.\d+([eE]\d+)?'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    # strings must be enclosed within quotation marks
    # correct regex to catch other quotation marks should be (["'`])(.*?)\1, but for some reason re throws error
    r'"(.*?)"'

    # strip quotation marks
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print("Error starting at character '" + str(t.value[0]) + "' at line: " + str(t.lexer.lineno))
    t.lexer.skip(1)


def find_tok_column(t):
    return lexer.charno


lexer = lex.lex()
lexer.charno = 1
