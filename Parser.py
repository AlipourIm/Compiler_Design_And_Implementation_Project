from Scanner import Scanner
from SymbolTable import SymbolTable


class Parser:
    def __init__(self):
        pass

    def main(self):
        scanner = Scanner()
        line = -1
        while True:
            token = scanner.get_next_token()
            print(str(scanner.line) + ".\t" + str(token))
            if token[1] == "EOF":
                break
        SymbolTable.print_symbols()