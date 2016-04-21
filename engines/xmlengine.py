import os

from retriever.lib.models import Engine
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
    """Engine instance for writing data to a XML file."""
    name = "XML"
    abbreviation = "xml"
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
         os.path.join(DATA_DIR, "{db}_{table}.xml")),
    ]

    def create_db(self):
        """Override create_db since there is no database just an XML file"""
        return None

    def create_table(self):
        """Create the table by creating an empty XML file"""
        self.output_file = open(self.table_name(), "w")
        self.output_file.write('<?xml version="1.0"?>')
        self.output_file.write('\n<' + os.path.splitext(os.path.basename(self.table_name()))[0] + '>')

    def disconnect(self):
        try:
            self.output_file.close()
            current_output_file = open(self.table_name(), "r")
            file_contents = current_output_file.readlines()
            current_output_file.close()
            file_contents[-1] = file_contents[-1].strip(',')
            file_contents.append('\n</' + os.path.splitext(os.path.basename(self.table_name()))[0] + '>')
            self.output_file = open(self.table_name(), "w")
            self.output_file.writelines(file_contents)
            self.output_file.close()
        except:
            pass

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.write('\n' + statement)

    def format_insert_value(self, value, datatype):

        """Formats a value for an insert statement"""
        v = Engine.format_insert_value(self, value, datatype)
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
        offset = 0
        for i in range(len(self.table.columns)):
            column = self.table.columns[i]
            if 'auto' in column[1][0]:
                values = values[:i + offset] + [self.auto_column_number] + values[i + offset:]
                self.auto_column_number += 1
                offset += 1
        open_tag = '<row>\n'
        keys = [columnname[0] for columnname in self.table.columns]
        write_data = ""
        for i in range(len(keys)):
            write_data += '    ' + '<' + str(keys[i]) + '>' + str(values[i]) + '</' + str(keys[i]) + '>' + "\n"
        end_tag = '</row>'
        return open_tag + write_data + end_tag

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        return os.path.exists(tablename)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
