from Code import *
from Parser import *
from SymbolTable import *
import sys
import re


# return true if the string express variable (rather then a number)
def is_variable(string):
    return re.search('[a-zA-Z]', string)

# Start translate the .asm file to .hack file
file_name = sys.argv[1]
# Open the .hack file
file_hack = open(file_name[:-4] + '.hack', 'w')
parser = Parser(file_name)
symbol_table = SymbolTable()
code = Code()
sum_hack_lines = 0
# Filter all symbols from the file
while parser.has_more_commands():
    parser.advance()
    if parser.command_type() == 'L_COMMAND':
        symbol_to_add = parser.symbol()
        symbol_table.add_entry(symbol_to_add, sum_hack_lines)
        sum_hack_lines -= 1
    sum_hack_lines += 1
parser.restart_reading()

# Begins to perform the translation for each command line
next_in_ram = 16
while parser.has_more_commands():
    parser.advance()
    command_in_bin = ''
    if parser.command_type() == 'A_COMMAND':
        a_command_symbol = parser.symbol()
        a_command_symbol = a_command_symbol.replace(' ', '')
        value = ''
        if is_variable(a_command_symbol):
            if symbol_table.contains(a_command_symbol):
                value = symbol_table.get_address(a_command_symbol)
            else:
                symbol_table.add_entry(a_command_symbol, next_in_ram)
                value = next_in_ram
                next_in_ram += 1
        else:
            value = a_command_symbol
        command_in_bin = format(int(value), 'b').zfill(16) + '\n'
        # value_in_bin_as_str = str(bin(int(value)))[2:]
        # command_in_bin = [0 for i in range(16 - len(value_in_bin_as_str))] + value_in_bin_as_str + '\n'
    elif parser.command_type() == 'C_COMMAND':
        c = parser.comp()
        d = parser.dest()
        j = parser.jump()
        cc = code.comp(c)
        dd = code.dest(d)
        jj = code.jump(j)
        command_in_bin = '111' + cc + dd + jj + '\n'
    file_hack.write(command_in_bin)
file_hack.close()
