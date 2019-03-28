import os

from pandas import HDFStore

from retriever.lib.defaults import DATA_DIR
from retriever.lib.dummy import DummyConnection
from retriever.lib.models import Engine


class engine(Engine):
    """Engine instance for writing data to a HDF5 file."""

    name = "HDF5"
    abbreviation = "hdf5"
    insert_limit = 1000
    required_opts = [
        ("file",
         "Enter the filename of your HDF5 file",
         "hdf5.h5"),
        ("table_name",
         "Format of table name",
         "{db}_{table}"),
        ("data_dir",
         "Install directory",
         DATA_DIR),
    ]

    def create_db(self):
        """Override create_db since an SQLite dataset needs to be created
        first followed by the creation of an empty HDFStore file.
        """
        from retriever.engines.sqlite import engine

        self.dbname = self.script.name.lower()
        self.sqlite_engine = engine()
        self.sqlite_engine.opts = {"file": self.opts["file"].split(".")[0] + ".db",
                                   "table_name": self.opts["table_name"],
                                   "data_dir": self.opts["data_dir"]}
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
        df = self.sqlite_engine.fetch_table(table_name)
        self.file.put(table_name, df, data_columns=True)

    def get_connection(self):
        """Gets the db connection."""
        self.get_input()
        return DummyConnection()

    def disconnect(self):
        """Close the file after being written"""
        self.file.close()
