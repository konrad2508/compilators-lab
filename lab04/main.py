import sys
import ply.yacc as yacc
import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    scanner = Mparser.scanner

    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=scanner.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    errors = typeChecker.get_errors()

    if len(errors) > 0:
        for error in errors:
            print(error)
    # else:
    #     print(ast)
