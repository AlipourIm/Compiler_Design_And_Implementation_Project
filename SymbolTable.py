class SymbolTable:
    f = open("symbol_table.txt", "w")
    symbol_table = []
    keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return", "endif"]

    def __init__(self):
        for keyword in SymbolTable.keywords:
            self.symbol_table.append(SymbolRecord(keyword, is_keyword=True))

    def add_row(self, lexeme):
        pass

    def print_table_phase1(self):
        pass

    @staticmethod
    def add_symbol(lexeme):
        for symbol_record in SymbolTable.symbol_table:
            if lexeme == symbol_record.lexeme:
                return symbol_record
        SymbolTable.symbol_table.append(SymbolRecord(lexeme))

    @staticmethod
    def declare_variable(lexeme, address, type_arg):
        tmp_table = SymbolTable.symbol_table[::-1]
        for symbol_record in tmp_table:
            if symbol_record.lexeme == lexeme:
                symbol_record.address = address
                symbol_record.type = type_arg
                symbol_record.proc_var_func = 'var'
                return

    @staticmethod
    def get_token_type(lexeme):  # ID or KEYWORD.
        return "KEYWORD" if (lexeme in SymbolTable.keywords) else "ID"

    @staticmethod
    def print_symbols():
        for i in range(len(SymbolTable.symbol_table)):
            SymbolTable.f.write(str(i + 1) + ".\t" + str(SymbolTable.symbol_table[i]) + "\n")

    @staticmethod
    def close_file():
        SymbolTable.f.close()


class SymbolRecord:
    def __init__(self, lexeme, is_keyword=False):
        self.lexeme = lexeme
        self.is_keyword = is_keyword
        self.address = None
        self.type = None
        self.scope = None
        self.proc_var_func = None
        self.no_arg_cell = None

    def __str__(self):
        return f'lexeme: {self.lexeme}, isKeyword: {self.is_keyword}, address: {self.address}, type: {self.type}, proc_var_func: {self.proc_var_func}, no_arg_cell: {self.no_arg_cell}, scope: {self.scope}'
