import sys
import ply.yacc as yacc
import Mparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter
from Exceptions import ReturnValueException

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

    if ast is not None:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)

        errors = typeChecker.get_errors()

        if len(errors) > 0:
            for error in errors:
                print(error)
        else:
            interpreter = Interpreter()
            try:
                interpreter.visit(ast)
            except ReturnValueException as e:
                print('Returned value: %s' % str(e.value))
