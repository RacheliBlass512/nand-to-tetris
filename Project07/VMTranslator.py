from CodeWriter import *
from Parser import *
import sys

file_name = sys.argv[1]
# create Parser object
parser = Parser(file_name)
# create CodeWriter object
code_writer = CodeWriter(file_name[:-3] + '.asm')
# while there is more commands to parse in the file parse it and write the asm translation
while parser.has_more_commands():
    parser.advance()
    command_type = parser.command_type()
    if command_type == 'C_ARITHMETIC':
        code_writer.write_arithmetic(parser.arg1())
    elif command_type == 'C_PUSH' or command_type == 'C_POP':
        code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
code_writer.close()
