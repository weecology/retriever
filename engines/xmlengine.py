import os
import io
from builtins import str
from builtins import object
from builtins import range
from retriever.lib.models import Engine
from retriever import DATA_DIR
from retriever.lib.tools import xml2csv, sort_csv


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
    table_names = []

    def create_db(self):
        """Override create_db since there is no database just an XML file"""
        return None

    def create_table(self):
        """Create the table by creating an empty XML file"""
        self.output_file = io.open(self.table_name(), "w")
        self.output_file.write('<?xml version="1.0" ?>')
        self.output_file.write('\n<root>')
        self.table_names.append((self.output_file, self.table_name()))
        self.auto_column_number = 1

    def disconnect(self):
        """Close out the xml files

        Close all the file objects that have been created
        Re-write the files stripping off the last comma and then close with a closing tag)
        """
        for output_file_i, file_name in self.table_names:

            try:
                output_file_i.close()
                current_input_file = open(file_name, "r")
                file_contents = current_input_file.readlines()
                current_input_file.close()
                file_contents[-1] = file_contents[-1].strip(',')
                current_output_file = open(file_name, "w")
                current_output_file.writelines(file_contents)
                current_output_file.write('\n</root>')
                current_output_file.close()

            except:
                # when disconnect is called by app.connect_wizard.ConfirmPage to
                # confirm the connection, output_file doesn't exist yet, this is
                # fine so just pass
                pass

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.writelines(statement)

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement"""
        v = Engine.format_insert_value(self, value, datatype, escape=False)
        if v == 'null':
            return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except:
            pass
        return v

    def insert_statement(self, values):
        print (values, values[0][2])

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

        open_tag = '\n<row>\n'
        end_tag = '</row>'
        xml_lines = []
        for line_data in newrows:
            write_data = ""
            for i in range(len(keys)):
                write_data += '    ' + '<' + str(keys[i]) + '>' + str(line_data[i]) + '</' + str(keys[i]) + '>' + "\n"
            xml_lines.append(open_tag + write_data + end_tag)
        return xml_lines

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        return os.path.exists(tablename)

    def to_csv(self):
        """Export table from xml engine to CSV file"""
        keys = self.table.get_insert_columns(join=False, create=True)
        csv_outfile = xml2csv(self.table_name(), header_values=keys)
        return sort_csv(csv_outfile)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
