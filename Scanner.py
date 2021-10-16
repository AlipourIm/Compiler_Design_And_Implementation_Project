import os


class Scanner:
    def __init__(self):
        self.buffer_pointer = 0
        self.buffer = ""
        self.line = 0
        self.file = open("input.txt", "r")
        self.final_states, self.final_state_message, self.look_ahead_states = Scanner.final_state_initializer()
        self.dfa_table = Scanner.dfa_initializer()
        self.refill_buffer()

    @staticmethod
    def dfa_initializer():
        dfa_table = []
        with open(os.path.join(os.path.dirname(__file__), "preprocess/DFA_Table.txt"), "r") as f:
            number_of_states = 0
            for line in f:
                dfa_table.append(line.strip('][').replace('"', '').split(','))
                number_of_states += 1
        for i in range(number_of_states):
            dfa_table[i][255] = dfa_table[i][255].replace("]\n", "")
        f.close()
        dfa_table = [list(map(int, i)) for i in dfa_table]
        return dfa_table

    @staticmethod
    def final_state_initializer():
        final_states = []
        final_states_message = []
        with open(os.path.join(os.path.dirname(__file__), "preprocess/final_states.txt"), "r") as f:
            for line in f:
                items = line.split(", '")
                items[0] = int(items[0].replace("[", ""))
                items[1] = items[1].replace("']\n", "")
                final_states.append(int(items[0]))
                final_states_message.append(items[1])
            f.close()
        with open(os.path.join(os.path.dirname(__file__), "preprocess/look_ahead_states.txt"), "r") as f:
            look_ahead_states = list(map(int, f.readline().split()))
            f.close()
            return final_states, final_states_message, look_ahead_states

    def refill_buffer(self):
        self.buffer = "" + self.file.read(32)
        if len(self.buffer) < 32:
            self.buffer = self.buffer + "\0"
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
        current_state = 0
        lexeme = ""
        while not (current_state in self.look_ahead_states or current_state in self.final_states):
            lexeme += self.buffer[self.buffer_pointer]
            current_state = self.dfa_table[current_state][ord(self.buffer[self.buffer_pointer])]
            self.buffer_pointer += 1
            if self.buffer_pointer == 32:
                self.refill_buffer()  # Buffer has EOF, my idea: use a flag.
        if current_state in self.look_ahead_states:  # How to look ahead?
            self.buffer_pointer -= 1
            lexeme = lexeme[:-1]
        return lexeme, self.final_state_message[self.final_states.index(current_state)]


scanner = Scanner()

while True:
    token = scanner.get_next_token()
    print(token)
    if token[1] == "EOF":
        break
