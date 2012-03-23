import os
import platform
from retriever.lib.models import Engine, no_cleanup


class DummyCursor:
    pass

class DummyConnection:
    def cursor(self):
        pass
    def commit(self):
        pass

class engine(Engine):
    """Engine instance for writing data to a CSV file."""
    name = "CSV"
    abbreviation = "c"
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
                      "{db}_{table}.csv"),
                     ]
                      
    def create_db(self):
        return None
        
    def create_table(self):
        self.output_file = open(self.tablename(), "w")
        self.output_file.write(','.join(['"%s"' % c[0] for c in self.table.columns]))
        
    def execute(self, statement, commit=True):
        self.output_file.write('\n' + statement)
        
    def format_insert_value(self, value, datatype):
        v = Engine.format_insert_value(self, value, datatype)
        if v == 'null': return ""
        try:
            if len(v) > 1 and v[0] == v[-1] == "'":
                v = '"%s"' % v[1:-1]
        except:
            pass
        return v
        
    def insert_statement(self, values):
        return ','.join([str(value) for value in values])
        
    def table_exists(self, dbname, tablename):
        try:
            tablename = self.tablename(name=tablename, dbname=dbname)
            return os.path.exists(tablename)
        except:
            return False

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
