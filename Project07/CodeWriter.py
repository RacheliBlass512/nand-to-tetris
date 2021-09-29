# translate vm command to asm command and write it to asm file
class CodeWriter:
    # constructor
    def __init__(self, file_name):
        self.file_name = file_name.split('/')[-1][:-4]
        self.file_asm = open(file_name, 'w')
        self.sum_labels = 0

    # translate arithmetic command to asm
    def write_arithmetic(self, command):
        if command == 'add':
            self.file_asm.write('@0\nA=M-1\nD=M\n@0\nM=M-1\n@0\nA=M-1\nM=M+D\n\n')
        elif command == 'sub':
            self.file_asm.write('@0\nA=M-1\nD=M\n@0\nM=M-1\n@0\nA=M-1\nM=M-D\n\n')
        elif command == 'neg':
            self.file_asm.write('@0\nA=M-1\nM=-M\n\n')
        elif command == 'eq':
            self.write_bool_command('EQ')
        elif command == 'gt':
            self.write_bool_command('GT')
        elif command == 'lt':
            self.write_bool_command('LT')
        elif command == 'and':
            self.file_asm.write('@0\nA=M-1\nD=M\n@0\nM=M-1\n@0\nA=M-1\nM=D&M\n\n')
        elif command == 'or':
            self.file_asm.write('@0\nA=M-1\nD=M\n@0\nM=M-1\n@0\nA=M-1\nM=D|M\n\n')
        elif command == 'not':
            self.file_asm.write('@0\n'
                                'A=M-1 //A=RAM[0]-1\n'
                                'M=!M //D=RAM[A]\n\n')

    # translate push, pop commands to asm according to the segment
    def write_push_pop(self, command, segment, index):
        asm_code = '// ' + command + ' ' + segment + ' ' + index + '\n'
        type_segment1 = ['local', 'argument', 'this', 'that']
        if segment in type_segment1:
            base_adrr_ptr = type_segment1.index(segment) + 1
            asm_code += '@' + str(base_adrr_ptr) + '\n'
            asm_code += 'D=M\n'
            asm_code += '@' + index + '\n'
            if command == 'C_PUSH':
                asm_code += 'D=D+A //D=num to push to the stack\n' \
                            'A=D\n' \
                            'D=M\n' \
                            '@0\n' \
                            'A=M //A=RAM[0]\n' \
                            'M=D  //RAM[A]=D\n' \
                            '@0\n' \
                            'M=M+1 //RAM[0]+=1\n'
            elif command == 'C_POP':
                asm_code += 'D=D+A //D= index to pop to\n' \
                            '@13\n' \
                            'M=D //RAM[13] =  index to pop to\n' \
                            '@0\n' \
                            'M=M-1 //RAM[0]--\n' \
                            'A=M //A=RAM[0], the top of the stack\n' \
                            'D=M //D=RAM[A] , the value of the top of the stack\n' \
                            '@13\n' \
                            'A=M // A=INDEX TO POP TO\n' \
                            'M=D\n'
        elif segment == 'constant':
            if command == 'C_PUSH':
                asm_code += '@' + index + '\n'
                asm_code += 'D=A //D= num to push\n' \
                            '@0\n' \
                            'A=M\n' \
                            'M=D //RAM[SP]=D\n' \
                            '@0\n' \
                            'M=M+1\n'
        elif segment == 'static':
            if command == 'C_PUSH':
                asm_code += '@' + self.file_name + '.' + str(index) + '\n'
                asm_code += 'D=M //D=num to push\n' \
                            '@0\n' \
                            'A=M //A= top of the stack\n' \
                            'M=D\n' \
                            '@0\n' \
                            'M=M+1\n'
            elif command == 'C_POP':
                asm_code += '@0\n' \
                            'M=M-1 //RAM[0]--\n' \
                            'A=M //A=RAM[0], the top of the stack\n' \
                            'D=M //D=RAM[A] , the value of the top of the stack\n'
                asm_code += '@' + self.file_name + '.' + str(index) + '\n'
                asm_code += 'M=D\n'
        elif segment == 'temp':
            if command == 'C_PUSH':
                asm_code += '@' + str(int(index) + 5) + '\n'
                asm_code += 'D=M //D=num tp push\n' \
                            '@0\n' \
                            'A=M\n' \
                            'M=D\n' \
                            '@0\n' \
                            'M=M+1\n'
            elif command == 'C_POP':
                asm_code += '@0\n' \
                            'M=M-1 //RAM[0]--\n' \
                            'A=M //A=RAM[0], the top of the stack\n' \
                            'D=M //D=RAM[A] , the value of the top of the stack\n'
                asm_code += '@' + str(int(index) + 5) + '\n'
                asm_code += 'M=D\n'
        elif segment == 'pointer':
            base_adrr_ptr = 3
            if command == 'C_PUSH':
                asm_code += '@' + str(base_adrr_ptr + int(index)) + '\n'
                asm_code += 'D=M\n' \
                            '@0\n' \
                            'A=M\n' \
                            'M=D\n' \
                            '@0\n' \
                            'M=M+1\n'
            elif command == 'C_POP':
                asm_code += '@0\n' \
                            'M=M-1 //RAM[0]--\n' \
                            'A=M //A=RAM[0], the top of the stack\n' \
                            'D=M //D=RAM[A] , the value of the top of the stack\n'
                asm_code += '@' + str(base_adrr_ptr + int(index)) + '\n'
                asm_code += 'M=D\n'
        self.file_asm.write(asm_code)

    def close(self):
        self.file_asm.close()

    # translate eq, lt, gt arithmetic commands to asm
    def write_bool_command(self, type):
        asm_code = '@0\n' \
                   'A=M-1\n' \
                   'D=M\n' \
                   '@0\n' \
                   'M=M-1\n' \
                   '@0\n' \
                   'A=M-1\n' \
                   'D=M-D\n'
        label = type + str(self.sum_labels)
        asm_code += '@' + label + '\n'
        asm_code += 'D;J' + type + '\n' \
                                   '@0\n' \
                                   'A=M-1\n' \
                                   'M=0\n'
        cont_lable = 'CONT_' + type + str(self.sum_labels)
        asm_code += '@' + cont_lable + '\n'
        asm_code += 'D;JMP\n'
        asm_code += '(' + label + ')\n'
        asm_code += '@0\n' \
                    'A=M-1\n' \
                    'M=-1\n'
        asm_code += '(' + cont_lable + ')\n\n'
        self.file_asm.write(asm_code)
        self.sum_labels += 1
