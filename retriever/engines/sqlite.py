import os
import sys
from builtins import range
from osgeo import gdal, gdalconst
from osgeo import ogr
import csv
import sqlite3

#sys.path.insert(0,"/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages")

"""Importing GDAL/OGR module from OSGEO (suppports only Python2)"""

# try:
#     import gdal, ogr
#     print(gdal.__version__)
#     #gdal.UseExceptions()

# except:
#     sys.exit("ERROR: OSGeo not installed... \
#     \nDownload from here => http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries")

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
                      os.path.join(DATA_DIR, "sqlite.db"),
                      ""),
                     ("table_name",
                      "Format of table name",
                      "{db}_{table}"),
                     ]

    file_name = None

    def auto_create_table(self, table, url=None, filename=None, pk=None):

        if table.dataset_type == "RasterDataset":

            self.table = table
            if url and not filename:
                filename = Engine.filename_from_url(url)

            if url and not self.find_file(filename):
                # If the file doesn't exist, download it
                self.download_file(url, filename)

            file_path = self.find_file(filename)
            filename, file_extension = os.path.splitext(os.path.basename(file_path))
            self.file_name = filename

        else:
            Engine.auto_create_table(self, table, url, filename, pk)


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

        if not path:
            path = Engine.format_data_dir(self)

        # df = gdal.Open(path)
        #
        # for band in range(1,df.RasterCount+1):
        #
        #     os.system("gdal_translate -b {} -of XYZ {} {}.csv \
        #             -co ADD_HEADER_LINE=YES".format(band, path, path))
        #
        #     os.system("ogr2ogr -update -append -f SQLite sqlite.db \
        #             -nln {}_band_{} {}.csv -dsco METADATA=NO \
        #             -dsco INIT_WITH_EPSG=NO".format(self.file_name,band, path))
        #
        #     os.system("rm {}.csv".format(path))

        dest = sqlite3.connect("sqlite.db")
        cur = dest.cursor()

        print("Working with {}".format(path))

        data = gdal.OpenShared(path, gdalconst.GA_ReadOnly)

        GeoTrans = data.GetGeoTransform()

        ColRange = range(data.RasterXSize)
        RowRange = range(data.RasterYSize)

        for band in range(1, data.RasterCount+1):

            rBand = data.GetRasterBand(band)
            nData = rBand.GetNoDataValue()

            if nData == None:
                nData = -9999
            else:
                print("NoData Value: {}".format(nData))

            HalfX = GeoTrans[1] / 2
            HalfY = GeoTrans[5] / 2

            sql = "DROP TABLE IF EXISTS {}_band{}".format(self.file_name,band)
            cur.execute(sql)

            print("Creating table {}_band{}".format(self.file_name,band))

            create_stmt = "CREATE TABLE {}_band{} (x INT,y INT,z INT);".format(self.file_name, band)
            cur.execute(create_stmt)

            # sys.exit("Done with a table")

            print("Inserting values to {}_band{}".format(self.file_name, band))

            for row in RowRange:
                    RowData = rBand.ReadAsArray(0, row, data.RasterXSize, 1)[0]
                    for col in ColRange:
                        if RowData[col] != nData:
                            if RowData[col] > 0:
                                X = GeoTrans[0] + ( col * GeoTrans[1] )
                                Y = GeoTrans[3] + ( row * GeoTrans[5] )
                                X += HalfX
                                Y += HalfY

                                insert_stmt = """INSERT INTO {}_band{}(x, y, z) VALUES(?, ?, ?);""".format(self.file_name, band)
                                cur.execute(insert_stmt, (int(X), int(Y), int(RowData[col])))

            dest.commit()

            print("End of insertion to {}_band{}".format(self.file_name, band))

            # sys.exit("Done with a table")

            dest.close()

    def insert_vector(self,path=None, srid=4326):

        if not path:
            path = Engine.format_data_dir(self)

        vector_file = ogr.Open(path,0)
        n_layers = vector_file.GetLayerCount()

        for i in range(0,n_layers):
            shape = vector_file.GetLayer(i)
            layer_definition = shape.GetLayerDefn()
            fields = list()

            for i in range(layer_definition.GetFieldCount()):
                fields.append(layer_definition.GetFieldDefn(i).GetName())

            field_list = ','.join(fields)

            os.system("ogr2ogr -append -select {} -overwrite \
            -f 'sqlite' sqlite.db {}".format(field_list, path))

        vector_file.close()


        #os.system("ogr2ogr -f 'sqlite' sqlite.db {}".format(path))

        # os.system("ogr2ogr -overwrite -progress -f csv '{}/{}' '{}'.shp".format(path, self.file_name, path))
        #
        # conn = dbapi.connect("sqlite.db")
        # conn.text_factory = str #allow utf-8 data to be stored
        # cur = conn.cursor()
        #
        # file = "{}/{}/{}.csv".format(path,self.file_name,self.file_name)

        # with open(file,"r") as f:
        #     reader = csv.reader(f)
        #     header = True
        #     for row in reader:
        #         if header:
        #         # gather column names from the first row of the csv
        #         header = False
        #
        #         sql = "DROP TABLE IF EXISTS {}".format(self.file_name)
        #         cur.execute(sql)
        #
        #         list = list(str(column) for column in row)
        #         separator = ", "
        #         head = separator.join(list)
        #
        #         sql = "CREATE TABLE {} ({})".format(self.file_name, head)
        #         cur.execute(sql)
        #
        #         for column in row:
        #             if column.lower().endswith("_id"):
        #                 index = "{}__{}".format(self.file_name, column)
        #                 sql = "CREATE INDEX {} on {} ({})".format( index, self.file_name, column )
        #                 c.execute(sql)
        #
        #         list = list("?" for column in row)
        #         separator = ", "
        #         head = separator.join(list)
        #
        #         insertsql = "INSERT INTO {} VALUES ({})".format(self.file_name, head)
        #
        #         rowlen = len(row)
        #
        #     else:
        #         # skip lines that don't have the right number of columns
        #         if len(row) == rowlen:
        #             c.execute(insertsql, row)
        #
        # conn.commit()
        #
        # c.close()
        # conn.close()

    def create_db(self):
        """Don't create database for SQLite

        SQLite doesn't create databases. Each database is a file and needs a separate
        connection. This overloads`create_db` to do nothing in this case.
        """

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
        for i in range(0, column_count):
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

    def table_exists(self, dbname, tablename):

        """Determine if the table already exists in the database."""
        if not hasattr(self, 'existing_table_names'):
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            self.existing_table_names = set()
            for line in self.cursor:
                self.existing_table_names.add(line[0].lower())
        return self.table_name(name=tablename, dbname=dbname).lower() in self.existing_table_names

    def get_connection(self):
        """Get db connection."""
        import sqlite3 as dbapi
        self.get_input()
        return dbapi.connect(self.opts["file"])
