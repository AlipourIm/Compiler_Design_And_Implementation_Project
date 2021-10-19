from Scanner import Scanner
from SymbolTable import SymbolTable


class Parser:

    def __init__(self):
        self.f = open("tokens.txt", "w")
        self.tokens = []

    def main(self):
        scanner = Scanner()
        line = -1
        tokens_in_line = ""

        while True:
            token = scanner.get_next_token()

            if line != token[2]:
                if line != -1:
                    self.f.write(tokens_in_line + "\n")
                line = token[2]
                tokens_in_line = str(line) + ".\t"

            tokens_in_line += "(" + token[1] + ", " + token[0] + ") "
            if token[1] == "EOF":
                break
        SymbolTable.print_symbols()