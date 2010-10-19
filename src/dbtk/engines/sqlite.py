import os
import platform
from dbtk.lib.models import Engine, no_cleanup

class engine(Engine):
    """Engine instance for SQLite."""
    name = "SQLite"
    abbreviation = "s"
    datatypes = ["INTEGER",
                 "INTEGER",
                 "REAL",
                 "REAL",
                 "TEXT",
                 "INTEGER"]
    required_opts = [["file", 
                      "Enter the filename of your SQLite database: ",
                      "sqlite.db",
                      ""]]
    def create_db(self):
        """SQLite doesn't create databases; each database is a file and needs
        a separate connection."""
        return None
    def tablename(self):
        """The database file is specifically connected to, so database.table 
        is not necessary."""
        return self.db.dbname + "_" + self.table.tablename
    def get_cursor(self):
        """Gets the db connection and cursor."""
        import sqlite3 as dbapi
        self.get_input()
        self.connection = dbapi.connect(self.opts["file"])
        self.cursor = self.connection.cursor()

