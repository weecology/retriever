import os

from retriever.lib.defaults import DATA_DIR
from retriever.lib.dummy import DummyConnection
from retriever.lib.models import Engine
from retriever.lib.tools import open_fr, open_fw
from retriever.lib.engine_tools import xml2csv, sort_csv


class engine(Engine):
    """Engine instance for writing data to a XML file."""

    name = "XML"
    abbreviation = "xml"
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
         "{db}_{table}.xml"),
        ("data_dir",
         "Install directory",
         DATA_DIR),
    ]
    table_names = []

    def create_db(self):
        """Override create_db since there is no database just an XML file."""
        return None

    def create_table(self):
        """Create the table by creating an empty XML file."""
        table_path = os.path.join(self.opts["data_dir"], self.table_name())
        self.output_file = open_fw(table_path, encoding=self.encoding)
        self.output_file.write(u'<?xml version="1.0" encoding="UTF-8"?>')
        self.output_file.write(u'\n<root>')
        self.table_names.append((self.output_file, table_path))
        self.auto_column_number = 1

        # Register all tables created to enable
        # testing python files having custom download function
        if self.script.name not in self.script_table_registry:
            self.script_table_registry[self.script.name] = []
        self.script_table_registry[self.script.name].append(
            (self.table_name(), self.table))

    def disconnect(self):
        """Close out the xml files

        Close all the file objects that have been created
        Re-write the files stripping off the last comma and then close with a closing tag)
        """
        if self.table_names:
            for output_file_i, file_name in self.table_names:
                output_file_i.close()
                current_input_file = open_fr(file_name, encoding=self.encoding)
                file_contents = current_input_file.readlines()
                current_input_file.close()
                file_contents[-1] = file_contents[-1].strip(',')
                current_output_file = open_fw(file_name, encoding=self.encoding)
                current_output_file.writelines(file_contents)
                current_output_file.write(u'\n</root>')
                current_output_file.close()
            self.table_names = []

    def execute(self, statement, commit=True):
        """Write a line to the output file."""
        self.output_file.writelines(statement)

    def executemany(self, statement, values, commit=True):
        """Write a line to the output file."""
        self.output_file.writelines(statement)

    def format_insert_value(self, value, datatype):
        """Format value for an insert statement."""
        v = Engine.format_insert_value(self, value, datatype)
        if v is None:
            return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except BaseException:
            pass
        return v

    def insert_statement(self, values):
        """Create the insert statement.

        Wrap each data value with column values(key)
        using _format_single_row <key> value </key>.
        """
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

        xml_lines = ['\n<row>\n{}</row>' \
                     ''.format(self._format_single_row(keys, line_data))
                     for line_data in newrows]
        return xml_lines

    def _format_single_row(self, keys, line_data):
        """Create an xml string from the keys and line_data values."""
        row_values = ['    <{key}>{value}</{key}>\n'.format(key=key, value=value)
                      for key, value in zip(keys, line_data)]
        return ''.join(row_values)

    def to_csv(self, sort=True, path=None, select_columns=None):
        """Export table from xml engine to CSV file."""
        for table_item in self.script_table_registry[self.script.name]:
            header = table_item[1].get_insert_columns(join=False, create=True)
            outputfile = os.path.normpath(
                os.path.join(path if path else '', os.path.splitext(os.path.basename(table_item[0]))[0] + '.csv'))
            csv_outfile = xml2csv(table_item[0], outputfile=outputfile, header_values=header)
            sort_csv(csv_outfile)

    def get_connection(self):
        """Get db connection."""
        self.get_input()
        return DummyConnection()
