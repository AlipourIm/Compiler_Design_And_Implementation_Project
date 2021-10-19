class SymbolTable:
    f = open("symbol_table.txt", "w")
    symbol_table = ["if", "else", "void", "int", "repeat", "break", "until", "return"]

    def __init__(self):
        pass

    def add_row(self, lexeme):
        pass

    def print_table_phase1(self):
        pass

    @staticmethod
    def add_symbol(symbol):
        if symbol not in SymbolTable.symbol_table:
            SymbolTable.symbol_table.append(symbol)

    @staticmethod
    def get_token_type(symbol): # ID or KEYWORD?
        return "KEYWORD" if (SymbolTable.symbol_table.index(symbol) <= 7) else "ID"

    @staticmethod
    def print_symbols():
        for i in range(len(SymbolTable.symbol_table)):
            SymbolTable.f.write(str(i + 1) + ".\t" + SymbolTable.symbol_table[i] + "\n")

    @staticmethod
    def close_file():
        SymbolTable.f.close()
