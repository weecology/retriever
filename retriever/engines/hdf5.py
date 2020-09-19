import os

import pandas as pd
from pandas import HDFStore
import sqlite3 as dbapi

from retriever.lib.defaults import DATA_DIR
from retriever.lib.dummy import DummyConnection
from retriever.lib.models import Engine


class engine(Engine):
    """Engine instance for writing data to a HDF5 file."""

    name = "HDF5"
    abbreviation = "hdf5"
    insert_limit = 1000
    required_opts = [
        ("file", "Enter the filename of your HDF5 file", "hdf5.h5"),
        ("table_name", "Format of table name", "{db}_{table}"),
        ("data_dir", "Install directory", DATA_DIR),
    ]

    def create_db(self):
        """Override create_db since an SQLite dataset needs to be created
        first followed by the creation of an empty HDFStore file.
        """
        file_path = os.path.join(self.opts["data_dir"], self.opts["file"])
        self.file = HDFStore(file_path)

    def create_table(self):
        """Don't create table for HDF5

        HDF5 doesn't create tables. Each database is a file which has been
        created. This overloads`create_table` to do nothing in this case.
        """
        return None

    def insert_data_from_file(self, filename):
        """Fill the table by fetching the dataframe from the
        SQLite engine and putting it into the HDFStore file.
        """
        table_name = self.table_name()
        df = self.fetch_table(table_name)
        self.file.put(table_name, df, data_columns=True)

    def fetch_table(self, table_name):
        """Return a table from sqlite dataset as pandas dataframe."""
        connection = self.get_sqlite_connection()
        sql_query = "SELECT * FROM {};".format(table_name)
        return pd.read_sql_query(sql_query, connection)

    def get_sqlite_connection(self):
        # self.get_input()
        file = self.opts["file"]
        file = (file.split("."))[0] + ".db"
        db_file = self.opts["data_dir"]
        full_path = os.path.join(db_file, file)
        return dbapi.connect(os.path.normpath(full_path))

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()

    def disconnect(self):
        """Close the file after being written"""
        self.file.close()
        file = self.opts["file"]
        file = (file.split("."))[0] + ".db"
        os.remove(file)
