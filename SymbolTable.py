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
    def declare_variable(lexeme, address, type_arg, scope, no_arg_cell=0):
        SymbolTable.symbol_table.append(
            SymbolRecord(lexeme=lexeme, address=address, type_=type_arg, scope=scope, no_arg_cell=no_arg_cell,
                         var_arr_func='array' if no_arg_cell else 'var'))

    @staticmethod
    def declare_param_variable(lexeme, offset, type_arg, scope, no_arg_cell=0):
        SymbolTable.symbol_table.append(
            SymbolRecord(lexeme=lexeme, offset=offset, type_=type_arg, scope=scope, no_arg_cell=no_arg_cell,
                         var_arr_func='array' if no_arg_cell else 'var', is_param=True))

    @staticmethod
    def declare_function(lexeme, type_arg):
        no_arg_cell = 0
        no_var = 0
        arg_type_list = []
        tmp_table = SymbolTable.symbol_table[::-1]
        for symbol_record in tmp_table:
            if symbol_record.lexeme == lexeme:
                symbol_record.type = type_arg
                symbol_record.no_arg_cell = no_arg_cell
                symbol_record.var_arr_func = 'func'
                symbol_record.no_var = no_var
                symbol_record.arg_type_list = arg_type_list[::-1]
                return
            else:
                if symbol_record.is_param:
                    no_arg_cell += 1
                    arg_type_list.append((symbol_record.type, symbol_record.var_arr_func))
                else:
                    no_var += 1
                SymbolTable.symbol_table.pop()

    @staticmethod
    def find_address(lexeme):
        tmp_table = SymbolTable.symbol_table[::-1]
        for symbol_record in tmp_table:
            if symbol_record.lexeme == lexeme:
                return symbol_record.address

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
    def __init__(self, lexeme, is_keyword=False, address=None, type_=None, scope=None, var_arr_func=None,
                 no_arg_cell=None, offset=None, is_param=False, no_var=None):
        self.lexeme = lexeme
        self.is_keyword = is_keyword
        self.address = address
        self.type = type_
        self.scope = scope
        self.var_arr_func = var_arr_func
        self.no_arg_cell = no_arg_cell
        self.offset = offset
        self.is_param = is_param
        self.no_var = no_var
        self.arg_type_list = []

    def __str__(self):
        return f'lexeme: {self.lexeme}, isKeyword: {self.is_keyword}, address: {self.address}, offset: {self.offset}, ' \
               f'type: {self.type}, var_arr_func: {self.var_arr_func}, no_arg_cell: {self.no_arg_cell}, ' \
               f'no_var: {self.no_var} ' \
               f'scope: {self.scope} ' \
               f'arg_type_list: {self.arg_type_list}'
