import os


class Scanner:
    def __init__(self):
        self.buffer_pointer = 0
        self.buffer = ""
        self.lexeme = ""
        self.line = 0
        self.current_state = 0
        self.file = open("input.txt", "r")
        self.final_states, self.look_ahead_states = Scanner.final_state_initializer()
        self.dfa_table = Scanner.dfa_initializer()

    @staticmethod
    def dfa_initializer():
        dfa_table = []
        with open(os.path.join(os.path.dirname(__file__), "preprocess/DFA_Table.txt"), "r") as f:
            for line in f:
                dfa_table.append(line.strip('][').replace('"', '').split(','))
        for i in range(20):
            dfa_table[i][255] = dfa_table[i][255].replace("]\n", "")
        f.close()
        dfa_table = [list(map(int, i)) for i in dfa_table]
        return dfa_table

    @staticmethod
    def final_state_initializer():
        final_states = []
        look_ahead_states = []
        with open(os.path.join(os.path.dirname(__file__), "preprocess/final_states.txt"), "r") as f:
            for line in f:
                items = line.split(", ")
                items[0] = int(items[0].replace("[", ""))
                items[1] = items[1].replace("]", "")
                final_states.append(items)
            f.close()
        with open(os.path.join(os.path.dirname(__file__), "preprocess/look_ahead_states.txt"), "r") as f:
            look_ahead_states = list(map(int, f.readline().split()))
            f.close
            return final_states, look_ahead_states

    def refill_buffer(self):
        self.buffer = "" + self.file.read(32)
        self.buffer_pointer = 0

    def get_line(self):
        return self.line

    def get_file(self):
        return self.file

    def read_whole_file(self):
        return self.file.read()

    def read_one_character(self):
        return self.file.read(1)

    def get_next_token(self):
        self.current_state = 0
        self.lexeme = ""


scanner = Scanner()
