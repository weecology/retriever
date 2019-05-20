import os

from retriever.lib.defaults import DATA_DIR
from retriever.lib.dummy import DummyConnection
from retriever.lib.models import Engine
from retriever.lib.tools import open_fw, open_csvw
from retriever.lib.engine_tools import sort_csv


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
        self.file = open_fw(table_path, encoding=self.encoding)
        self.output_file = open_csvw(self.file)
        column_list = self.table.get_insert_columns(join=False, create=True)
        self.output_file.writerow([u'{}'.format(val) for val in column_list])
        self.table_names.append((self.file, table_path))

        # Register all tables created to enable
        # testing python files having custom download function
        Engine.register_tables(self)

    def disconnect(self):
        """Close the last file in the dataset"""
        for output_tuple in self.table_names:
            output_tuple[0].close()

    def disconnect_files(self):
        """Close each file after being written"""
        self.file.close()

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.writerows(statement)

    def executemany(self, statement, values, commit=True):
        """Write a line to the output file"""
        self.output_file.writerows(statement)

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
