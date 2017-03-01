import os
from retriever.lib.models import Engine, no_cleanup


class engine(Engine):
    """Engine instance for PostgreSQL."""
    name = "PostgreSQL"
    abbreviation = "postgres"
    datatypes = {
        "auto": "serial",
        "int": "integer",
        "bigint": "bigint",
        "double": "double precision",
        "decimal": "decimal",
        "char": "varchar",
        "bool": "boolean",
    }
    max_int = 2147483647
    required_opts = [("user",
                      "Enter your PostgreSQL username",
                      "postgres"),
                     ("password",
                      "Enter your password",
                      ""),
                     ("host",
                      "Enter your PostgreSQL host",
                      "localhost"),
                     ("port",
                      "Enter your PostgreSQL port",
                      5432),
                     ("database",
                      "Enter your PostgreSQL database name",
                      "postgres"),
                     ("database_name",
                      "Format of schema name",
                      "{db}"),
                     ("table_name",
                      "Format of table name",
                      "{db}.{table}"),
                     ]

    def create_db_statement(self):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        return Engine.create_db_statement(self).replace("DATABASE", "SCHEMA")

    def create_db(self):
        """Creates the database"""
        try:
            Engine.create_db(self)
        except:
            self.connection.rollback()
            pass

    def create_table(self):
        """PostgreSQL needs to commit operations individually."""
        Engine.create_table(self)
        self.connection.commit()

    def drop_statement(self, objecttype, objectname):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        statement = Engine.drop_statement(self, objecttype, objectname)
        statement += " CASCADE;"
        return statement.replace(" DATABASE ", " SCHEMA ")

    def escape_single_quotes(self, value):
        """Escapes single quotes in the value"""
        return value.replace("'", "''")

    def insert_data_from_file(self, filename):
        """Use PostgreSQL's "COPY FROM" statement to perform a bulk insert."""
        self.get_cursor()
        ct = len([True for c in self.table.columns if c[1][0][:3] == "ct-"]) != 0
        if (([self.table.cleanup.function, self.table.delimiter,
              self.table.header_rows] == [no_cleanup, ",", 1])
            and not self.table.fixed_width
            and not ct
            and (not hasattr(self.table, "do_not_bulk_insert") or not self.table.do_not_bulk_insert)):
            columns = self.table.get_insert_columns()
            filename = os.path.abspath(filename)
            statement = """
COPY """ + self.table_name() + " (" + columns + """)
FROM '""" + filename.replace("\\", "\\\\") + """'
WITH DELIMITER ','
CSV HEADER;"""
            try:
                self.execute("BEGIN")
                self.execute(statement)
                self.execute("COMMIT")
            except:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def insert_statement(self, values):
        """Returns a SQL statement to insert a set of values"""
        statement = Engine.insert_statement(self, values)
        if isinstance(statement, bytes):
            statement = statement.decode("utf-8", "ignore")
        return statement

    def table_exists(self, dbname, tablename):
        """Checks to see if the given table exists"""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT schemaname, tablename FROM pg_tables WHERE schemaname NOT LIKE 'pg_%';")
            self.existing_table_names = set()
            for schema, table in self.cursor:
                self.existing_table_names.add((schema.lower(), table.lower()))
        return (dbname.lower(), tablename.lower()) in self.existing_table_names

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement"""
        if datatype == "bool":
            try:
                if int(value) == 1:
                    return "TRUE"
                elif int(value) == 0:
                    return "FALSE"
            except:
                pass
        return Engine.format_insert_value(self, value, datatype)

    def get_connection(self):
        """Gets the db connection."""
        import psycopg2 as dbapi
        self.get_input()
        conn = dbapi.connect(host=self.opts["host"],
                             port=int(self.opts["port"]),
                             user=self.opts["user"],
                             password=self.opts["password"],
                             database=self.opts["database"])
        conn.set_client_encoding('Latin1')
        return conn
