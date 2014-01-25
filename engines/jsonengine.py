"""Engine for writing data to a JSON file"""

import os
import json
from retriever.lib.models import Engine, no_cleanup


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
                      "{db}_{table}.json"),
                     ]
                      
    def create_db(self):
        """Override create_db since there is no database just a JSON file""" 
        return None
        
    def create_table(self):
        """Create the table by creating an empty json"""
        self.output_file = open(self.table_name(), "w")
        self.output_file.write('[')
        
    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.write('\n' + statement + ',')
        
    def format_insert_value(self, value, datatype):
        """Cleanup values for inserting

        Replace nulls with empty strings and single quotes with double quotes

        """
        v = Engine.format_insert_value(self, value, datatype)
        if v == 'null': return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except:
            pass
        return v
        
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
