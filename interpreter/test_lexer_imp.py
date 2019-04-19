from lexer_imp import *

if __name__ == '__main__':
    file = open('hello.imp')
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    for token in tokens:
        print(token)
