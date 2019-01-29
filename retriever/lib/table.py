from future import standard_library

standard_library.install_aliases()

import csv
import io
import sys
from functools import reduce

from retriever.lib.cleanup import *


class Dataset(object):
    """Dataset generic properties"""

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url


class TabularDataset(Dataset):
    """Tabular database table."""

    def __init__(self, name=None, url=None, pk=True,
                 contains_pk=False, delimiter=None,
                 header_rows=1, column_names_row=1,
                 fixed_width=False, cleanup=Cleanup(),
                 record_id=0,
                 columns=[],
                 replace_columns=[],
                 missingValues=None,
                 cleaned_columns=False, **kwargs):

        self.name = name
        self.url = url
        self.pk = pk
        self.contains_pk = contains_pk
        self.delimiter = delimiter
        self.header_rows = header_rows
        self.column_names_row = column_names_row
        self.fixed_width = fixed_width
        self.cleanup = cleanup
        self.record_id = record_id
        self.columns = columns
        self.replace_columns = replace_columns
        self.missingValues = missingValues
        self.cleaned_columns = cleaned_columns
        self.dataset_type = "TabularDataset"
        for key in kwargs:
            if hasattr(self, key):
                self.key = kwargs[key]
            else:
                setattr(self, key, kwargs[key])

        if hasattr(self, 'schema'):
            self.add_schema()
        if hasattr(self, 'dialect'):
            self.add_dialect()

        Dataset.__init__(self, self.name, self.url)

    def add_dialect(self):
        """Initialize dialect table properties.

        These include a table's null or missing values,
        the delimiter, the function to perform on missing values
        and any values in the dialect's dict.
        """
        for key, _ in self.dialect.items():
            if key == "missingValues":
                if self.dialect["missingValues"]:
                    self.missingValues = self.dialect["missingValues"]
                    self.cleanup = Cleanup(correct_invalid_value,
                                           missingValues=self.missingValues)
            elif key == "delimiter":
                self.delimiter = str(self.dialect["delimiter"])
            else:
                setattr(self, key, self.dialect[key])

    def add_schema(self):
        """Add a schema to the table object.

        Define the data type for the columns in the table.
        """
        spec_data_types = {
            # Dict to map retriever and frictionless data types.
            # spec types not defined, default to char
            "integer": "int",
            "object": "bigint",
            "number": "double",
            "string": "char",
            "boolean": "bool",
            "year": "int",
            # Retriever specific data types
            "auto": "auto",
            "int": "int",
            "bigint": "bigint",
            "double": "double",
            "decimal": "decimal",
            "char": "char",
            "bool": "bool",
            "skip": "skip"
        }

        for key in self.schema:
            if key == "fields":
                column_list = []
                for obj in self.schema["fields"]:
                    type = None
                    if str(obj["type"]).startswith("pk-") or str(obj["type"]).startswith("ct-"):
                        type = obj["type"]
                    else:
                        type = spec_data_types.get(obj["type"], "char")

                    if "size" in obj:
                        column_list.append((obj["name"],
                                            (type,
                                             obj["size"])))
                    else:
                        column_list.append((obj["name"],
                                            (type,)))
                self.columns = column_list
            elif key == "ct_column":
                setattr(self, key, "'" + self.schema[key] + "'")
            else:
                setattr(self, key, self.schema[key])

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
            "index": "indices",
            "repeat": "repeats", 
            "system": "systems", 
            "class": "classes"
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
            self.columns = [(self.clean_column_name(name[0]), name[1])
                            for name in column_names]
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
        return columns

    def get_column_datatypes(self):
        """Get set of column names for insert statements."""
        columns = []
        for item in self.get_insert_columns(False):
            for column in self.columns:
                if item == column[0]:
                    columns.append(column[1][0])

        return columns


class RasterDataset(Dataset):
    """Raster table implementation"""

    def __init__(self, name=None, url=None, dataset_type="RasterDataset", **kwargs):
        self.name = name
        self.group = None
        self.relative_path = 0
        self.resolution = None
        self.resolution_units = None
        self.dimensions = None
        self.noDataValue = None
        self.geoTransform = None
        self.parameter = None
        self.extent = None
        self.dataset_type = dataset_type
        self.url = url
        for key in kwargs:
            setattr(self, key, kwargs[key])
        Dataset.__init__(self, self.name, self.url)


class VectorDataset(Dataset):
    """Vector table implementation."""

    def __init__(self, name=None, url=None, dataset_type="VectorDataset", **kwargs):
        self.name = name
        self.pk = None
        self.contains_pk = False
        self.feature_count = 0
        self.attributes = []
        self.attributes_dict = {}
        self.fields_dict = {}
        self.extent = {}
        self.saptialref = None
        self.dataset_type = dataset_type
        self.url = url
        for key in kwargs:
            if hasattr(self, key):
                self.key = kwargs[key]
            else:
                setattr(self, key, kwargs[key])

        Dataset.__init__(self, self.name, self.url)

myTables = {
    "vector": VectorDataset,
    "raster": RasterDataset,
    "tabular": TabularDataset,
}
