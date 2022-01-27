from SymbolTable import SymbolTable


class CodeGen:
    def __init__(self):
        self.ss = []  # semantic stack
        self.program_block = []
        self.i = 0  # Counter for program block list
        self.static_data_pointer = 1000
        self.temp_data_pointer = 2000
        self.scope = 0
        self.program_block_file = open("output.txt", "w")

    def code_gen(self, action_symbol, token):
        if action_symbol == "#push_type":
            self.push_type(token)
        elif action_symbol == '#push_id':
            self.push_id(token)
        elif action_symbol == '#decl_id':
            self.decl_id(token)
        elif action_symbol == '#end_decl_var':
            self.end_decl_var()
        elif action_symbol == '#push_num':
            self.push_num(token)
        elif action_symbol == '#end_decl_arr':
            self.end_decl_arr()
        elif action_symbol == '#inc_scope':
            self.inc_scope()
        elif action_symbol == '#dec_scope':
            self.dec_scope()
        elif action_symbol == '#direct_assign':
            self.direct_assign()
        elif action_symbol == '#push_op':
            self.push_op(token)
        elif action_symbol == '#operate':
            self.operate()

        else:
            pass

    def push_type(self, token):
        self.ss.append(token[0])

    def decl_id(self, token):
        self.ss.append(token[0])

    def push_id(self, token):
        self.ss.append(SymbolTable.find_address(token[0]))

    def end_decl_var(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        #   TODO : handle 'void type' semantic error.

        address = self.allocate_static_data(4)

        SymbolTable.declare_variable(lexeme, address, type_arg, self.scope)

        self.ss_pop(2)

    def allocate_static_data(self, byte):
        self.static_data_pointer += byte
        return self.static_data_pointer - byte

    def allocate_temp_variable(self, byte = 4):
        self.temp_data_pointer += byte
        return self.temp_data_pointer - byte

    def ss_pop(self, count=1):
        for i in range(count):
            self.ss.pop()

    def push_num(self, token):
        self.ss.append('#' + token[0])

    def end_decl_arr(self):
        no_arg_cell = int(self.ss[-1][1:])  # convert (#100, string) to (100, int)
        lexeme = self.ss[-2]
        type_arg = self.ss[-3]

        address = self.allocate_static_data(4 * no_arg_cell)

        #   TODO : handle 'void type' semantic error.

        SymbolTable.declare_variable(lexeme, address, type_arg, self.scope, no_arg_cell=no_arg_cell)

        self.ss_pop(3)

    def inc_scope(self):
        self.scope += 1

    def dec_scope(self):
        self.scope -= 1

    def direct_assign(self):
        self.program_block.append(['ASSIGN', self.ss[-1], self.ss[-2], ''])
        self.i += 1
        self.ss_pop(2)

    def flush_program_block(self):

        print("number of codes generated = ", self.i)

        if len(self.program_block) == 0:
            self.program_block_file.write("The code has not been generated.")

        for i in range(len(self.program_block)):
            code = self.program_block[i]
            self.program_block_file.write(f"{i}\t({code[0]}, {code[1]}, {code[2]}, {code[3]})\n")

        self.program_block_file.close()

    def push_op(self, token):
        self.ss.append(token[0])

    def operate(self):
        t = self.allocate_temp_variable()

        if self.ss[-2] == '+':
            self.program_block.append(['ADD', self.ss[-3], self.ss[-1], t])
        elif self.ss[-2] == '-':
            self.program_block.append(['SUB', self.ss[-3], self.ss[-1], t])
        elif self.ss[-2] == '*':
            self.program_block.append(['MULT', self.ss[-3], self.ss[-1], t])
        elif self.ss[-2] == '<':
            self.program_block.append(['LT', self.ss[-3], self.ss[-1], t])
        elif self.ss[-2] == '==':
            self.program_block.append(['EQ', self.ss[-3], self.ss[-1], t])


        self.i += 1
        self.ss_pop(3)
        self.ss.append(t)

