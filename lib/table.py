from future import standard_library
standard_library.install_aliases()
from builtins import next
from builtins import object

import csv
import io
import sys
from functools import reduce

from retriever.lib.cleanup import *


class Table(object):
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
        self.escape_single_quotes = True
        self.escape_double_quotes = True
        self.cleaned_columns = False
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)

    def auto_get_columns(self, header):
        """Gets the column names from the header row

        Identifies the column names from the header row.
        Replaces database keywords with alternatives.
        Replaces special characters and spaces.
        """
        columns = [self.clean_column_name(x) for x in header]
        column_values = {x: [] for x in columns if x}
        self.cleaned_columns = True
        return [[x, None] for x in columns if x], column_values

    def clean_column_name(self, column_name):
        """Clean column names using the expected sql guidelines
        remove leading whitespaces, replace sql key words, etc..
        """
        column_name = column_name.lower().strip().replace("\n", "")
        replace_columns = {old.lower(): new.lower()
                           for old, new in self.replace_columns}
        column_name = str(replace_columns.get(column_name, column_name).strip())
        replace = [
            ("%", "percent"),
            ("&", "and"),
            ("\xb0", "degrees"),
            ("^", "_power_"),
            ("<", "_lthn_"),
            (">", "_gthn_"),
        ]
        replace += [(x, '') for x in (")", "?", "#", ";" "\n", "\r", '"', "'")]
        replace += [(x, '_') for x in (" ", "(", "/", ".", "-", "*", ":", "[", "]")]

        column_name = reduce(lambda x, y: x.replace(*y), replace, column_name)

        while "__" in column_name:
            column_name = column_name.replace("__", "_")
        column_name = column_name.lstrip("0123456789_").rstrip("_")
        replace_dict = {
            "group": "grp",
            "order": "ordered",
            "check": "checked",
            "references": "refs",
            "long": "lon",
            "column": "columns",
            "cursor": "cursors",
            "delete": "deleted",
            "insert": "inserted",
            "join": "joins",
            "select": "selects",
            "table": "tables",
            "update": "updates",
            "date": "record_date"
        }
        for x in (")", "\n", "\r", '"', "'"):
            replace_dict[x] = ''
        for x in (" ", "(", "/", ".", "-"):
            replace_dict[x] = '_'
        if column_name in replace_dict:
            column_name = replace_dict[column_name]
        return column_name

    def combine_on_delimiter(self, line_as_list):
        """Combine a list of values into a line of csv data"""
        dialect = csv.excel
        dialect.escapechar = "\\"
        if sys.version_info >= (3, 0):
            writer_file =  io.StringIO()
        else:
            writer_file =  io.BytesIO()
        writer = csv.writer(writer_file, dialect=dialect, delimiter=self.delimiter)
        writer.writerow(line_as_list)
        return writer_file.getvalue()

    def values_from_line(self, line):
        linevalues = []
        if self.columns[0][1][0] == 'pk-auto':
            column = 1
        else:
            column = 0

        for value in line:
            try:
                this_column = self.columns[column][1][0]

                # If data type is "skip" ignore the value
                if this_column == "skip":
                    pass
                elif this_column == "combine":
                    # If "combine" append value to end of previous column
                    linevalues[-1] += " " + value
                else:
                    # Otherwise, add new value
                    linevalues.append(value)
            except:
                # too many values for columns; ignore
                pass
            column += 1

        # make sure we have enough values by padding with None
        keys = self.get_insert_columns(join=False, create=False)
        if len(linevalues) < len(keys):
            linevalues.extend([None for _ in range(len(keys) - len(linevalues))])

        return linevalues

    def get_insert_columns(self, join=True, create=False):
        """Gets column names for insert statements

        `create` should be set to `True` if the returned values are going to be used
        for creating a new table. It includes the `pk_auto` column if present. This
        column is not included by default because it is not used when generating
        insert statements for database management systems.
        """
        columns = []
        if not self.cleaned_columns:
            column_names = list(self.columns)
            self.columns[:] = []
            self.columns = [(self.clean_column_name(name[0]), name[1]) for name in column_names]
            self.cleaned_columns = True
        for item in self.columns:
            if not create and item[1][0] == 'pk-auto':
                # don't include this columns if create=False
                continue
            thistype = item[1][0]
            if (thistype != "skip") and (thistype != "combine"):
                columns.append(item[0])
        if join:
            return ", ".join(columns)
        else:
            return columns

    def get_column_datatypes(self):
        """Gets a set of column names for insert statements."""
        columns = []
        for item in self.get_insert_columns(False):
            for column in self.columns:
                if item == column[0]:
                    columns.append(column[1][0])

        return columns
