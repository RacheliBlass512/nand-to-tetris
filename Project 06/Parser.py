def remove_comments(command):
    head, sep, tail = command.partition('/')
    head, sep, tail = head.partition('\n')
    without_whitespace = head.replace(' ', '')
    return without_whitespace


class Parser:

    def __init__(self, file):
        file_asm = open(file)
        self.file_lines = file_asm.readlines()
        self.curr_line = 0
        self.next_command = ''

    def has_more_commands(self):
        """
        Checks for additional unread lines.
        :return: True - if there are more lines, False - otherwise
        """
        if len(self.file_lines) > self.curr_line:
            return True
        return False

    def advance(self):
        """
        Read the next line that contains a command into the variable 'self.next_command'
        """
        if self.has_more_commands():
            self.next_command = ''
            while self.next_command == '':
                self.next_command = self.file_lines[self.curr_line]
                self.curr_line += 1
                self.next_command = remove_comments(self.next_command)

    def command_type(self):
        """
        Check the type of the current command.
        :return: 'A_COMMAND' - for command that start with @, 'L_COMMAND' - for labels, 'L_COMMAND' - for standard command
        """
        if '@' in self.next_command:
            return 'A_COMMAND'
        if self.next_command[0] == '(':
            return 'L_COMMAND'
        return 'C_COMMAND'

    def symbol(self):
        """
        Extracts the command without the @ for 'A_COMMAND' command
        Returns the command unchanged for an 'A_COMMAND' command
        :return: the command as string.
        """
        if self.command_type() == 'A_COMMAND':
            return self.next_command.split('@')[1]
        if self.command_type() == 'L_COMMAND':
            return self.next_command.split('(')[1][:-1]

    def dest(self):
        """
        Extracts the part of the dest command from the line
        :return: the dest command as string
        """
        if self.command_type() == 'C_COMMAND':
            if '=' in self.next_command:
                return self.next_command.split('=')[0]
            return ''

    def comp(self):
        """
        Extracts the part of the comp command from the line
        :return: the comp command as string
        """
        if self.command_type() == 'C_COMMAND':
            if '=' in self.next_command:
                second_part = self.next_command.split('=')[1]
                second_part_only = second_part.split(';')[0]
                return second_part_only
            else:
                return self.next_command.split(';')[0]

    def jump(self):
        """
        Extracts the part of the jump command from the line
        :return: the jump command as string
        """
        if self.command_type() == 'C_COMMAND':
            if ';' in self.next_command:
                return self.next_command.split(';')[1]
        return ''

    def restart_reading(self):
        self.curr_line = 0
        self.next_command = ''
