"""Database Toolkit Excel Functions

This module contains optional functions for importing data from Excel.

"""

class Excel:
    @staticmethod
    def empty_cell(cell):
        """Tests whether an excel cell is empty or contains only
        whitespace"""
        if cell.ctype == 0:
            return True
        if str(cell.value).strip() == "":
            return True
        return False
    @staticmethod
    def cell_value(cell):
        """Returns the string value of an excel spreadsheet cell"""
        return str(cell.value).strip()
