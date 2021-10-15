import os


class Scanner:
    def __init__(self):
        self.buffer_pointer = 0
        self.buffer = ""
        self.lexeme = ""
        self.line = 0
        self.file = open("input.txt", "r")
        self.dfa_table = []
        with open(os.path.join(os.path.dirname(__file__), "preprocess/DFA_Table.txt"), "r") as f:
            for line in f:
                self.dfa_table.append(line.strip('][').replace('"', '').split(','))
        for i in range(20):
            self.dfa_table[i][255] = self.dfa_table[i][255].replace("]\n", "")
        f.close()
        self.dfa_table = [list(map(int, i)) for i in self.dfa_table]

    def get_line(self):
        return self.line

    def get_file(self):
        return self.file

    def read_whole_file(self):
        return self.file.read()

    def read_one_character(self):
        return self.file.read(1)

    def get_next_token(self):
        pass                    # To be implemented

scanner = Scanner()
