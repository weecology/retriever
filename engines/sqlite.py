import os
import csv

from retriever.lib.models import Engine, no_cleanup
from retriever import DATA_DIR
from retriever.lib.tools import sortcsv


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
        """Escapes single quotes in the line"""
        return line.replace("'", "''")

    def get_bulk_insert_statement(self):
        """Get insert statement for bulk inserts

        This places ?'s instead of the actual values so that executemany() can
        operate as designed

        """
        columns = self.table.get_insert_columns()
        types = self.table.get_column_datatypes()
        columncount = len(self.table.get_insert_columns(False))
        insert_stmt = "INSERT INTO " + self.table_name()
        insert_stmt += " (" + columns + ")"
        insert_stmt += " VALUES ("
        for i in range(0, columncount):
            insert_stmt += "?, "
        insert_stmt = insert_stmt.rstrip(", ") + ");"
        return insert_stmt

    def insert_data_from_file(self, filename):
        """Use executemany to perform a high speed bulk insert

        Checks to see if a given file can be bulk inserted, and if so loads
        it in chunks and inserts those chunks into the database using
        executemany.

        """
        CHUNK_SIZE = 1000000
        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (([self.table.cleanup.function, self.table.header_rows] == [no_cleanup, 1])
            and not self.table.fixed_width
            and not ct
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)
            ):
            columns = self.table.get_insert_columns()
            filename = os.path.abspath(filename)
            try:
                bulk_insert_statement = self.get_bulk_insert_statement()
                with open(filename, 'r') as data_file:
                    data_chunk = data_file.readlines(CHUNK_SIZE)
                    del(data_chunk[:self.table.header_rows])
                    while data_chunk:
                        data_chunk_split = [row.split(self.table.delimiter)
                                            for row in data_chunk]
                        self.cursor.executemany(bulk_insert_statement, data_chunk_split)
                        data_chunk = data_file.readlines(CHUNK_SIZE)
                self.connection.commit()
            except:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def to_csv(self):
        """Export SQLite table to CSV"""
        tablename = str(Engine.table_name(self))
        csvfile_output = tablename + '.csv'
        # fixing SQLite encoding issue
        self.connection.text_factory = str
        self.get_cursor()
        sql_query = ("SELECT * FROM " + tablename + ";")
        self.cursor.execute(sql_query)

        row = self.cursor.fetchone()
        colnames = [tuple_i[0] for tuple_i in self.cursor.description]
        csv_out = open(csvfile_output, 'wb')
        csv_writer = csv.writer(csv_out, dialect='excel')
        csv_writer.writerow(colnames)

        while row is not None:
            csv_writer.writerow([values for values in row])
            row = self.cursor.fetchone()

        csv_out.close()
        sortcsv(csvfile_output)
        return csvfile_output

    def table_exists(self, dbname, tablename):
        """Determine if the table already exists in the database"""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            self.existing_table_names = set()
            for line in self.cursor:
                self.existing_table_names.add(line[0].lower())
        return self.table_name(name=tablename, dbname=dbname).lower() in self.existing_table_names

    def get_connection(self):
        """Gets the db connection."""
        import sqlite3 as dbapi
        self.get_input()
        return dbapi.connect(self.opts["file"])
