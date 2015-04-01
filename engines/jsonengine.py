"""Engine for writing data to a JSON file"""

import os
import json
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR

class DummyConnection:
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
    name = "JSON"
    abbreviation = "json"
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
                      os.path.join(DATA_DIR, "{db}_{table}.json")),
                     ]

    def create_db(self):
        """Override create_db since there is no database just a JSON file"""
        return None

    def create_table(self):
        """Create the table by creating an empty json file"""
        self.output_file = open(self.table_name(), "w")
        self.output_file.write('[')

    def disconnect(self):
        """Close out the JSON with a ] and close the file

        Do to an extra comma after the last entry it is necessary to close the
        current file, read it back in, and remove the extra comma, before adding
        the closing bracket, and re-writing the file to disk. This will be
        inefficient for large files and we may want to replace it with something
        better.

        """
        try:
            self.output_file.close()
            current_output_file = open(self.table_name(), "r")
            file_contents = current_output_file.readlines()
            current_output_file.close()
            file_contents[-1] = file_contents[-1].strip(',')
            file_contents.append('\n]\n')
            self.output_file = open(self.table_name(), "w")
            self.output_file.writelines(file_contents)
            self.output_file.close()
        except:
            #when disconnect is called by app.connect_wizard.ConfirmPage to
            #confirm the connection, output_file doesn't exist yet, this is
            #fine so just pass
            pass

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.write('\n' + statement + ',')

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement

        Overrides default behavior by:
        1. Storing decimal numbers as floats rather than strings
        2. Not escaping quotes (handled by the json module)
        3. Replacing "null" with None which will convert to the 'null' keyword
           in json

        """
        self.format_insert_value(value, datatype, json=True)


    def insert_statement(self, values):
        if not hasattr(self, 'auto_column_number'):
            self.auto_column_number = 1
        offset = 0
        for i in range(len(self.table.columns)):
            column = self.table.columns[i]
            if 'auto' in column[1][0]:
                values = values[:i+offset] + [self.auto_column_number] + values[i+offset:]
                self.auto_column_number += 1
                offset += 1
        #FIXME: Should nulls be inserted here? I'm guessing the should be skipped. Find out.
        datadict = {column[0]: value for column, value in zip(self.table.columns, values)}
        return json.dumps(datadict)

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        return os.path.exists(tablename)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
