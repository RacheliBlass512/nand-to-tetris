# gets a command with comments and return command without comments
def remove_comments(command):
    head, sep, tail = command.partition('/')
    head, sep, tail = head.partition('\n')
    return head


class Parser:
    # constructor
    def __init__(self, file):
        file_vm = open(file)
        self.file_lines = file_vm.readlines()
        self.curr_line = 0
        self.next_command = ''

    # boolean function, return True if there is more commands to parse in the vm file
    def has_more_commands(self):
        if len(self.file_lines) > self.curr_line:
            return True
        return False

    # set next command to be the next line and ignores whitespace
    def advance(self):
        if self.has_more_commands():
            self.next_command = ''
            while self.next_command == '':
                self.next_command = self.file_lines[self.curr_line]
                self.curr_line += 1
                self.next_command = remove_comments(self.next_command)

    # return the type of the next command
    def command_type(self):
        if self.next_command.split(' ')[0] == 'push':
            return 'C_PUSH'
        if self.next_command.split(' ')[0] == 'pop':
            return 'C_POP'
        return 'C_ARITHMETIC'

    # if the next command is C_ARITHMETIC return the first arg in the command: add, sub etc.
    # and if the next command is C_PUSH or C_POP return the second arg in the command: constant, local etc.
    def arg1(self):
        if self.command_type()=='C_ARITHMETIC':
            return self.next_command.split(' ')[0]
        else:
            return self.next_command.split(' ')[1]

    # occurs only if the next command is C_PUSH or C_POP
    # return the third arg in the command, the index
    def arg2(self):
        if self.command_type() == 'C_PUSH' or self.command_type() == 'C_POP':
            return self.next_command.split(' ')[2]
        return None