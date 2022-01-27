from anytree import Node, RenderTree

from CodeGen import CodeGen
from ErrorHandler import ErrorHandler
from Scanner import Scanner
from SymbolTable import SymbolTable
from ActionTable import ActionTable as at


class Parser:

    def __init__(self):
        self.tokens_file = open("tokens.txt", "w")
        self.tokens = []
        self.line = -1
        self.tokens_in_line = ""

        self.root = Node("Program")
        self.current_node = self.root
        self.current_node_id = 0
        self.stack = [0]

    def main(self):
        scanner = Scanner()
        code_gen = CodeGen()
        symbol_table = SymbolTable()

        avoid_get_next_token = False
        lexeme, message, line, token, terminal, terminal_id = [None for _ in range(6)]

        while True:

            if avoid_get_next_token:
                avoid_get_next_token = False
            else:
                token = scanner.get_next_token()
                lexeme, message, line = token

                self.update_line(token)

                terminal = lexeme
                if message in ['NUM', 'ID', '$']:
                    terminal = message
                terminal_id = at.terminals.index(terminal)

            action = at.table[self.current_node_id][terminal_id]

            while action[0] in ['go', 'return', 'sync', 'action_symbol']:

                if action[0] in ['return', 'sync']:

                    self.current_node_id = self.stack.pop()
                    node_parent = self.current_node.parent

                    if action[0] == 'sync':
                        ErrorHandler.catch_syntax_error(self.line, f'syntax error, missing {self.current_node.name}')
                        # remove it from parse_tree
                        self.current_node.parent = None

                    self.current_node = node_parent
                    action = at.table[self.current_node_id][terminal_id]

                elif action[0] == 'go':
                    node_str = 'epsilon' if action[1] == 'ε' else at.non_terminals[action[1]].replace('_', '-')
                    self.current_node = Node(node_str, parent=self.current_node)

                    if action[1] == 'ε':
                        self.current_node_id = action[2]

                    else:
                        self.current_node_id = action[1]
                    self.stack.append(action[2])
                    action = at.table[self.current_node_id][terminal_id]

                elif action[0] == 'action_symbol':
                    print("new action symbol: ", action)
                    code_gen.code_gen(action[1], token)
                    self.current_node_id = action[2]
                    action = at.table[self.current_node_id][terminal_id]

            if action[0] == 'get':
                if action[1] == terminal:
                    if message == '$':
                        Node('$', parent=self.current_node)
                    else:
                        Node(f'({message}, {lexeme})', parent=self.current_node)
                else:
                    ErrorHandler.catch_syntax_error(self.line, f'syntax error, missing {action[1]}')
                    avoid_get_next_token = True

                self.current_node_id = action[2]

            elif action[0] == 'empty':
                if token[1] == '$':
                    ErrorHandler.catch_syntax_error(self.line, f'syntax error, Unexpected EOF')
                    # remove $ node from end of parse_tree, as in test_case_10
                    self.current_node.parent = None
                else:
                    ErrorHandler.catch_syntax_error(self.line, f'syntax error, illegal {terminal}')

            if token[1] == '$':

                self.print_parse_tree()

                # flush last line if it includes any token other than $
                if self.tokens_in_line[-1] != "\t":
                    self.tokens_file.write(self.tokens_in_line + "\n")
                # flush ErrorHandler for last line
                print(code_gen.ss)
                code_gen.flush_program_block()
                ErrorHandler.flush_lexical_error()
                ErrorHandler.flush_syntax_error()
                break

        SymbolTable.print_symbols()

        self.tokens_file.close()
        return

    def update_line(self, token):
        if self.line != token[2]:
            if self.line != -1:
                self.tokens_file.write(self.tokens_in_line + "\n")
            self.line = token[2]
            self.tokens_in_line = str(self.line) + ".\t"
        if token[1] != "$":
            self.tokens_in_line += "(" + token[1] + ", " + token[0] + ") "

    def print_parse_tree(self):
        # for pre, fill, node in RenderTree(self.root):
        #     print("%s%s" % (pre, node.name))
        parse_tree = ""

        for pre, fill, node in RenderTree(self.root):
            parse_tree += "%s%s" % (pre, node.name) + '\n'
        parse_tree = parse_tree[:-1]
        with open("parse_tree.txt", "w") as f:
            f.write(parse_tree)
        return
