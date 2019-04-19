import sys
from parser_imp import *

if __name__ == '__main__':
    filename = 'foo.imp'
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)

    print(tokens)

    parser = bexp()
    result = parser(tokens, 0)
    print(result)

