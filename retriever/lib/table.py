from future import standard_library

standard_library.install_aliases()

import csv
import io
import sys
from functools import reduce
from collections import OrderedDict

from retriever.lib.cleanup import *


class TableMain(object):
    """Refactor table moddule since raster, vector and tabular data

    all have some common table features
    """

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url


class Table(TableMain):
    """Information about a database table."""

    def __init__(self, **kwargs):
        self.name = None
        self.url = None
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
        self.missingValues = None
        self.cleaned_columns = False
        for key in kwargs:
            setattr(self, key, kwargs[key])
        # for key, item in list(kwargs.items()):
        #     setattr(self, key, item[0] if isinstance(item, tuple) else item)


        # if key == "fields":
        #     # fields = columns of the table
        #
        #     # list of column tuples
        #     column_list = []
        #     for obj in val:
        #         # fields is a collection of JSON objects
        #         # (similar to a list of dicts in python)
        #
        #         if "size" in obj:
        #             column_list.append((obj["name"],
        #                                 (obj["type"], obj["size"])))
        #         else:
        #             column_list.append((obj["name"],
        #                                 (obj["type"],)))
        #
        #     table_dict["columns"] = column_list
        #
        # elif key == "ct_column":
        #     table_dict[key] = "'" + val + "'"
        # for key in self.schema:
        if hasattr(self, 'schema'):

            for key in self.schema:
                if key == "fields":
                    column_list = []
                    for obj in self.schema["fields"]:

                        if "size" in obj:
                            column_list.append((obj["name"],
                                                (obj["type"], obj["size"])))
                        else:
                            column_list.append((obj["name"],
                                                (obj["type"],)))

                    self.columns = column_list
                elif key == "ct_column":
                    setattr(self, key, "'" + self.schema[key] + "'")
                else:
                    setattr(self, key, self.schema[key])
        if hasattr(self, 'dialect'):
            for key, val in self.dialect.items():
                if key == "missingValues":
                    if self.dialect["missingValues"]:
                        self.missingValues = self.dialect["missingValues"]
                        self.cleanup = Cleanup(correct_invalid_value, missingValues=self.missingValues)
                elif key == "delimiter":
                    self.delimiter = str(self.dialect["delimiter"])
                else:
                    setattr(self, key, self.dialect[key])

        TableMain.__init__(self, self.name, self.url)

    def auto_get_columns(self, header):
        """Get column names from the header row.

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
        remove leading whitespaces, replace sql key words, etc.
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
        replace += [(x, '_') for x in (" ", "(", "/", ".", "+", "-", "*", ":", "[", "]")]

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
            "date": "record_date",
            "index": "indices"
        }
        for x in (")", "\n", "\r", '"', "'"):
            replace_dict[x] = ''
        for x in (" ", "(", "/", ".", "-"):
            replace_dict[x] = '_'
        if column_name in replace_dict:
            column_name = replace_dict[column_name]
        return column_name

    def combine_on_delimiter(self, line_as_list):
        """Combine a list of values into a line of csv data."""
        dialect = csv.excel
        dialect.escapechar = "\\"
        if sys.version_info >= (3, 0):
            writer_file = io.StringIO()
        else:
            writer_file = io.BytesIO()
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
        """Get column names for insert statements.

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
        """Get set of column names for insert statements."""
        columns = []
        for item in self.get_insert_columns(False):
            for column in self.columns:
                if item == column[0]:
                    columns.append(column[1][0])

        return columns


class TableRaster(TableMain):
    """Raster table implementation"""
    def __init__(self, **kwargs):
        self.name = None
        self.group = None
        self.relative_path = 0
        self.resolution = None
        self.resolution_units = None
        self.dimensions = None
        self.noDataValue = None
        self.geoTransform = None
        self.parameter = None
        self.extent = None
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)


class TableVector(TableMain):
    """Vector table implementation"""

    def __init__(self, **kwargs):
        self.name = None
        self.pk = None
        self.contains_pk = False
        self.feature_count = 0
        self.attributes = []
        self.attributes_dict = {}
        self.fields_dict = {}
        self.extent = {}
        self.saptialref = None
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)

    def create_table_statement(self):
        """Return create table statment for vector data"""
        self.fields_dict

    def drop_vetor_data_tabe(self):
        """Drop the table for vector data

        NOTE: This may require droping the foreign keys cascaded
        """
        self.fields_dict

    def insert_to_table(self):
        """This function is used to insert to table"""
        self.fields_dict

    def extract_table(self):
        """Select a set of data from the table"""
        self.fields_dict

    def to_raster(self):
        """Convert vector to Raster"""

        self.fields_dict

    def project_to_WGS1984(self, package_proj = None):
        if not package_proj:
            self.fields_dict


myTables = {
    "vector": TableVector,
    "raster": TableRaster,
    "tabular": Table,
}
