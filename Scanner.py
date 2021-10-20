from DFA import DFA
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
        self.dfa_table = DFA.dfa_table
        self.refill_buffer()

    @staticmethod
    def final_state_initializer():
        final_states = []
        final_states_message = []
        for i in DFA.final_states:
            final_states.append(i[0])
            final_states_message.append(i[1])
        return final_states, final_states_message, DFA.look_ahead_states

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

        while True:
            lexeme, message, line = self.find_next_token()

            if "ERR" in message:
                ErrorHandler.catch_lexical_error(line, lexeme, message)
                continue
            elif "WHITESPACE" in message or "COMMENT" in message:
                continue
            elif "KEYWORD/ID" in message:
                SymbolTable.add_symbol(lexeme)
                message = message.replace("KEYWORD/ID", SymbolTable.get_token_type(lexeme))

            return lexeme, message, line

    def find_next_token(self):
        start_line = self.line
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
            if self.buffer_pointer != 0:
                self.buffer_pointer -= 1
                if self.buffer[self.buffer_pointer] == "\n":
                    self.line -= 1
            else:
                self.lexeme += "" + tmp_lexeme[len(tmp_lexeme) - 1]
                self.current_state = self.dfa_table[self.current_state][ord(self.lexeme)]

            tmp_lexeme = tmp_lexeme[:-1]

        return tmp_lexeme, self.final_state_message[self.final_states.index(tmp_current_state)], start_line
