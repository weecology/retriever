import os
import platform
import shutil
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR, HOME_DIR

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
    name = "Download Only"
    abbreviation = "download"

    def create_db(self):
        return None

    def create_table(self):
        assert False, "Download Only should not trigger create_table()"

    def execute(self, statement, commit=True):
        assert False, "Download Only should not trigger execute()"
        
    def format_insert_value(self, value, datatype):
        assert False, "Download Only should not trigger format_insert_value()"

    def insert_statement(self, values):
        assert False, "Download Only should not trigger format_insert_statement()"
        
    def table_exists(self, dbname, tablename):
        try:
            tablename = self.table_name(name=tablename, dbname=dbname)
            return os.path.exists(tablename)
        except:
            return False

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()
