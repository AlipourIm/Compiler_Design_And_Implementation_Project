class ErrorHandler:
    lexical_error_file = open("lexical_errors.txt", "w")
    syntax_error_file = open("syntax_errors.txt", "w")
    line = -1
    errors_in_line = ""
    number_of_lexical_errors = 0
    number_of_syntax_errors = 0

    def __init__(self):
        pass

    def catch_error(self, error_name, characters_of_error, line_of_error):
        pass

    @staticmethod
    def flush_lexical_error():
        if ErrorHandler.number_of_lexical_errors == 0:
            ErrorHandler.lexical_error_file.write("There is no lexical error.")
        else:
            ErrorHandler.lexical_error_file.write(ErrorHandler.errors_in_line + "\n")
        ErrorHandler.close_file(ErrorHandler.lexical_error_file)

    @staticmethod
    def catch_lexical_error(line, lexeme, message):

        ErrorHandler.number_of_lexical_errors += 1

        if "comment" in message:
            lexeme = lexeme if len(lexeme) < 8 else lexeme[0:7] + "..."

        if ErrorHandler.line != line:
            if ErrorHandler.line != -1:
                ErrorHandler.lexical_error_file.write(ErrorHandler.errors_in_line + "\n")
            ErrorHandler.line = line
            ErrorHandler.errors_in_line = str(ErrorHandler.line) + ".\t"

        ErrorHandler.errors_in_line += "(" + lexeme + ", " + message.replace("ERR: ", "") + ") "

    @staticmethod
    def catch_syntax_error(line, message):
        ErrorHandler.number_of_syntax_errors += 1
        ErrorHandler.syntax_error_file.write("#" + str(line) + " : " + message)

    @staticmethod
    def flush_syntax_error():
        if ErrorHandler.number_of_syntax_errors == 0:
            ErrorHandler.syntax_error_file.write("There is no syntax error.")
        ErrorHandler.close_file(ErrorHandler.syntax_error_file)

    @staticmethod
    def close_file(f):
        f.close()
