from anytree import Node, RenderTree

import FirstFollowPredict
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

        while True:
            token = scanner.get_next_token()
            lexeme, message, line = token

            terminal = lexeme
            if message in ['NUM', 'ID', '$']:
                terminal = message

            print("_________\nNew Terminal: ", terminal)
            terminal_id = at.terminals.index(terminal)

            # self.print_parse_tree()

            action = at.table[self.current_node_id][terminal_id]
            self.print_action(terminal, terminal_id, action)

            if self.current_node_id == 46:
                print(FirstFollowPredict.FirstFollowPredict.follows[1])

            while action[0] in ['go', 'return']:
                if action[0] == 'return':
                    print('...conducting a return state')
                    self.current_node_id = self.stack.pop()
                    # while self.current_node.name == 'epsilon':
                    #     self.current_node = self.current_node.parent
                    self.current_node = self.current_node.parent

                    print("stack after return = ", self.stack)
                    print(f"current_node_id = {self.current_node_id} ({self.current_node.name})", '\n')
                    action = at.table[self.current_node_id][terminal_id]
                    self.print_action(terminal, terminal_id, action)

                if action[0] == 'go':
                    node_str = 'epsilon' if action[1] == 'ε' else at.non_terminals[action[1]].replace('_', '-')
                    self.current_node = Node(node_str, parent=self.current_node)
                    # self.print_parse_tree()
                    if action[1] == 'ε':
                        self.current_node_id = action[2]
                        # self.current_node_id = self.stack.pop()
                        # self.current_node = self.current_node.parent

                    else:
                        self.current_node_id = action[1]
                    self.stack.append(action[2])
                    action = at.table[self.current_node_id][terminal_id]
                    self.print_action(terminal, terminal_id, action)

            if action[0] == 'get':
                Node(f'({message}, {lexeme})', parent=self.current_node)
                # self.current_node = self.current_node.parent
                print(token)
                # self.print_parse_tree()
                self.current_node_id = action[1]

            # self.print_parse_tree()

            if self.line != token[2]:
                if self.line != -1:
                    self.tokens_file.write(self.tokens_in_line + "\n")
                self.line = token[2]
                self.tokens_in_line = str(self.line) + ".\t"

            if token[1] != "$":
                self.tokens_in_line += "(" + token[1] + ", " + token[0] + ") "
            else:

                Node("$", parent=self.root)
                self.print_parse_tree()

                # flush last line if it includes any token other than $
                if self.tokens_in_line[-1] != "\t":
                    self.tokens_file.write(self.tokens_in_line + "\n")
                # flush ErrorHandler for last line
                ErrorHandler.flush_lexical_error()
                break

        SymbolTable.print_symbols()

        self.tokens_file.close()

    def print_parse_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))
        parse_tree = ""

        for pre, fill, node in RenderTree(self.root):
            parse_tree += "%s%s" % (pre, node.name) + '\n'
        parse_tree = parse_tree[:-1]
        with open("parse_tree.txt", "w") as f:
            f.write(parse_tree)
        return

    def print_action(self, terminal, terminal_id, action):
        if self.current_node_id < len(at.non_terminals):
            print(f"table[{self.current_node_id} ({at.non_terminals[self.current_node_id]})]"
                  f"[{terminal_id} ({terminal})]"
                  f" = {action}")
        elif self.current_node_id < 2 * len(at.non_terminals):
            print(f"table[{self.current_node_id} ({at.non_terminals[self.current_node_id - 45]})]"
                  f"[{terminal_id} ({terminal})]"
                  f" = {action}")
        else:
            print(f"table[{self.current_node_id} ({self.current_node.name})]"
                  f"[{terminal_id} ({terminal})]"
                  f" = {action}")
        return
