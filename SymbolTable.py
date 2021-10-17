class SymbolTable:
    symbol_table = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
    f = open("symbol-table.txt", "w")

    def __init__(self):
        pass

    def add_row(self, lexeme):
        pass

    def print_table_phase1(self):
        pass

    @staticmethod
    def add_symbol(symbol):
        if not (symbol in SymbolTable.symbol_table):
            SymbolTable.append(symbol)

    @staticmethod
    def print_symbols():
        for i in range(len(SymbolTable.symbol_table)):
            SymbolTable.f.write(str(i + 1) + ".\t" + SymbolTable.symbol_table[i] + "\n")

    @staticmethod
    def close_file():
        SymbolTable.f.close()
