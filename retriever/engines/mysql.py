from __future__ import print_function
from builtins import str
import os
from retriever.lib.models import Engine, no_cleanup
from retriever import ENCODING, MYSQL_CONF_PATH, open_fr
import re


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

    def check_credentials(self):
        """
        Checks the credentials of the user in the file path ~/.my.cnf for the MySQL
        credentials by checking the username provided by the user in cli.
        If found, it updates the credentials to initialize the connection, else uses the
        default ones.
        """
        self.get_input()
        if os.path.exists(MYSQL_CONF_PATH):
            sql_conf = open_fr(MYSQL_CONF_PATH)
            sql_conf_lines = sql_conf.readlines()
            for line in sql_conf_lines:
                if re.search("user = ", line) and re.sub("user = ", "", line) == self.opts["user"]:
                    username = re.sub("user = ", "", line)
                    pswd_line_index = sql_conf_lines.index(line)+1
                    while not (re.search("password = ", sql_conf_lines[pswd_line_index])):
                        pswd_line_index+=1
                    password = re.sub("password = ", "", sql_conf_lines[pswd_line_index])
                    self.opts["password"] = password

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

    def set_engine_encoding(self):
        """Set MySQL database encoding to match data encoding

           Please update the encoding lookup table if the required encoding is not present.
        """
        encoding = ENCODING.lower()
        if self.script.encoding:
            encoding = self.script.encoding.lower()
        encoding_lookup = {'iso-8859-1': 'latin1', 'latin-1': 'latin1', 'utf-8': 'utf8'}
        db_encoding = encoding_lookup.get(encoding)
        self.execute("SET NAMES '{0}';".format(db_encoding))

    def get_connection(self):
        """Gets the db connection."""
        self.check_credentials()
        args = {'host': self.opts['host'],
                'port': int(self.opts['port']),
                'user': self.opts['user'],
                'passwd': self.opts['password']}
        import pymysql as dbapi
        import pymysql.constants.CLIENT as client
        args['client_flag'] = client.LOCAL_FILES
        return dbapi.connect(**args)
