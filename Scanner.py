import os


class Scanner:
    def __init__(self, buffer_length=32):
        self.buffer_length = buffer_length
        self.look_ahead_character = ""
        self.current_state = 0
        self.lexeme = ""
        self.buffer_pointer = 0
        self.buffer = ""
        self.line = 1
        self.file = open("input.txt", "r")
        self.final_states, self.final_state_message, self.look_ahead_states = Scanner.final_state_initializer()
        self.dfa_table = Scanner.dfa_initializer()
        self.buffer_initializer()
        print(self.look_ahead_character)

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
        self.look_ahead_character += "" + self.buffer[len(self.buffer) - 1]
        self.buffer = "" + self.file.read(self.buffer_length)
        if len(self.buffer) < self.buffer_length:
            self.buffer = self.buffer + "\0"
        self.buffer_pointer = 0

    def buffer_initializer(self):
        self.buffer = "" + self.file.read(self.buffer_length)
        self.look_ahead_character += "" + self.buffer[len(self.buffer) - 1]
        if len(self.buffer) < self.buffer_length:
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
        lexeme, message = self.find_next_token()

        return lexeme, message

    def find_next_token(self):
        while not (self.current_state in self.final_states):
            if self.buffer[self.buffer_pointer] == "\n":
                self.line += 1
            self.lexeme += self.buffer[self.buffer_pointer]
            self.current_state = self.dfa_table[self.current_state][ord(self.buffer[self.buffer_pointer])]
            self.buffer_pointer += 1
            if self.buffer_pointer == self.buffer_length:
                self.refill_buffer()
        current_state = self.current_state
        lexeme = self.lexeme
        self.current_state = 0
        self.lexeme = ""
        if current_state in self.look_ahead_states:
            if self.buffer_pointer != self.buffer_length - 1:
                self.buffer_pointer -= 1
            else:
                self.lexeme += "" + self.look_ahead_character
                self.current_state = self.dfa_table[self.current_state][ord(self.look_ahead_character)]
            if self.buffer[self.buffer_pointer] == "\n":
                self.line -= 1
            lexeme = lexeme[:-1]

        return lexeme, self.final_state_message[self.final_states.index(current_state)]


scanner = Scanner()

while True:
    token = scanner.get_next_token()
    print(token)
    print(scanner.line)
    if token[1] == "EOF":
        break
