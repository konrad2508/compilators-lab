import sys

from Mparser import parser
from scanner import lexer
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "./examples/init.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    tokens = parser.parse(text, lexer=lexer)
    checker = TypeChecker()
    checker.visit(tokens)

    if checker.any_errors():
        for error in checker.get_errors():
            print(error)
    else:
        print(tokens)