import os
import xmlrpclib
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
        self.output_file.write('<params>')

    def disconnect(self):
        try:
            self.output_file.close()
            current_output_file = open(self.table_name(), "r")
            file_contents = current_output_file.readlines()
            current_output_file.close()
            #file_contents[-1] = file_contents[-1].strip(',')
            file_contents.append('\n</params\n')
            self.output_file = open(self.table_name(), "w")
            self.output_file.writelines(file_contents)
            self.output_file.close()
        except:
            pass

    def execute(self, statement, commit=True):
        """Write a line to the output file"""
        self.output_file.write('\n' + statement)

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement

        """
        datatype = datatype.split('-')[-1]
        strvalue = str(value).strip()

        # Remove any quotes already surrounding the string
        quotes = ["'", '"']
        if len(strvalue) > 1 and strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
            strvalue = strvalue[1:-1]
        nulls = ("null", "none")

        if strvalue.lower() in nulls:
            return None
        elif datatype in ("int", "bigint", "bool"):
            if strvalue:
                intvalue = strvalue.split('.')[0]
                if intvalue:
                    return int(intvalue)
                else:
                    return None
            else:
                return None
        elif datatype in ("double", "decimal"):
            if strvalue:
                return float(strvalue)
            else:
                return None
        elif datatype=="char":
            if strvalue.lower() in nulls:
                return None
            else:
                return strvalue
        else:
            return None


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
        return xmlrpclib.dumps(datadict)

    def table_exists(self, dbname, tablename):
        """Check to see if the data file currently exists"""
        tablename = self.table_name(name=tablename, dbname=dbname)
        return os.path.exists(tablename)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()