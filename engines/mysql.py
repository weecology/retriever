from __future__ import print_function
from builtins import str
import os
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
        """Returns a SQL statement to create a database."""
        createstatement = "CREATE DATABASE IF NOT EXISTS " + self.database_name()
        return createstatement

    def insert_data_from_file(self, filename):
        """Calls MySQL "LOAD DATA LOCAL INFILE" statement to perform a bulk
        insert."""

        mysql_set_autocommit_off = """SET autocommit=0; SET UNIQUE_CHECKS=0; SET FOREIGN_KEY_CHECKS=0; SET sql_log_bin=0;"""
        mysql_set_autocommit_on = """SET GLOBAL innodb_flush_log_at_trx_commit=1; COMMIT; SET autocommit=1; SET unique_checks=1; SET foreign_key_checks=1;"""
        
        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (self.table.cleanup.function == no_cleanup and
                not self.table.fixed_width and
                not ct and
                (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)):

            print ("Inserting data from " + os.path.basename(filename) + "...")

            columns = self.table.get_insert_columns()
            statement = """
LOAD DATA LOCAL INFILE '""" + filename.replace("\\", "\\\\") + """'
INTO TABLE """ + self.table_name() + """
FIELDS TERMINATED BY '""" + self.table.delimiter + """'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE """ + str(self.table.header_rows) + """ LINES
(""" + columns + ")"
            try:
                self.cursor.execute(mysql_set_autocommit_off)
                self.cursor.execute(statement)

                self.cursor.execute(mysql_set_autocommit_on)
            except Exception as e:
                self.disconnect()  # If the execute fails the database connection can get hung up
                self.cursor.execute(mysql_set_autocommit_on)
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def table_exists(self, dbname, tablename):
        """Checks to see if the given table exists"""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT table_schema, table_name "
                "FROM information_schema.tables WHERE table_schema NOT IN "
                "('mysql', 'information_schema', 'performance_schema');")
            self.existing_table_names = set()
            for schema, table in self.cursor:
                self.existing_table_names.add((schema.lower(), table.lower()))
        return (dbname.lower(), tablename.lower()) in self.existing_table_names

    def set_engine_encoding(self, encoding='ISO-8859-1'):
        """Set MySQL database encoding to match data encoding

        Defaults to latin1 and falls back to it if an unknown encoding is provided

        """
        encoding_lookup = {'ISO-8859-1': 'latin1'}
        db_encoding = encoding_lookup.get(encoding, 'latin1')
        self.execute("SET NAMES '{0}';".format(db_encoding))

    def get_connection(self):
        """Gets the db connection."""
        args = {'host': self.opts['host'],
                'port': int(self.opts['port']),
                'user': self.opts['user'],
                'passwd': self.opts['password']}
        import pymysql as dbapi
        import pymysql.constants.CLIENT as client
        args['client_flag'] = client.LOCAL_FILES
        self.get_input()
        return dbapi.connect(**args)
