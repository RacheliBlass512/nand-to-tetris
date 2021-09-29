class SymbolTable:
    def __init__(self):
        self.symbol_table = {
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7
            , 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13,
            'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576, 'SP': 0,
            'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4
        }

    def add_entry(self, symbol, entry):
        """
        Add new Symbol to symbol table
        :param symbol: the new symbol to add
        :param entry: the address of the new symbol
        """
        if not (self.contains(symbol)):
            self.symbol_table[symbol] = entry

    def contains(self, symbol):
        """
        Check if the symbol that given is exist in the symbol table.
        :param symbol: the symbol to find
        :return: True - if the symbol exist, False - otherwise
        """
        return symbol in self.symbol_table

    def get_address(self, symbol):
        """
        Get the address of symbol that exists in the symbol table
        :param symbol: symbol to find
        :return: the address of the given symbol
        """
        return self.symbol_table.get(symbol)