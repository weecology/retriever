"""DBTK Excel Functions

This module contains optional functions for importing data from Excel.

"""

import xlrd

class Excel():
    def empty_cell(self, cell):
        """Tests whether an excel cell is empty or contains only
        whitespace"""
        if cell.ctype == 0:
            return True
        if str(cell.value).strip() == "":
            return True
        return False
    
    def cell_value(self, cell):
        """Returns the string value of an excel spreadsheet cell"""
        return str(cell.value).strip()