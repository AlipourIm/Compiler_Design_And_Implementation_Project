class Scanner:
    def __init__(self):
        self.pos = 0
        self.lexeme = ""
        self.line = 0
        self.file = open("input.txt", "r")

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


