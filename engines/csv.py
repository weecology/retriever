import os
import platform
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
        if not hasattr(self, 'auto_column_number'):
            self.auto_column_number = 1
        offset = 0
        for i in range(len(self.table.columns)):
            column = self.table.columns[i]
            if 'auto' in column[1][0]:
                values = values[:i+offset] + [self.auto_column_number] + values[i+offset:]
                self.auto_column_number += 1
                offset += 1
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
