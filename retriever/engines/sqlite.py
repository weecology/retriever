import os
import pandas as pd
from builtins import range
from collections import OrderedDict

from retriever.lib.defaults import DATA_DIR
from retriever.lib.models import Engine, no_cleanup


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
    placeholder = "?"
    insert_limit = 1000
    required_opts = [("file",
                      "Enter the filename of your SQLite database",
                      "sqlite.db"),
                     ("table_name",
                      "Format of table name",
                      "{db}_{table}"),
                     ("data_dir",
                      "Install directory",
                      DATA_DIR),
                     ]

    def create_db(self):
        """Don't create database for SQLite

        SQLite doesn't create databases. Each database is a file and needs a separate
        connection. This overloads`create_db` to do nothing in this case.
        """
        return None

    def fetch_tables(self, dataset, table_names):
        """Return sqlite dataset as list of pandas dataframe."""
        connection = self.get_connection()
        sql_query = "SELECT * FROM {};"
        data = OrderedDict([
                    (table[len(dataset) + 1:],
                    pd.read_sql_query(sql_query.format(table), connection))
                    for table in table_names
               ])
        return data

    def get_bulk_insert_statement(self):
        """Get insert statement for bulk inserts

        This places ?'s instead of the actual values so that executemany() can
        operate as designed
        """
        columns = self.table.get_insert_columns()
        column_count = len(self.table.get_insert_columns(False))
        insert_stmt = "INSERT INTO " + self.table_name()
        insert_stmt += " (" + columns + ")"
        insert_stmt += " VALUES ("
        for _ in range(0, column_count):
            insert_stmt += "?, "
        insert_stmt = insert_stmt.rstrip(", ") + ")"
        return insert_stmt

    def insert_data_from_file(self, filename):
        """Perform a high speed bulk insert

        Checks to see if a given file can be bulk inserted, and if so loads
        it in chunks and inserts those chunks into the database using
        executemany.
        """
        chunk_size = 1000000
        self.get_cursor()

        # Determine if the dataset includes cross-tab data
        crosstab = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0

        if (([self.table.cleanup.function, self.table.header_rows] == [no_cleanup, 1])
            and not self.table.fixed_width
            and not crosstab
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)):
            filename = os.path.abspath(filename)
            try:
                bulk_insert_statement = self.get_bulk_insert_statement()
                line_endings = set(['\n', '\r', '\r\n'])
                with open(filename, 'r') as data_file:
                    data_chunk = data_file.readlines(chunk_size)
                    data_chunk = [line.rstrip('\r\n') for line in data_chunk if line not in line_endings]
                    del data_chunk[:self.table.header_rows]
                    while data_chunk:
                        data_chunk_split = [row.split(self.table.delimiter)
                                            for row in data_chunk]
                        self.cursor.executemany(bulk_insert_statement, data_chunk_split)
                        data_chunk = data_file.readlines(chunk_size)
                self.connection.commit()
            except:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def get_connection(self):
        """Get db connection."""
        import sqlite3 as dbapi

        self.get_input()
        file = self.opts["file"]
        db_file = self.opts["data_dir"]
        full_path = os.path.join(db_file, file)
        self.set_engine_encoding()
        return dbapi.connect(os.path.normpath(full_path))
