import os

from retriever.lib.defaults import ENCODING
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
    placeholder = "%s"
    insert_limit = 1000
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

    def auto_create_table(self, table, url=None, filename=None, pk=None):
        if table.dataset_type in ["RasterDataset", "VectorDataset"]:
            self.table = table
            if url and not filename:
                filename = Engine.filename_from_url(url)

            if url and not self.find_file(filename):
                # If the file doesn't exist, download it
                self.download_file(url, filename)

            file_path = self.find_file(filename)
            if file_path:
                filename, _ = os.path.splitext(os.path.basename(file_path))

                self.create_table()
        else:
            Engine.auto_create_table(self, table, url, filename, pk)

    def create_db_statement(self):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        return Engine.create_db_statement(self).replace("DATABASE", "SCHEMA")

    def create_db(self):
        """Create Engine database."""
        try:
            Engine.create_db(self)
        except BaseException:
            self.connection.rollback()
            pass

    def create_table(self):
        """Create a table and commit.

        PostgreSQL needs to commit operations individually.
        Enable PostGis extensions if a script has a non tabular table.
        """
        if self.table and self.table.dataset_type and \
                not self.table.dataset_type == "TabularDataset":
            try:
                # Check if Postgis is installed and EXTENSION are Loaded
                if self.execute("SELECT PostGIS_full_version();") or \
                        self.execute("SELECT PostGIS_version()"):
                    pass
            except BaseException:
                print("Make sure you have Postgis\n"
                      "And CREATE EXTENSION postgis, postgis_topology")
                raise
            return
        Engine.create_table(self)
        self.connection.commit()

    def drop_statement(self, objecttype, objectname):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        statement = Engine.drop_statement(self, objecttype, objectname)
        statement += " CASCADE;"
        return statement.replace(" DATABASE ", " SCHEMA ")

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
            except BaseException:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)

    def insert_statement(self, values):
        """Return SQL statement to insert a set of values."""
        statement = Engine.insert_statement(self, values)
        if isinstance(statement, bytes):
            statement = statement.decode("utf-8", "ignore")
        return statement

    def supported_raster(self, path, ext=None):
        path = os.path.normpath(os.path.abspath(path))
        if ext:
            raster_extensions = ext
        else:
            raster_extensions = ['.gif', '.img', '.bil',
                                 '.jpg', '.tif', '.tiff', '.hdf', '.l1b']

        return [os.path.normpath(os.path.join(root, names))
                for root, _, files in os.walk(path, topdown=False)
                for names in files
                if os.path.splitext(names)[1] in raster_extensions]

    def insert_raster(self, path=None, srid=4326):
        """Import Raster into Postgis Table

        Uses raster2pgsql -I -C -s <SRID> <PATH> <SCHEMA>.<DBTABLE>
        | psql -d <DATABASE>
        The sql processed by raster2pgsql is run
         as psql -U postgres -d <gisdb> -f <elev>.sql
         """
        if not path:
            path = Engine.format_data_dir(self)
        raster_sql = "raster2pgsql -M -d -I -s {SRID} {path} -F -t 100x100 {SCHEMA_DBTABLE}".format(
            SRID=srid,
            path=path, SCHEMA_DBTABLE=self.table_name())

        cmd_string = """ | psql -U {USER} -d {DATABASE}""".format(
            USER=self.opts["user"],
            DATABASE=self.opts["database"])
        os.system(raster_sql + cmd_string)

    def insert_vector(self, path=None, srid=4326):
        """Import Vector into Postgis Table

        -- Enable PostGIS (includes raster)
        CREATE EXTENSION postgis;

        -- Enable Topology
        CREATE EXTENSION postgis_topology;

        -- fuzzy matching needed for Tiger
        CREATE EXTENSION fuzzystrmatch;

        -- Enable US Tiger Geocoder
        CREATE EXTENSION postgis_tiger_geocoder;
        Uses shp2pgsql -I -s <SRID> <PATH/TO/SHAPEFILE> <SCHEMA>.<DBTABLE>
        | psql -U postgres -d <DBNAME>>

        The sql processed by shp2pgsql is run
        as  psql -U postgres -d <DBNAME>>
         """
        if not path:
            path = Engine.format_data_dir(self)
        raster_sql = "shp2pgsql -I -s {SRID} {path} {SCHEMA_DBTABLE}".format(
            SRID=srid,
            path=path, SCHEMA_DBTABLE=self.table_name())

        cmd_string = """ | psql -U {USER} -d {DATABASE}""".format(
            USER=self.opts["user"],
            DATABASE=self.opts["database"])
        print(raster_sql + cmd_string)
        os.system(raster_sql + cmd_string)

    def format_insert_value(self, value, datatype):
        """Format value for an insert statement."""
        if datatype == "bool":
            try:
                if int(value) == 1:
                    return "TRUE"
                elif int(value) == 0:
                    return "FALSE"
            except BaseException:
                pass
        return Engine.format_insert_value(self, value, datatype)

    def get_connection(self):
        """Gets the db connection.

        Please update the encoding lookup table if the required encoding is not present.
        """
        import psycopg2 as dbapi
        self.get_input()
        conn = dbapi.connect(host=self.opts["host"],
                             port=int(self.opts["port"]),
                             user=self.opts["user"],
                             password=self.opts["password"],
                             database=self.opts["database"])
        encoding = ENCODING.lower()
        if self.script.encoding:
            encoding = self.script.encoding.lower()
        encoding_lookup = {
            'iso-8859-1': 'Latin1',
            'latin-1': 'Latin1',
            'utf-8': 'UTF8'}
        db_encoding = encoding_lookup.get(encoding)
        conn.set_client_encoding(db_encoding)
        return conn
