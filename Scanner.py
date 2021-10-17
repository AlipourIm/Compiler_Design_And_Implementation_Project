import os

from ErrorHandler import ErrorHandler
from SymbolTable import SymbolTable


class Scanner:
    def __init__(self, buffer_length=32):
        self.buffer_length = buffer_length
        self.current_state = 0
        self.lexeme = ""
        self.buffer_pointer = 0
        self.buffer = ""
        self.line = 1
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
        self.buffer = "" + self.file.read(self.buffer_length)
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
        if "ERR" in message:
            ErrorHandler.print_lexical_error(self.line, lexeme, message)
        elif "KEYWORD/ID" in message:
            SymbolTable.add_symbol(lexeme)

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
        tmp_current_state = self.current_state
        tmp_lexeme = self.lexeme
        self.current_state = 0
        self.lexeme = ""
        if tmp_current_state in self.look_ahead_states:
            if self.buffer_pointer != self.buffer_length - 1:
                self.buffer_pointer -= 1
            else:
                self.lexeme += "" + tmp_lexeme[len(tmp_lexeme) - 1]
                self.current_state = self.dfa_table[self.current_state][ord(self.lexeme)]
            if self.buffer[self.buffer_pointer] == "\n":
                self.line -= 1
            tmp_lexeme = tmp_lexeme[:-1]

        return tmp_lexeme, self.final_state_message[self.final_states.index(tmp_current_state)]


scanner = Scanner()
while True:
    token = scanner.get_next_token()
    print(str(scanner.line) + ".\t" + str(token))
    if token[1] == "EOF":
        break
SymbolTable.print_symbols()