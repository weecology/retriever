from builtins import str
from builtins import object

import os
import io
import sys
import csv

from retriever.lib.models import Engine
from retriever import DATA_DIR, open_fw, open_csvw
from retriever.lib.tools import sort_csv


class DummyConnection(object):

    def cursor(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


class DummyCursor(DummyConnection):
    pass


class engine(Engine):
    """Engine instance for writing data to a CSV file."""
    name = "CSV"
    abbreviation = "csv"
    datatypes = {
        "auto": "INTEGER",
        "int": "INTEGER",
        "bigint": "INTEGER",
        "double": "REAL",
        "decimal": "REAL",
        "char": "TEXT",
        "bool": "INTEGER",
    }
    required_opts = [
        ("table_name",
         "Format of table name",
         os.path.join(DATA_DIR, "{db}_{table}.csv")),
    ]
    table_names = []

    def create_db(self):
        """Override create_db since there is no database just a CSV file"""
        return None

    def create_table(self):
        """Create the table by creating an empty csv file"""
        self.auto_column_number = 1
        self.file = open_fw(self.table_name())
        self.output_file = open_csvw(self.file)
        self.output_file.writerow([u'{}'.format(val) for val in self.table.get_insert_columns(join=False,create=True)])
        self.table_names.append((self.file, self.table_name()))

    def disconnect(self):
        """Close the last file in the dataset"""
        for output_tuple in self.table_names:
            output_tuple[0].close()

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.writerows(statement)

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement"""
        v = Engine.format_insert_value(self, value, datatype, escape=False, processed=True)
        if v == 'null':
            return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except:
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

    def table_exists(self, db_name, table_name):
        """Check to see if the data file currently exists"""
        table_name = self.table_name(name=table_name, dbname=db_name)
        return os.path.exists(table_name)

    def to_csv(self):
        """Export sorted version of CSV file"""
        for keys in self.script.tables:
            table_name = self.opts['table_name'].format(db=self.db_name, table=keys)
            sort_csv(table_name)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
