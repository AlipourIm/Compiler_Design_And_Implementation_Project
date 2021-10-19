class ErrorHandler:
    f = open("lexical_errors.txt", "w")
    line = -1
    errors_in_line = ""
    number_of_errors = 0

    def __init__(self):
        pass

    def catch_error(self, error_name, characters_of_error, line_of_error):
        pass

    @staticmethod
    def flush_lexical_error():
        if ErrorHandler.number_of_errors == 0:
            ErrorHandler.f.write("There is no lexical error.")
        else:
            ErrorHandler.f.write(ErrorHandler.errors_in_line + "\n")

    @staticmethod
    def catch_lexical_error(line, lexeme, message):

        ErrorHandler.number_of_errors += 1

        if "comment" in message:
            lexeme = lexeme if len(lexeme) < 8 else lexeme[0:7] + "..."

        if ErrorHandler.line != line:
            if ErrorHandler.line != -1:
                ErrorHandler.f.write(ErrorHandler.errors_in_line + "\n")
            ErrorHandler.line = line
            ErrorHandler.errors_in_line = str(ErrorHandler.line) + ".\t"

        ErrorHandler.errors_in_line += "(" + lexeme + ", " + message.replace("ERR: ", "") + ") "

    @staticmethod
    def close_file():
        ErrorHandler.f.close()
