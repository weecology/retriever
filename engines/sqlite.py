from builtins import range
import os
from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR


class engine(Engine):
    """Engine instance for SQLite."""
    name = "SQLite"
    abbreviation = "sqlite"
    datatypes = {
        "auto": ("INTEGER", "AUTOINCREMENT"),
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
        """Escapes single quotes in the line"""
        return line.replace("'", "''")

    def get_bulk_insert_statement(self):
        """Get insert statement for bulk inserts

        This places ?'s instead of the actual values so that executemany() can
        operate as designed
        """
        columns = self.table.get_insert_columns()
        types = self.table.get_column_datatypes()
        column_count = len(self.table.get_insert_columns(False))
        insert_stmt = "INSERT INTO " + self.table_name()
        insert_stmt += " (" + columns + ")"
        insert_stmt += " VALUES ("
        for i in range(0, column_count):
            insert_stmt += "?, "
        insert_stmt = insert_stmt.rstrip(", ") + ")"
        return insert_stmt

    def table_exists(self, dbname, tablename):
        """Determine if the table already exists in the database"""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            self.existing_table_names = set()
            for line in self.cursor:
                self.existing_table_names.add(line[0].lower())
        return self.table_name(name=tablename, dbname=dbname).lower() in self.existing_table_names

    def to_csv(self):
        Engine.to_csv(self)

    def get_connection(self):
        """Gets the db connection."""
        import sqlite3 as dbapi
        self.get_input()
        return dbapi.connect(self.opts["file"])
