import os
import pandas as pd

from retriever.lib.defaults import DATA_DIR
from retriever.lib.dummy import DummyConnection
from retriever.lib.engine_tools import sort_csv
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for writing data to a CSV file."""

    name = "CSV"
    abbreviation = "csv"
    auto_column_number = 0
    datatypes = {
        "auto": "INTEGER",
        "int": "INTEGER",
        "bigint": "INTEGER",
        "double": "REAL",
        "decimal": "REAL",
        "char": "TEXT",
        "bool": "INTEGER",
    }
    insert_limit = 1000
    required_opts = [
        ("table_name",
         "Format of table name",
         "{db}_{table}.csv"),
        ("data_dir",
         "Install directory",
         DATA_DIR),
    ]
    table_names = []

    def create_db(self):
        """Override create_db since there is no database just a CSV file"""
        return None

    def create_table(self):
        """Create the table by creating an empty csv file"""
        self.auto_column_number = 1
        table_path = os.path.join(self.opts["data_dir"], self.table_name())
        self.output_file = open(table_path, 'a')
        column_list = self.table.get_insert_columns(join=False, create=True)
        self.output_file.writelines(','.join([u'{}'.format(val) for val in column_list]))
        self.output_file.write('\n')
        self.table_names.append((self.output_file, table_path))

        # Register all tables created to enable
        # testing python files having custom download function
        Engine.register_tables(self)

    def disconnect(self):
        """Close the last file in the dataset"""
        for output_tuple in self.table_names:
            output_tuple[0].close()

    def disconnect_files(self):
        """Close each file after being written"""
        self.output_file.close()

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.writelines(statement)

    def executemany(self, statement, values, commit=True):
        """Write a line to the output file"""
        chunk = pd.DataFrame(statement)
        chunk.to_csv(self.output_file, mode='a', index=False, header= None, chunksize= 10**6)

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement"""
        v = Engine.format_insert_value(self, value, datatype)
        if v == 'null':
            return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except BaseException:
            pass
        return v

    def insert_statement(self, values):
        """Returns a comma delimited row of values"""
        if not hasattr(self, 'auto_column_number'):
            self.auto_column_number = 1

        if self.table.columns[0][1][0][3:] == 'auto':
            newrows = []
            for rows in values:
                insert_stmt = [self.auto_column_number] + rows
                newrows.append(insert_stmt)
                self.auto_column_number += 1
            return newrows
        else:
            return values

    def insert_data_from_file(self, filename):
        """Perform a high speed bulk insert

        Checks to see if a given file can be bulk inserted, and if so loads
        it in chunks and inserts those chunks into the csv using chunksize.
        """
        chunk_size = 100000

        # Determine if the dataset includes cross-tab data
        crosstab = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0

        if (([self.table.cleanup.function, self.table.header_rows] == [no_cleanup, 1])
            and not self.table.fixed_width
            and not crosstab
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)):
            filename = os.path.abspath(filename)
            try:
                for chunk in pd.read_csv(filename, chunksize=chunk_size):
                    chunk.to_csv(self.output_file, mode='a', header=None, index=False,
                                 chunksize=chunk_size)
            except:
                self.output_file.truncate()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        tabledir = self.opts["data_dir"]
        table_name = os.path.join(tabledir, tablename)
        return os.path.exists(table_name)

    def to_csv(self, sort=True, path=None, select_columns=None):
        """Export sorted version of CSV file"""
        for table_item in self.script_table_registry[self.script.name]:
            sort_csv(table_item[0])

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()