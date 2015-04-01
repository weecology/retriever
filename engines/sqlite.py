import os
import platform
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR

class engine(Engine):
    """Engine instance for SQLite."""
    name = "SQLite"
    abbreviation = "sqlite"
    datatypes = {
                 "auto": "INTEGER",
                 "int": "INTEGER",
                 "bigint": "INTEGER",
                 "double": "REAL",
                 "decimal": "REAL",
                 "char": "TEXT",
                 "bool": "INTEGER",
                 }
    required_opts = [("file", 
                      "Enter the filename of your SQLite database",
                      os.path.join(DATA_DIR, "sqlite.db"),
                      ""),
                     ("table_name",
                      "Format of table name",
                      "{db}_{table}"),
                     ]
                      
    def create_db(self):
        """SQLite doesn't create databases; each database is a file and needs
        a separate connection."""
        return None
        
    def escape_single_quotes(self, line):
        return line.replace("'", "''")
        
    def table_exists(self, dbname, tablename):
        """Determine if the table already exists in the database"""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            self.existing_table_names = set()
            for line in self.cursor:
                self.existing_table_names.add(line[0].lower())
        return self.table_name(name=tablename, dbname=dbname).lower() in self.existing_table_names
        
    def get_connection(self):
        """Gets the db connection."""
        import sqlite3 as dbapi
        self.get_input()
        return dbapi.connect(self.opts["file"])
