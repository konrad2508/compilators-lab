#!/usr/bin/python

from argparse import ArgumentParser
from collections import defaultdict

import ply.lex as lex


def parse():
    parser = ArgumentParser(
        description="lab1 solution - scanner")
    parser.add_argument(dest='path_to_code',
                        type=str,
                        help='path to file with code to be scanned')
    return vars(parser.parse_args())


tokens = ["DOTADD", "DOTSUB", "DOTMUL", "DOTDIV",
          "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN",
          "LEQ", "GEQ", "NEQ", "EQ",
          "FLOAT", "INT", "ID",
          "STRING"]

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

tokens += list(reserved.values())
literals = "+-*/=<>()[]{}\',;:"

t_ignore = ' \t'

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'\-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LEQ = r'<='
t_GEQ = r'>='
t_NEQ = r'!='
t_EQ = r'=='


def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-zA-Z]\w*'
    # t.value = str(t.value)
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    line_starts[t.lexer.lineno] = t.lexpos


def t_error(t):
    print("[{}]: illegal character '{}'".format(t.lineno, t.value[0]))
    t.lexer.skip(1)


def t_ignore_COMMENT(t):
    r'\#.*'
    pass


# from ply docs


def find_column(token):
    line_start = line_starts[token.lineno]
    return (token.lexpos - line_start) + 1


line_starts = defaultdict(int)

lexer = lex.lex()

if __name__ == '__main__':
    path_to_code = parse()['path_to_code']
    with open(path_to_code, "r") as file:
        text = file.read()
        lexer.input(text)
        for token in lexer:
            column = find_column(text, token)
            print("[{}, {}], {}({})".format(
                token.lineno, column, token.type, token.value))
