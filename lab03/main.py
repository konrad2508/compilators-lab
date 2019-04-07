import sys
import ply.yacc as yacc
import Mparser
import os
from TreePrinter import TreePrinter

if __name__ == '__main__':
    filename = ""

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    if os.path.exists('parser.out'):
        os.remove('parser.out')

    if os.path.exists('parsetab.py'):
        os.remove('parsetab.py')

    scanner = Mparser.scanner

    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)

    sys.stdout = open('example_tree/out.tree', 'w+')
    ast.printTree()
