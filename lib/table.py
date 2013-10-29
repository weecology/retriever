from retriever.lib.cleanup import *
import csv


class Table:
    """Information about a database table."""
    def __init__(self, name, **kwargs):
        self.name = name
        self.pk = True
        self.contains_pk = False
        self.delimiter = None
        self.header_rows = 1
        self.column_names_row = 1
        self.fixed_width = False
        self.cleanup = Cleanup()
        self.record_id = 0
        self.columns = []
        self.replace_columns = []
        self.escape_single_quotes=True
        self.escape_double_quotes=True
        for key, item in kwargs.items():
            setattr(self, key, item[0] if isinstance(item, tuple) else item)
            
    def auto_get_columns(self, header):
        """Gets the column names from the header row

        Identifies the column names from the header row.
        Replaces database keywords with alternatives.
        Replaces special characters and spaces.

        """
        if self.fixed_width:
            column_names = self.extract_values(header)
        else:
            # Get column names from header row
            values = self.split_on_delimiter(header)
            column_names = [name.strip() for name in values]
        
        columns = map(lambda x: self.clean_column_name(x), column_names)
        column_values = {x:[] for x in columns}

        return [[x, None] for x in columns], column_values
        
    def clean_column_name(self, column_name):
        '''Makes sure a column name is formatted correctly by removing reserved 
        words, symbols, numbers, etc.'''
        column_name = column_name.lower()
        
        replace = [
                   ("%", "percent"),
                   ("&", "and"),
                   ("\xb0", "degrees"),
                   ("group", "grp"),
                   ("order", "sporder"),
                   ("references", "refs"),
                   ("long", "lon"),
                   ("date", "record_date"),
                   ("?", ""),
                   ] + self.replace_columns
        replace += [(x, '') for x in (")", "\n", "\r", '"', "'")]
        replace += [(x, '_') for x in (" ", "(", "/", ".", "-")]
        column_name = reduce(lambda x, y: x.replace(*y), replace, column_name)
        
        while "__" in column_name:
            column_name = column_name.replace("__", "_")
        column_name = column_name.lstrip("0123456789_").rstrip("_")
        
        return column_name
        
    def split_on_delimiter(self, line):
        dialect = csv.excel
        dialect.escapechar = "\\"
        r = csv.reader([line], dialect=dialect, delimiter=self.delimiter)
        return r.next()
