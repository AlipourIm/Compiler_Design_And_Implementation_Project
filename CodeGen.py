from ErrorHandler import ErrorHandler
from SymbolTable import SymbolTable


class CodeGen:
    def __init__(self):
        self.ss = []  # semantic stack
        self.program_block = []
        self.i = 0  # Counter for program block list
        self.top_sp = 5000
        self.return_jump = 5004
        self.static_data_pointer = 5008
        self.temp_data_pointer = 30000
        self.scope = 0
        self.line = 0
        self.program_block_file = open("output.txt", "w")
        self.break_stack = []  # A stack for loop breaks to be back-patched consists of pairs of break_line and loop
        # number for each instance
        self.loop_counter = 0  # A counter for loops that has not been finished yet.
        self.offset_pointer = 0
        self.current_func_lexeme = None
        self.program_block.append(['ASSIGN', '#' + str(40000), self.top_sp, ''])
        self.i += 1

    def code_gen(self, action_symbol, token, line):
        self.line = line
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
        elif action_symbol == '#jump_over_func':
            self.jump_over_func()
        elif action_symbol == '#start_decl_fun':
            self.start_decl_fun()
        elif action_symbol == '#end_decl_func':
            self.end_decl_func()
        elif action_symbol == '#call_func':
            self.call_func()
        elif action_symbol == '#return_void':
            self.return_void()
        elif action_symbol == '#return_exp':
            self.return_exp()
        elif action_symbol == '#jp_main':
            self.jp_main()
        elif action_symbol == '#assign_to_local':
            self.assign_to_local()

    def push_type(self, token):
        self.ss.append(token[0])

    def decl_id(self, token):
        self.ss.append(token[0])

    def push_id(self, token):
        lexeme = token[0]
        if not SymbolTable.exists(lexeme):
            ErrorHandler.catch_semantic_error(self.line, f"Semantic Error! '{lexeme}' is not defined.")
            self.ss.append([None, None, None])
            return

        if SymbolTable.is_function(lexeme):
            self.ss.append(SymbolTable.find_function(lexeme))
        else:
            if SymbolTable.is_global(lexeme):
                self.ss.append(SymbolTable.find_address(lexeme))
            else:
                self.ss.append(SymbolTable.find_offset(lexeme))

    def end_decl_var(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]
        self.ss_pop(2)

        if type_arg == 'void':
            ErrorHandler.catch_semantic_error(self.line, f"Semantic Error! Illegal type of void for '{lexeme}'.")
            return

        # if in the global scope, set a direct address for variable
        if self.scope == 0:
            address = self.allocate_static_data(4)
            SymbolTable.declare_global_variable(lexeme, address, type_arg, self.scope)

            # push the address for upcoming assign to zero
            self.ss.append([address, type_arg, 'var'])

        # if in the function scope, set an offset for local variable
        else:
            offset = self.allocate_local_data(4)
            SymbolTable.declare_local_variable(lexeme, offset, type_arg, self.scope)

            # push the offset for upcoming assign to zero
            self.ss.append(['!' + str(offset), type_arg, 'var'])

        self.ss.append(['#0', 'int', 'var'])
        self.assign()
        self.ss_pop(1)

    def end_decl_arr(self):
        no_arg_cell = int(self.ss[-1][0][1:])  # convert (#123, string) to (123, int)
        lexeme = self.ss[-2]
        type_arg = self.ss[-3]
        self.ss_pop(3)

        if type_arg == 'void':
            ErrorHandler.catch_semantic_error(self.line, f"Semantic Error! Illegal type of void for '{lexeme}'.")
            return

        if self.scope == 0:
            address = self.allocate_static_data(4 * (1 + no_arg_cell))
            SymbolTable.declare_global_variable(lexeme, address, type_arg, self.scope, no_arg_cell=no_arg_cell)

            # ASSIGN address of first cell of array (address + 4) in the pointer of array (address)
            self.program_block.append(['ASSIGN', '#' + str(address + 4), address, ''])
            self.i += 1
            # ASSIGN 0 to all elements of the new declared array
            for cell in range(no_arg_cell):
                self.ss.append([4 * cell + 4 + address, type_arg, 'var'])
                self.ss.append(['#0', 'int', 'var'])
                self.assign()
                self.ss_pop(1)

        else:
            offset = self.allocate_local_data(4 * (1 + no_arg_cell))
            SymbolTable.declare_local_variable(lexeme, offset, type_arg, self.scope, no_arg_cell=no_arg_cell)

            # ASSIGN offset of first cell of array (address + 4) in the pointer of array (address)
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(4 + offset), t1])
            self.i += 1
            rhs = [str(t1), 'int', 'var']

            self.ss.append(['!' + str(offset), 'int', 'var'])
            self.ss.append(rhs)
            self.assign()
            self.ss_pop(1)

            # ASSIGN 0 to all elements of the new declared array
            for cell in range(no_arg_cell):
                self.ss.append(['!' + str(4 * cell + 4 + offset), 'int', 'var'])
                self.ss.append(['#0', 'int', 'var'])
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
        self.ss.append(['#' + token[0], 'int', 'var'])

    def inc_scope(self):
        self.scope += 1
        self.offset_pointer = 12

    def dec_scope(self):
        self.scope -= 1

    def assign(self):
        rhs = self.ss[-1]
        lhs = self.ss[-2]

        rhs[0] = self.offset_to_temp(rhs[0])

        lhs[0] = self.offset_to_temp(lhs[0])

        self.program_block.append(['ASSIGN', rhs[0], lhs[0], ''])
        self.i += 1
        self.ss_pop(1)

    def indirect_addr(self):
        index = self.ss[-1]
        array_pointer = self.ss[-2]
        self.ss_pop(2)

        self.ss.append(['#4', 'int', 'var'])
        self.ss.append('*')
        self.ss.append(index)
        self.operate()

        self.ss.append('+')
        self.ss.append([array_pointer[0], 'int', 'var'])
        self.operate()

        self.ss[-1][0] = '@' + str(self.ss[-1][0])

    def flush_program_block(self):

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
        operator = self.ss[-2]
        rhs2 = self.ss[-1]
        self.ss_pop(3)

        if rhs1 == [None, None, None] or rhs2 == [None, None, None]:
            self.ss.append([None, None, None])
            return

        # innovative semantic error in case of operating int with void
        if rhs1[1] != rhs2[1]:
            ErrorHandler.catch_semantic_error(self.line,
                                              f"Semantic Error! Type mismatch in operands, Got void instead of int.")
            self.ss.append([None, None, None])
            return

        # semantic error in case of operating array with var (supposing int)
        if rhs1[2] != rhs2[2]:
            ErrorHandler.catch_semantic_error(self.line,
                                              f"Semantic Error! Type mismatch in operands, Got array instead of int.")
            self.ss.append([None, None, None])
            return

        rhs1[0] = self.offset_to_temp(rhs1[0])
        rhs2[0] = self.offset_to_temp(rhs2[0])

        lhs_offset = self.allocate_local_data(4)
        lhs = [self.allocate_temp_variable(), rhs1[1], rhs1[2]]
        self.program_block.append(['ADD', self.top_sp, '#' + str(lhs_offset), lhs[0]])
        self.i += 1
        lhs[0] = '@' + str(lhs[0])

        if operator == '+':
            self.program_block.append(['ADD', rhs1[0], rhs2[0], lhs[0]])
        elif operator == '-':
            self.program_block.append(['SUB', rhs1[0], rhs2[0], lhs[0]])
        elif operator == '*':
            self.program_block.append(['MULT', rhs1[0], rhs2[0], lhs[0]])
        elif operator == '<':
            self.program_block.append(['LT', rhs1[0], rhs2[0], lhs[0]])
        elif operator == '==':
            self.program_block.append(['EQ', rhs1[0], rhs2[0], lhs[0]])

        self.i += 1
        self.ss.append(['!' + str(lhs_offset), lhs[1], lhs[2]])

    def pop_exp(self):
        self.ss_pop(1)

    def label(self):
        self.ss.append(self.i)

    def repeat_jump(self):
        # First, complete conditional jump
        condition = self.ss[-1][0]
        condition = self.offset_to_temp(condition)
        self.program_block.append(['JPF', condition, self.ss[-2], ''])
        self.i += 1
        self.ss_pop(2)

        # Then, handle break statements
        while len(self.break_stack) != 0 and self.break_stack[-1][1] == self.loop_counter:
            last_item = self.break_stack.pop()
            self.program_block[last_item[0]] = ['JP', self.i, '', '']
        self.loop_counter -= 1

    def save_label(self):
        self.program_block.append(['ADD', '?', '?', '?'])
        self.program_block.append(['JPF', 'condition', '?', ''])
        self.ss.append(self.i)
        self.i += 2

    def if_jpf(self):
        address = self.ss[-1]
        condition = self.ss[-2][0]

        condition = self.offset_to_temp_backpatching(condition, address)
        self.program_block[address + 1] = ['JPF', condition, self.i, '']
        self.ss_pop(2)

    def if_jpf_save_label(self):
        address = self.ss[-1]
        condition = self.ss[-2][0]

        condition = self.offset_to_temp_backpatching(condition, address)
        self.program_block[address + 1] = ['JPF', condition, self.i + 1, '']
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
        if self.loop_counter == 0:
            ErrorHandler.catch_semantic_error(self.line, "Semantic Error! No 'repeat ... until' found for 'break'.")
            return
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

    def start_decl_fun(self):
        type_arg = self.ss[-2]
        lexeme = self.ss[-1]
        self.current_func_lexeme = lexeme

        SymbolTable.add_symbol(lexeme)

        # reserve a jump from before of function to after of function
        self.program_block.append(['JP', '? jump to after of function', '', ''])
        self.i += 1

        # push the address for first line of function
        self.ss.append(self.i)

    def end_decl_func(self):
        type_arg = self.ss[-3]
        lexeme = self.ss[-2]
        address = self.ss[-1]

        SymbolTable.declare_function(lexeme, type_arg, address)

    def jump_over_func(self):
        type_arg = self.ss[-3]
        lexeme = self.ss[-2]
        address = self.ss[-1]

        self.ss_pop(3)
        SymbolTable.pop_function_locals(lexeme)

        # TODO : what if type_arg is int
        self.return_void()

        # back-patching, fill jump from before of function to after of function
        if lexeme == 'main':
            self.program_block[address - 1] = ['JP', address, '', '']
        else:
            self.program_block[address - 1] = ['JP', self.i, '', '']

    def call_func(self):
        # extract arguments from semantic stack.
        args = []
        while type(self.ss[-1]) != tuple:
            args.insert(0, self.ss[-1])
            self.ss_pop(1)
        arg_type_list, address, lexeme, return_type = self.ss[-1]
        self.ss_pop(1)

        # semantic check 'c' for mismatch in number of arguments
        if len(args) != len(arg_type_list):
            ErrorHandler.catch_semantic_error(self.line,
                                              f"Semantic Error! Mismatch in numbers of arguments of '{lexeme}'.")
            self.ss.append([None, return_type, 'var'])
            return

        #  semantic check 'f' for mismatch type in any argument
        for i in range(len(args)):
            if arg_type_list[i][1] == 'var' and args[i][2] == 'array':
                ErrorHandler.catch_semantic_error(self.line,
                                                  f"Semantic Error! Mismatch in type of argument {i + 1} of '{lexeme}'. Expected 'int' but got 'array' instead.")
                self.ss.append([None, return_type, 'var'])
                return
            if arg_type_list[i][1] == 'array' and args[i][2] == 'var':
                ErrorHandler.catch_semantic_error(self.line,
                                                  f"Semantic Error! Mismatch in type of argument {i + 1} of '{lexeme}'. Expected 'array' but got 'int' instead.")
                self.ss.append([None, return_type, 'var'])
                return

        # check if the function call is for print
        if address == -1:
            arg = args[0]

            arg[0] = self.offset_to_temp(arg[0])

            self.program_block.append(['PRINT', arg[0], '', ''])
            self.i += 1
            self.ss.append(['#0', 'void', 'var'])
            return

        # set callee's top_sp with next empty offset
        self.ss.append(['!' + str(4 + self.offset_pointer), 'int', 'var'])
        self.ss.append([self.top_sp, 'int', 'var'])
        self.assign()
        self.ss_pop(1)

        # assign arguments to callee's activation frame
        for counter in range(len(arg_type_list)):
            self.ss.append(['!' + str(12 + (4 * counter) + self.offset_pointer), 'int', 'var'])
            # TODO : semantic check parameter mismatch
            self.ss.append(args[counter])
            self.assign()
            self.ss_pop(1)

        # set callee's return address the line after JP to callee
        self.ss.append(['!' + str(8 + self.offset_pointer), 'int', 'var'])
        self.ss.append(['#' + str(self.i + 4), 'int', 'var'])
        self.assign()
        self.ss_pop(1)

        # update top_sp for callee's frame
        self.program_block.append(['ADD', self.top_sp, '#' + str(self.offset_pointer), self.top_sp, ''])
        self.i += 1

        # jump to callee
        self.program_block.append(['JP', str(address), '', ''])
        self.i += 1

        # push return value into semantic stack
        t1 = self.allocate_local_data(4)
        self.ss.append(['!' + str(t1), return_type, 'var'])

    def offset_to_temp(self, expression):
        if str(expression)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(expression)[1:], t1])
            self.i += 1
            expression = '@' + str(t1)
        elif len(str(expression)) > 1 and str(expression)[0:2] == '@!':
            t1 = self.allocate_temp_variable()
            self.program_block.append(['ADD', self.top_sp, '#' + str(expression)[2:], t1])
            self.i += 1
            self.program_block.append(['ASSIGN', '@' + str(t1), t1, ''])
            self.i += 1
            expression = '@' + str(t1)
        return expression

    def offset_to_temp_backpatching(self, expression, address):
        if str(expression)[0] == '!':
            t1 = self.allocate_temp_variable()
            self.program_block[address] = ['ADD', self.top_sp, '#' + str(expression)[1:], t1]
            expression = '@' + str(t1)
        else:
            self.program_block[address] = ['JP', address + 1, '', '']
        return expression

    def return_void(self):
        # put void return value at !0
        self.ss.append(['#0', 'void', 'var'])
        self.return_exp()

    def return_exp(self):
        if self.current_func_lexeme == 'main':
            self.ss_pop(1)
            return
        # put return value at !0(@top_sp)
        exp = self.ss[-1]
        self.ss_pop(1)
        self.ss.append(['@' + str(self.top_sp), exp[1], exp[2]])
        self.ss.append(exp)
        self.assign()
        self.ss_pop(1)

        # extract return address from !8
        self.program_block.append(['ADD', self.top_sp, '#' + str(8), self.return_jump])
        self.i += 1

        # restore top_sp from !4
        self.ss.append([self.top_sp, 'int', 'var'])
        self.ss.append(['!4', 'int', 'var'])
        self.assign()
        self.ss_pop(1)

        self.program_block.append(['ASSIGN', '@' + str(self.return_jump), self.return_jump, ''])
        self.i += 1

        # return to caller
        self.program_block.append(['JP', '@' + str(self.return_jump), '', ''])
        self.i += 1

    def jp_main(self):
        # _, address = SymbolTable.find_function('main')
        # self.program_block[1] = ['JP', address, '', '']
        pass

    def assign_to_local(self):
        expression = self.ss[-1]
        self.ss_pop(1)

        t1 = self.allocate_local_data(4)
        self.ss.append([t1, expression[1], expression[2]])
        self.ss.append(expression)
        self.assign()
