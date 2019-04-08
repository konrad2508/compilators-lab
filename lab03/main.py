import sys
import ply.yacc as yacc
import Mparser
import os
from TreePrinter import TreePrinter

# TODO ######################################################################################################
#                                                                                                           #
#       1) Wyjebac shift/reduce konflikty                                                                   #
#           - tak naprawde sa 3, bo 9 jest takich samych                                                    #
#           - nie wyglada to na cos waznego, bo wszystko dziala prawidlowo nawet z nimi                     #
#           - te 9 powstalo z zamiany w p_bin_expr prawej strony dzialania z 'value' na 'expression'        #
#           - reszta powstala z podmiany 'value' na 'object' w p_expression                                 #
#       2) Cleanup kodu                                                                                     #
#           - wydupczenie jakis niepotrzebnych debugowych printow                                           #
#           - jakies cos zrobienie by sie dalo cos powiedziec o tym kodzie bo obecnie                       #
#             to jeden wielki clusterfuck                                                                   #
#       3) Przetestowanie dla innych skrajnych przypadkow                                                   #
#                                                                                                           #
# TODO ######################################################################################################

if __name__ == '__main__':
    filename = ""

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example0.m"
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
