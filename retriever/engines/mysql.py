from __future__ import print_function

import os
from builtins import str

from retriever.lib.defaults import ENCODING
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for MySQL."""

    name = "MySQL"
    abbreviation = "mysql"
    datatypes = {
        "auto": "INT(5) NOT NULL AUTO_INCREMENT",
        "int": "INT",
        "bigint": "BIGINT",
        "double": "DOUBLE",
        "decimal": "DECIMAL",
        "char": ("TEXT", "VARCHAR"),
        "bool": "BOOL",
    }
    max_int = 4294967295
    placeholder = "%s"
    insert_limit = 1000
    required_opts = [("user",
                      "Enter your MySQL username",
                      "root"),
                     ("password",
                      "Enter your password",
                      ""),
                     ("host",
                      "Enter your MySQL host",
                      "localhost"),
                     ("port",
                      "Enter your MySQL port",
                      3306),
                     ("database_name",
                      "Format of database name",
                      "{db}"),
                     ("table_name",
                      "Format of table name",
                      "{db}.{table}"),
                     ]

    def create_db_statement(self):
        """Return SQL statement to create a database."""
        createstatement = "CREATE DATABASE IF NOT EXISTS " + self.database_name()
        return createstatement

    def insert_data_from_file(self, filename):
        """Call MySQL "LOAD DATA LOCAL INFILE" statement to perform a bulk insert."""

        mysql_set_autocommit_off = """SET autocommit=0;"""
        mysql_set_autocommit_on = """SET autocommit=1;"""

        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (self.table.cleanup.function == no_cleanup and
                not self.table.fixed_width and
                not ct and
                (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)):

            print("Inserting data from " + os.path.basename(filename) + "...")

            columns = self.table.get_insert_columns()
            statement = """
BEGIN;
LOAD DATA LOCAL INFILE '""" + filename.replace("\\", "\\\\") + """'
INTO TABLE """ + self.table_name() + """
FIELDS TERMINATED BY '""" + self.table.delimiter + """'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE """ + str(self.table.header_rows) + """ LINES
(""" + columns + "); COMMIT;"
            try:
                self.cursor.execute(mysql_set_autocommit_off)
                self.cursor.execute(statement)

                self.cursor.execute(mysql_set_autocommit_on)
            except Exception as e:
                self.cursor.execute("ROLLBACK;")
                self.disconnect()  # If the execute fails the database connection can get hung up
                self.cursor.execute(mysql_set_autocommit_on)
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def table_exists(self, dbname, tablename):
        """Check to see if the given table exists."""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT table_schema, table_name "
                "FROM information_schema.tables WHERE table_schema NOT IN "
                "('mysql', 'information_schema', 'performance_schema');")
            self.existing_table_names = set()
            for schema, table in self.cursor:
                self.existing_table_names.add((schema.lower(), table.lower()))
        return (dbname.lower(), tablename.lower()) in self.existing_table_names

    def set_engine_encoding(self):
        """Set MySQL database encoding to match data encoding"""
        db_encoding = self.lookup_encoding()
        self.execute("SET NAMES '{0}';".format(db_encoding))
        Engine.set_engine_encoding(self)

    def lookup_encoding(self):
        """Convert well known encoding to MySQL syntax

        MySQL has a unique way of representing the encoding.
        For example, latin-1 becomes latin1 in MySQL.
        Please update the encoding lookup table if the required
        encoding is not present."""
        encoding = ENCODING.lower()
        if self.script.encoding:
            encoding = self.script.encoding.lower()
        encoding_lookup = {'iso-8859-1': 'latin1', 'latin-1': 'latin1', 'utf-8': 'UTF8MB4'}
        db_encoding = encoding_lookup.get(encoding)
        return db_encoding

    def get_connection(self):
        """Get db connection.

        PyMySQL has changed the default encoding from latin1 to utf8mb4.
        https://github.com/PyMySQL/PyMySQL/pull/692/files
        For PyMySQL to work well on CI infrastructure,
        connect with the preferred charset
        """
        args = {'host': self.opts['host'],
                'port': int(self.opts['port']),
                'user': self.opts['user'],
                'passwd': self.opts['password']}
        import pymysql as dbapi
        import pymysql.constants.CLIENT as client
        args['client_flag'] = client.LOCAL_FILES
        self.get_input()
        return dbapi.connect(charset=self.lookup_encoding(),
                             read_default_file='~/.my.cnf', **args)
