"""Data Retriever Excel Functions

This module contains optional functions for importing data from Excel.

"""
from builtins import object
from builtins import str


class Excel(object):
    @staticmethod
    def empty_cell(cell):
        """Test if excel cell is empty or contains only whitespace."""
        if cell.ctype == 0:
            return True
        if str(cell.value).strip() == "":
            return True
        return False

    @staticmethod
    def cell_value(cell):
        """Return string value of an excel spreadsheet cell."""
        if (cell.value).__class__.__name__ == 'unicode':
            return (str(cell.value).encode()).strip()
        return str(cell.value).strip()
