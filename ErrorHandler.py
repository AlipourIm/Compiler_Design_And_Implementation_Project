class ErrorHandler:
    f = open("lexical_errors.txt", "w")

    def __init__(self):
        pass

    def catch_error(self, error_name, characters_of_error, line_of_error):
        pass

    @staticmethod
    def print_lexical_error(line, lexeme, message):
        ErrorHandler.f.write(str(line) + ".\t(" + lexeme + " " + message + ")\n")

    @staticmethod
    def close_file():
        ErrorHandler.f.close()
