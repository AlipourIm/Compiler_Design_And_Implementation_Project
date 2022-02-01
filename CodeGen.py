from SymbolTable import SymbolTable


class CodeGen:
    def __init__(self):
        self.ss = []  # semantic stack
        self.program_block = []
        self.i = 0  # Counter for program block list
        self.top_sp = 100
        self.static_data_pointer = 504
        self.temp_data_pointer = 3000
        self.scope = 0
        self.program_block_file = open("output.txt", "w")
        self.break_stack = []  # A stack for loop breaks to be back-patched consists of pairs of break_line and loop
        # number for each instance
        self.loop_counter = 0  # A counter for loops that has not been finished yet.
        self.offset_pointer = 0

    def code_gen(self, action_symbol, token):

        print(self.ss)

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
        elif action_symbol == '#assign':
            self.assign()
        elif action_symbol == '#indirect_addr':
            self.indirect_addr()
        elif action_symbol == '#push_op':
            self.push_op(token)
        elif action_symbol == '#operate':
            self.operate()
        elif action_symbol == '#pop_exp':
            self.pop_exp()
        elif action_symbol == '#label':
            self.label()
        elif action_symbol == '#repeat_jump':
            self.repeat_jump()
        elif action_symbol == '#save_label':
            self.save_label()
        elif action_symbol == '#if_jpf':
            self.if_jpf()
        elif action_symbol == '#if_jpf_save_label':
            self.if_jpf_save_label()
        elif action_symbol == '#then_jp':
            self.then_jp()
        elif action_symbol == '#inc_loop_cnt':
            self.inc_loop_cnt()
        elif action_symbol == '#save_break':
            self.save_break()
        elif action_symbol == '#end_var_param':
            self.end_var_param()
        elif action_symbol == '#end_arr_param':
            self.end_arr_param()
        elif action_symbol == '#end_decl_fun':
            self.end_decl_fun()
        elif action_symbol == '#start_decl_fun':
            self.start_decl_fun()


        else:
            print(self.ss)

    def push_type(self, token):
        self.ss.append(token[0])

    def decl_id(self, token):
        self.ss.append(token[0])

    def push_id(self, token):
        lexeme = token[0]
        if SymbolTable.is_global(lexeme):
            self.ss.append(SymbolTable.find_address(lexeme))
        else:
            offset = SymbolTable.find_offset(lexeme)
            self.ss.append('!' + str(SymbolTable.find_offset(lexeme)))

    def end_decl_var(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]
        self.ss_pop(2)

        #   TODO : handle 'void type' semantic error.

        # if in the global scope, set a direct address for variable
        if self.scope == 0:
            address = self.allocate_static_data(4)
            SymbolTable.declare_global_variable(lexeme, address, type_arg, self.scope)

            # push the address for upcoming assign to zero
            self.ss.append(address)

        # if in the function scope, set an offset for local variable
        else:
            offset = self.allocate_local_data(4)
            SymbolTable.declare_local_variable(lexeme, offset, type_arg, self.scope)

            # push the offset for upcoming assign to zero
            self.ss.append('!' + str(offset))

        self.ss.append('#0')
        self.assign()
        self.ss_pop(1)

    def end_decl_arr(self):
        no_arg_cell = int(self.ss[-1][1:])  # convert (#100, string) to (100, int)
        lexeme = self.ss[-2]
        type_arg = self.ss[-3]
        self.ss_pop(3)

        #   TODO : handle 'void type' semantic error.

        if self.scope == 0:
            address = self.allocate_static_data(4 * (1 + no_arg_cell))
            SymbolTable.declare_global_variable(lexeme, address, type_arg, self.scope, no_arg_cell=no_arg_cell)

            # ASSIGN address of first cell of array (address + 4) in the pointer of array (address)
            self.program_block.append(['ASSIGN', '#' + str(address + 4), address, ''])
            self.i += 1
            # ASSIGN 0 to all elements of the new declared array
            for cell in range(no_arg_cell):
                self.ss.append(4 * cell + 4 + address)
                self.ss.append('#0')
                self.assign()
                self.ss_pop(1)

        else:
            offset = self.allocate_local_data(4 * (1 + no_arg_cell))
            SymbolTable.declare_local_variable(lexeme, offset, type_arg, self.scope, no_arg_cell=no_arg_cell)

            # ASSIGN offset of first cell of array (address + 4) in the pointer of array (address)
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(4 + offset), t1])
            self.i += 1
            rhs = str(t1)

            self.ss.append('!' + str(offset))
            self.ss.append(rhs)
            self.assign()
            self.ss_pop(1)

            # ASSIGN 0 to all elements of the new declared array
            for cell in range(no_arg_cell):
                self.ss.append('!' + str(4 * cell + 4 + offset))
                self.ss.append('#0')
                self.assign()
                self.ss_pop(1)

    def allocate_static_data(self, byte):
        self.static_data_pointer += byte
        return self.static_data_pointer - byte

    def allocate_temp_variable(self, byte=4):
        self.temp_data_pointer += byte
        return self.temp_data_pointer - byte

    def allocate_local_data(self, byte=4):
        self.offset_pointer += byte
        return self.offset_pointer - byte

    def ss_pop(self, count=1):
        for i in range(count):
            self.ss.pop()

    def push_num(self, token):
        self.ss.append('#' + token[0])

    def inc_scope(self):
        self.scope += 1
        self.offset_pointer = 0

    def dec_scope(self):
        self.scope -= 1

    def assign(self):
        rhs = self.ss[-1]
        lhs = self.ss[-2]

        if str(rhs)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(rhs)[1:], t1])
            self.i += 1
            rhs = '@' + str(t1)

        if str(lhs)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(lhs)[1:], t1])
            self.i += 1
            lhs = '@' + str(t1)

        self.program_block.append(['ASSIGN', rhs, lhs, ''])
        self.i += 1
        self.ss_pop(1)

    def indirect_addr(self):
        index = self.ss[-1]
        array_pointer = self.ss[-2]
        self.ss_pop(2)

        self.ss.append('#4')
        self.ss.append('*')
        self.ss.append(index)
        self.operate()

        self.ss.append('+')
        self.ss.append(array_pointer)
        self.operate()

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
        rhs1 = self.ss[-3]
        rhs2 = self.ss[-1]

        if str(rhs1)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(rhs1)[1:], t1])
            self.i += 1
            rhs1 = '@' + str(t1)

        if str(rhs2)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(rhs2)[1:], t1])
            self.i += 1
            rhs2 = '@' + str(t1)

        lhs_offset = self.allocate_local_data(4)
        lhs = self.allocate_temp_variable()
        self.program_block.append(['ADD', self.top_sp, '#' + str(lhs_offset), lhs])
        self.i += 1
        lhs = '@' + str(lhs)

        if self.ss[-2] == '+':
            self.program_block.append(['ADD', rhs1, rhs2, lhs])
        elif self.ss[-2] == '-':
            self.program_block.append(['SUB', rhs1, rhs2, lhs])
        elif self.ss[-2] == '*':
            self.program_block.append(['MULT', rhs1, rhs2, lhs])
        elif self.ss[-2] == '<':
            self.program_block.append(['LT', rhs1, rhs2, lhs])
        elif self.ss[-2] == '==':
            self.program_block.append(['EQ', rhs1, rhs2, lhs])

        self.i += 1
        self.ss_pop(3)
        self.ss.append('!' + str(lhs_offset))

    def pop_exp(self):
        # TODO : what if the result of expression is void? like output(p)
        self.ss_pop(1)

    def label(self):
        self.ss.append(self.i)

    def repeat_jump(self):
        # First, complete conditional jump
        self.program_block.append(['JPF', self.ss[-1], self.ss[-2], ''])
        self.i += 1
        self.ss_pop(2)

        # Then, handle break statements
        while len(self.break_stack) != 0 and self.break_stack[-1][1] == self.loop_counter:
            last_item = self.break_stack.pop()
            self.program_block[last_item[0]] = ['JP', self.i, '', '']
        self.loop_counter -= 1

    def save_label(self):
        self.program_block.append(['JPF', 'condition', '?', ''])
        self.ss.append(self.i)
        self.i += 1

    def if_jpf(self):
        self.program_block[self.ss[-1]] = ['JPF', self.ss[-2], self.i, '']
        self.ss_pop(2)

    def if_jpf_save_label(self):

        self.program_block[self.ss[-1]] = ['JPF', self.ss[-2], self.i + 1, '']
        self.ss_pop(2)

        self.program_block.append(['JP', '?', '', ''])
        self.ss.append(self.i)
        self.i += 1

    def then_jp(self):
        self.program_block[self.ss[-1]] = ['JP', self.i, '', '']
        self.ss_pop(1)

    def inc_loop_cnt(self):
        self.loop_counter += 1

    def save_break(self):
        #   TODO: handle a semantic error for when there is no loop to be braked
        self.program_block.append(['JP', '?', '', ''])
        self.break_stack.append([self.i, self.loop_counter])
        self.i += 1

    def end_var_param(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        #   TODO : handle 'void type' semantic error.

        offset = self.allocate_local_data(4)

        SymbolTable.declare_param_variable(lexeme, offset, type_arg, self.scope)

        self.ss_pop(2)

    def end_arr_param(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        #   TODO : handle 'void type' semantic error.

        offset = self.allocate_local_data(4)

        SymbolTable.declare_param_variable(lexeme, offset, type_arg, self.scope, -1)

        self.ss_pop(2)

    def end_decl_fun(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        SymbolTable.declare_function(lexeme, type_arg)

        self.ss_pop(2)

    def start_decl_fun(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]

        SymbolTable.add_symbol(lexeme)
