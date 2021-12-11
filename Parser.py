from ErrorHandler import ErrorHandler
from Scanner import Scanner
from SymbolTable import SymbolTable
from anytree import Node, RenderTree


class Parser:

    def __init__(self):
        self.f = open("tokens.txt", "w")
        self.parse_tree_file = open("parse_tree.txt", "w")
        self.tokens = []
        self.line = -1
        self.tokens_in_line = ""
        self.parse_tree = None

    def main(self):
        scanner = Scanner()

        while True:
            token = scanner.get_next_token()
            if self.line != token[2]:
                if self.line != -1:
                    self.f.write(self.tokens_in_line + "\n")
                self.line = token[2]
                self.tokens_in_line = str(self.line) + ".\t"

            if token[1] != "EOF":
                self.tokens_in_line += "(" + token[1] + ", " + token[0] + ") "
            else:
                # flush last line if it includes any token other than EOF
                if self.tokens_in_line[-1] != "\t":
                    self.f.write(self.tokens_in_line + "\n")
                # flush ErrorHandler for last line
                ErrorHandler.flush_lexical_error()
                break

        SymbolTable.print_symbols()

        self.f.close()

    def dump_parse_tree(self):
        for pre, fill, node in RenderTree(self.parse_tree):
            self.parse_tree_file.write("%s%s" % (pre, node.name))
        self.parse_tree_file.close()
