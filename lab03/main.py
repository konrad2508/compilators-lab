import sys
import ply.yacc as yacc
import Mparser

if __name__ == '__main__':
    filename = ""

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    scanner = Mparser.scanner

    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    ast.printTree()
