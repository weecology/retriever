"""Engine for writing data to a JSON file"""
from builtins import zip
from builtins import object
from builtins import range

import os
import json

from retriever.lib.models import Engine
from retriever import DATA_DIR, open_fw, open_fr
from collections import OrderedDict
from retriever.lib.tools import json2csv, sort_csv


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
    table_names = []

    def create_db(self):
        """Override create_db since there is no database just a JSON file"""
        return None

    def create_table(self):
        """Create the table by creating an empty json file"""
        self.output_file = open_fw(self.table_name())
        self.output_file.write("[")
        self.table_names.append((self.output_file, self.table_name()))
        self.auto_column_number = 1

    def disconnect(self):
        """Close out the JSON with a `\\n]}` and close the file.

        Close all the file objects that have been created
        Re-write the files stripping off the last comma and then close with a `\\n]}`.
        """
        if self.table_names:
            for output_file_i, file_name in self.table_names:
                output_file_i.close()
                current_input_file = open_fr(file_name)
                file_contents = current_input_file.readlines()
                current_input_file.close()
                file_contents[-1] = file_contents[-1].strip(',\n')
                current_output_file = open_fw(file_name)
                current_output_file.writelines(file_contents)
                current_output_file.writelines(['\n]'])
                current_output_file.close()
            self.table_names = []

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.writelines(statement)

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
        if not hasattr(self, 'auto_column_number'):
            self.auto_column_number = 1

        keys = self.table.get_insert_columns(join=False, create=True)
        if self.table.columns[0][1][0][3:] == 'auto':
            newrows = []
            for rows in values:
                insert_stmt = [self.auto_column_number] + rows
                newrows.append(insert_stmt)
                self.auto_column_number += 1
        else: 
            newrows = values
        json_dumps = []
        for line_data in newrows:
            tuples = (zip(keys, line_data))
            write_data = OrderedDict(tuples)
            json_dumps.append(json.dumps(write_data, ensure_ascii=False) + ",")
        return json_dumps

 
        tuples = (zip(keys, [value for value in values]))
        write_data = OrderedDict(tuples)
        return json.dumps(write_data, ensure_ascii=False)

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        return os.path.exists(tablename)

    def to_csv(self):
        """Export table from json engine to CSV file"""
        for keys in list(self.script.tables):
            table_name = self.opts['table_name'].format(db=self.db_name, table=keys)
            header = self.script.tables[keys].get_insert_columns(join=False, create=True)
            csv_outfile = json2csv(table_name, header_values=header)
            sort_csv(csv_outfile)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
