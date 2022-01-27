from SymbolTable import SymbolTable


class CodeGen:
    def __init__(self):
        self.ss = []  # semantic stack
        self.program_block = []
        self.i = 0  # Counter for program block list
        self.static_data_pointer = 1000

    def code_gen(self, action_symbol, token):
        if action_symbol == "#type_id":
            self.type_id(token)
        elif action_symbol == '#decl_id':
            self.decl_id(token)
        elif action_symbol == '#end_decl_var':
            self.end_decl_var()
        else:
            pass

    def type_id(self, token):
        self.ss.append(token[0])

    def decl_id(self, token):
        self.ss.append(token[0])

    def end_decl_var(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        ###########################################################################################
        #   TODO : handle 'void type' semantic error.
        ###########################################################################################

        address = self.allocate_static_data(4)

        SymbolTable.declare_variable(lexeme, address, type_arg)

        self.ss_pop(2)

    def allocate_static_data(self, byte):
        self.static_data_pointer += byte
        return self.static_data_pointer - byte

    def ss_pop(self, count=1):
        for i in range(count):
            self.ss.pop()
