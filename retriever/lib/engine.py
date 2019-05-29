from __future__ import division
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
from builtins import object
from builtins import range
from builtins import input
from builtins import zip
from builtins import next
from builtins import str
import os
import getpass
import zipfile
import gzip
import tarfile
import csv
import re
import requests
from collections import OrderedDict
from math import ceil
from tqdm import tqdm
from retriever.lib.tools import open_fr, open_fw, open_csvw, walk_relative_path
from setuptools import archive_util
from retriever.lib.defaults import DATA_DIR, DATA_SEARCH_PATHS, DATA_WRITE_PATH, ENCODING
from retriever.lib.cleanup import no_cleanup
from retriever.lib.warning import Warning
from urllib.request import urlretrieve
from requests.exceptions import InvalidSchema


class Engine(object):
    """A generic database system. Specific database platforms will inherit
    from this class."""

    _connection = None
    _cursor = None
    datatypes = []
    db = None
    debug = False
    instructions = "Enter your database connection information:"
    name = ""
    pkformat = "%s PRIMARY KEY %s "
    placeholder = None
    required_opts = []
    script = None
    spatial_support = False
    table = None
    use_cache = True
    warnings = []
    script_table_registry = OrderedDict()
    encoding = None

    def connect(self, force_reconnect=False):
        """Create a connection."""
        if force_reconnect:
            self.disconnect()

        if self._connection is None:
            self._connection = self.get_connection()

        return self._connection

    connection = property(connect)

    def disconnect(self):
        """Disconnect a connection."""
        if self._connection:
            self.connection.close()
            self._connection = None
            self._cursor = None

    def disconnect_files(self):
        """Files systems should override this method.

        Enables commit per file object.
        """
        pass

    def get_connection(self):
        """This method should be overridden by specific implementations
        of Engine."""
        raise NotImplementedError

    def add_to_table(self, data_source):
        """Adds data to a table from one or more lines specified
        in engine.table.source."""
        if self.table.columns[-1][1][0][:3] == "ct-":
            # cross-tab data
            real_line_length = self.get_ct_line_length(
                gen_from_source(data_source))

            real_lines = self.get_ct_data(
                gen_from_source(data_source))
        else:
            real_lines = gen_from_source(data_source)
            len_source = gen_from_source(data_source)
            real_line_length = sum(1 for _ in len_source)

        total = self.table.record_id + real_line_length
        count_iter = 1
        insert_limit = self.insert_limit
        types = self.table.get_column_datatypes()
        multiple_values = []
        progress_bar = tqdm(
            desc='Installing {}'.format(self.table_name()),
            total=total,
            unit='rows')

        line_values = None
        for line in real_lines:
            if line:
                # Only process non empty lines
                self.table.record_id += 1
                line_values = self.table.values_from_line(line)
                # Build insert statement with the correct number of values
                try:
                    clean_values = [
                        self.format_insert_value(
                            self.table.cleanup.function(
                                line_values[n],
                                self.table.cleanup.args),
                            types[n])
                        for n in range(len(line_values))
                        ]
                except Exception as e:
                    self.warning(
                        'Exception in line {}: {}'
                        .format(self.table.record_id, e))
                    continue

            if line or count_iter == real_line_length:
                if count_iter % insert_limit == 0 or count_iter == real_line_length:
                    # Add values to the list multiple_values
                    # if multiple_values list is full
                    # or we reached the last value in real_line_length
                    # execute the values in multiple_values
                    multiple_values.append(clean_values)
                    try:
                        insert_stmt = self.insert_statement(multiple_values)
                    except Exception as _:
                        if self.debug:
                            print(types)
                        if self.debug:
                            print(line_values)
                        if self.debug:
                            print(clean_values)
                        raise
                    try:
                        self.executemany(insert_stmt,
                                         multiple_values,
                                         commit=False)
                    except BaseException:
                        print(insert_stmt)
                        raise
                    multiple_values = []
                else:
                    multiple_values.append(clean_values)
            progress_bar.update()
            count_iter += 1
        progress_bar.close()
        self.connection.commit()

    def get_ct_line_length(self, lines):
        """Returns the number of real lines for cross-tab data"""
        real_line_length = 0
        for values in lines:
            initial_cols = len(self.table.columns) - \
                           (3 if hasattr(self.table, "ct_names") else 2)
            # add one if auto increment is not
            # set to get the right initial columns
            if not self.table.columns[0][1][0] == "pk-auto":
                initial_cols += 1
            rest = values[initial_cols:]
            real_line_length += len(rest)

        return real_line_length

    def get_ct_data(self, lines):
        """Create cross tab data."""
        for values in lines:
            initial_cols = len(self.table.columns) - \
                           (3 if hasattr(self.table, "ct_names") else 2)
            # add one if auto increment is not set to get the right initial columns
            if not self.table.columns[0][1][0] == "pk-auto":
                initial_cols += 1
            begin = values[:initial_cols]
            rest = values[initial_cols:]
            n = 0
            for item in rest:
                if hasattr(self.table, "ct_names"):
                    name = [self.table.ct_names[n]]
                    n += 1
                else:
                    name = []
                yield (begin + name + [item])

    def auto_create_table(self, table, url=None, filename=None, pk=None, make=True):
        """Create table automatically by analyzing a data source and
        predicting column names, data types, delimiter, etc."""
        if url and not filename:
            filename = filename_from_url(url)
        self.table = table

        if url and not self.find_file(filename):
            # If the file doesn't exist, download it
            self.download_file(url, filename)
        file_path = self.find_file(filename)

        if not self.table.delimiter:
            self.set_table_delimiter(file_path)

        if self.table.header_rows > 0 and not self.table.columns:
            source = (skip_rows,
                      (self.table.header_rows - 1, self.load_data(file_path)))

            lines = gen_from_source(source)
            header = next(lines)
            lines.close()

            source = (skip_rows,
                      (self.table.header_rows, self.load_data(file_path)))

            lines = gen_from_source(source)
            columns, _ = self.table.auto_get_columns(header)
            self.auto_get_datatypes(pk, lines, columns)

        if self.table.columns[-1][1][0][:3] == "ct-" \
                and hasattr(self.table, "ct_names") \
                and self.table.ct_column not in [c[0] for c in self.table.columns]:
            self.table.columns = self.table.columns[:-1] + \
                                 [(self.table.ct_column, ("char", 50))] + \
                                 [self.table.columns[-1]]
        if not make:
            return self.table
        self.create_table()

    def auto_get_datatypes(self, pk, source, columns):
        """Determine data types for each column.

        For string columns adds an additional 100 characters to the maximum
        observed value to provide extra space for cases where special characters
        are counted differently by different engines.

        """
        # Get all values for each column
        lines_to_scan = source
        # set default column data types as int
        column_types = [('int',)] * len(columns)
        max_lengths = [0] * len(columns)

        # Check the values for each column to determine data type
        for values in lines_to_scan:
            if values:
                for i in range(len(columns)):
                    try:
                        val = u"{}".format(values[i])

                        if self.table.cleanup.function != no_cleanup:
                            val = self.table.cleanup.function(
                                val, self.table.cleanup.args)

                        if val and val.strip():
                            if len(str(val)) + 100 > max_lengths[i]:
                                max_lengths[i] = len(str(val)) + 100

                            if column_types[i][0] in ('int', 'bigint'):
                                try:
                                    val = int(val)
                                    if column_types[i][0] == 'int' and \
                                            hasattr(self, 'max_int') and \
                                            val > self.max_int:
                                        column_types[i] = ['bigint', ]
                                except Exception as _:
                                    column_types[i] = ['double', ]
                            if column_types[i][0] == 'double':
                                try:
                                    val = float(val)
                                    if "e" in str(val) or ("." in str(val) and len(str(val).split(".")[1]) > 10):
                                        column_types[i] = ["decimal", "50,30"]
                                except Exception as _:
                                    column_types[i] = ['char', max_lengths[i]]
                            if column_types[i][0] == 'char':
                                if len(str(val)) + 100 > column_types[i][1]:
                                    column_types[i][1] = max_lengths[i]
                    except IndexError:
                        pass
        for i, value in enumerate(columns):
            column = value
            column[1] = column_types[i]
            if pk == column[0]:
                column[1][0] = "pk-" + column[1][0]
        if pk is None and columns[0][1][0] == 'pk-auto':
            self.table.columns = [("record_id", ("pk-auto",))]
            self.table.contains_pk = True
        else:
            self.table.columns = []

        for column in columns:
            self.table.columns.append((column[0], tuple(column[1])))

    def auto_get_delimiter(self, header):
        """Determine the delimiter.

        Find out which of a set of common delimiters occurs most in the header
        line and use this as the delimiter.

        """
        self.table.delimiter = "\t"
        for other_delimiter in [",", ";"]:
            if header.count(other_delimiter) > header.count(self.table.delimiter):
                self.table.delimiter = other_delimiter

    def convert_data_type(self, datatype):
        """Convert Retriever generic data types to database platform specific
        data types.
        """
        # get the type from the dataset variables
        key = datatype[0]
        this_pk = False
        if key[0:3] == "pk-":
            key = key[3:]
            this_pk = True
        elif key[0:3] == "ct-":
            key = key[3:]

        # format the dataset type to match engine specific type
        this_type = ""
        if key in list(self.datatypes.keys()):
            this_type = self.datatypes[key]
            if isinstance(this_type, tuple):
                if datatype[0] == 'pk-auto':
                    pass
                elif len(datatype) > 1:
                    this_type = this_type[1] + "(" + str(datatype[1]) + ")"
                else:
                    this_type = this_type[0]
            else:
                if len(datatype) > 1:
                    this_type += "(" + str(datatype[1]) + ")"

        # set the PRIMARY KEY
        if this_pk:
            if isinstance(this_type, tuple):
                this_type = self.pkformat % this_type
            else:
                this_type = self.pkformat % (this_type, "")
        return this_type

    def create_db(self):
        """Create a new database based on settings supplied in Database object
        engine.db."""
        db_name = self.database_name()
        if db_name:
            print("Creating database " + db_name + "...\n")
            # Create the database
            create_stmt = self.create_db_statement()
            if self.debug:
                print(create_stmt)
            try:
                self.execute(create_stmt)
            except Exception as e:
                try:
                    self.connection.rollback()
                except Exception as _:
                    pass
                print(e)
                print("Installing into existing database")

    def create_db_statement(self):
        """Return SQL statement to create a database."""
        create_stmt = "CREATE DATABASE " + self.database_name()
        return create_stmt

    def create_raw_data_dir(self, path=None):
        """Check to see if the archive directory exists and creates it if
        necessary."""
        if not path:
            path = self.format_data_dir()
        if not os.path.exists(path):
            os.makedirs(path)

    def create_table(self):
        """Create new database table based on settings supplied in Table
        object engine.table."""

        # Try to drop the table if it exists; this may cause an exception if it
        # doesn't exist, so ignore exceptions
        try:
            self.execute(self.drop_statement("TABLE", self.table_name()))
        except Exception as _:
            pass

        create_stmt = self.create_table_statement()
        if self.debug:
            print(create_stmt)
        try:
            self.execute(create_stmt)
            self.register_tables()

            if self.table.name not in self.script.tables:
                self.script.tables[self.table.name] = self.table
        except Exception as e:
            try:
                self.connection.rollback()
            except Exception as _:
                pass
            print(e)
            print("Replacing existing table")

    def register_tables(self):
        if self.script.name not in self.script_table_registry:
            self.script_table_registry[self.script.name] = []
        self.script_table_registry[self.script.name].append(
            (self.table_name(), self.table)
        )

    def create_table_statement(self):
        """Return SQL statement to create a table."""
        create_stmt = "CREATE TABLE " + self.table_name() + " ("
        columns = self.table.get_insert_columns(join=False, create=True)
        types = []
        for column in self.table.columns:
            for column_name in columns:
                if column[0] == column_name:
                    types.append(self.convert_data_type(column[1]))
        if self.debug:
            print(columns)

        column_strings = []
        for c, t in zip(columns, types):
            column_strings.append(c + ' ' + t)

        create_stmt += ', '.join(column_strings)
        create_stmt += " );"

        return create_stmt

    def database_name(self, name=None):
        """Return name of the database."""
        if not name:
            try:
                name = self.script.name
            except AttributeError:
                name = "{db}"
        try:
            db_name = self.opts["database_name"].format(db=name)
        except KeyError:
            db_name = name
        return db_name.replace('-', '_')

    def download_file(self, url, filename):
        """Download file to the raw data directory."""
        if not self.find_file(filename) or not self.use_cache:
            path = self.format_filename(filename)
            self.create_raw_data_dir()
            progbar = tqdm(unit='B',
                           unit_scale=True,
                           unit_divisor=1024,
                           miniters=1,
                           desc='Downloading {}'.format(filename))
            try:
                requests.get(url, allow_redirects=True,
                             stream=True,
                             headers={'user-agent': 'Weecology/Data-Retriever \
                                            Package Manager: http://www.data-retriever.org/'},
                             hooks={'response': reporthook(progbar, path)})

            except InvalidSchema:
                urlretrieve(url, path, reporthook=reporthook(progbar))

            self.use_cache = True
            progbar.close()

    def download_files_from_archive(self, url,
                                    file_names=None, archive_type="zip",
                                    keep_in_dir=False, archive_name=None):
        """Download files from an archive into the raw data directory."""

        if not archive_name:
            archive_name = filename_from_url(url)
        else:
            archive_name = self.format_filename(archive_name)

        archive_full_path = self.format_filename(archive_name)
        archive_dir = self.format_data_dir()
        if keep_in_dir:
            archive_base = os.path.splitext(os.path.basename(archive_name))[0]
            archive_dir = os.path.join(DATA_WRITE_PATH, archive_base)
            archive_dir = archive_dir.format(dataset=self.script.name)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

        if not file_names:
            self.download_file(url, archive_name)
            if archive_type == 'tar' or archive_type == 'tar.gz':
                file_names = self.extract_tar(
                    archive_full_path, archive_dir, archive_type)
            elif archive_type == 'zip':
                file_names = self.extract_zip(archive_full_path, archive_dir)
            elif archive_type == 'gz':
                file_names = self.extract_gz(archive_full_path, archive_dir)
            return file_names

        archive_downloaded = False
        for file_name in file_names:
            archive_full_path = self.format_filename(archive_name)
            if not self.find_file(os.path.join(archive_dir, file_name)):
                # if no local copy, download the data
                self.create_raw_data_dir()
                if not archive_downloaded:
                    self.download_file(url, archive_name)
                    archive_downloaded = True
                if archive_type == 'zip':
                    self.extract_zip(archive_full_path, archive_dir, file_name)
                elif archive_type == 'gz':
                    self.extract_gz(archive_full_path, archive_dir, file_name)
                elif archive_type == 'tar' or archive_type == 'tar.gz':
                    self.extract_tar(archive_full_path,
                                     archive_dir,
                                     archive_type,
                                     file_name)
        return file_names

    def drop_statement(self, object_type, object_name):
        """Return drop table or database SQL statement."""
        if self:
            drop_statement = "DROP %s IF EXISTS %s" % (
                object_type, object_name)
        return drop_statement

    def execute(self, statement, commit=True):
        """Execute given statement."""
        self.cursor.execute(statement)
        if commit:
            self.connection.commit()

    def executemany(self, statement, values, commit=True):
        """Execute given statement with multiple values."""
        self.cursor.executemany(statement, values)
        if commit:
            self.connection.commit()

    def extract_gz(self, archive_path, archivedir_write_path, file_name=None,
                   open_archive_file=None, archive=None):
        """Extract gz files.

        Extracts a given file name or all the files in the gz.
        """
        if file_name:
            open_archive_file = gzip.open(archive_path, 'r')
            file_obj = open_archive_file
            open_object = False
            self.write_fileobject(archivedir_write_path,
                                  file_name,
                                  file_obj=open_archive_file,
                                  open_object=False)
            if 'archive' in locals() and archive:
                archive.close()
            return [file_name]
        files_before = set(walk_relative_path(archivedir_write_path))
        archive_util.unpack_archive(archive_path, archivedir_write_path)
        files_after = set(walk_relative_path(archivedir_write_path))
        unpacked_files = files_after - files_before
        return list(unpacked_files)

    def extract_tar(self, archive_path,
                    archivedir_write_path,
                    archive_type,
                    file_name=None):
        """Extract tar or tar.gz files.

        Extracts a given file name or the file in the tar or tar.gz.
        # gzip archives can only contain a single file
        """
        if archive_type == 'tar' or archive_type == 'tar.gz':
            if file_name:
                archive = tarfile.open(archive_path, 'r')
                open_archive_file = archive.extractfile(file_name)

                self.write_fileobject(archivedir_write_path,
                                      file_name,
                                      file_obj=open_archive_file,
                                      open_object=False)
                if 'archive' in locals():
                    archive.close()
                return [file_name]
            else:
                if archive_type == 'tar':
                    tar = tarfile.open(archive_path, 'r')
                else:
                    tar = tarfile.open(archive_path, "r:gz")
                file_names = tar.getnames()
                tar.extractall(path=archivedir_write_path)
                tar.close()
                return file_names

    def extract_zip(self, archive_path, archivedir_write_path, file_name=None):
        """Extract zip files.

         Extracts a given file name or the entire files in the archive.
        """
        try:
            archive = zipfile.ZipFile(archive_path)
            if file_name:
                if archive.testzip():
                    archive.getinfo(file_name).file_size += (2 ** 64) - 1
                open_archive_file = archive.open(file_name, 'r')
                file_names = [file_name]
                archive = None
                file_obj = open_archive_file
                open_object = False
            else:
                file_names = [paths.filename
                              for paths in archive.infolist()
                              if not paths.filename.endswith('/')]
                file_obj = None
                open_object = True

            for fname in file_names:
                self.write_fileobject(archivedir_write_path, fname,
                                      file_obj,
                                      archive,
                                      open_object)
            return file_names
        except zipfile.BadZipFile as e:
            print("\n{0} can't be extracted, "
                  "may be corrupt \n{1}".format(file_name, e))

    def fetch_tables(self, table_names):
        """This can be overriden to return the tables of sqlite db
        as pandas data frame. Return False by default.
        """
        return False

    def final_cleanup(self):
        """Close the database connection."""
        if self.warnings:
            print('\n'.join(str(w) for w in self.warnings))

        self.disconnect()

    def find_file(self, filename):
        """Check for an existing datafile."""
        for search_path in DATA_SEARCH_PATHS:
            search_path = search_path.format(dataset=self.script.name) if self.script else search_path
            file_path = os.path.normpath(os.path.join(search_path, filename))
            if file_exists(file_path):
                return file_path
        return False

    def format_data_dir(self):
        """Return correctly formatted raw data directory location."""
        return DATA_WRITE_PATH.format(dataset=self.script.name)

    def format_filename(self, filename):
        """Return full path of a file in the archive directory."""
        return os.path.join(self.format_data_dir(), filename)

    def format_insert_value(self, value, datatype):
        """Format a value for an insert statement based on data type.

        Different data types need to be formated differently to be properly
        stored in database management systems. The correct formats are
        obtained by:

        1. Removing extra enclosing quotes
        2. Harmonizing null indicators
        3. Cleaning up badly formatted integers
        4. Obtaining consistent float representations of decimals
        """
        datatype = datatype.split('-')[-1]
        str_value = str(value).strip()

        # Remove any quotes already surrounding the string
        quotes = ["'", '"']
        if len(str_value) > 1 and str_value[0] == str_value[-1] and str_value[0] in quotes:
            str_value = str_value[1:-1]
        missing_values = ("null", "none")
        if str_value.lower() in missing_values:
            return None
        if datatype in ("int", "bigint", "bool"):
            if str_value:
                intvalue = str_value.split('.')[0]
                if intvalue:
                    return int(intvalue)
                return None
            return None
        if datatype in ("double", "decimal"):
            if str_value.strip():
                try:
                    decimals = float(str(str_value))
                    return decimals
                except Exception as _:
                    return None
            return None
        if datatype == "char":
            if str_value.lower() in missing_values:
                return None
            return str_value
        return None

    def get_cursor(self):
        """Get db cursor."""
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    cursor = property(get_cursor)

    def get_input(self):
        """Manually get user input for connection information when script is
        run from terminal."""
        for opt in self.required_opts:
            if not (opt[0] in list(self.opts.keys())):
                if opt[0] == "password":
                    print(opt[1])
                    self.opts[opt[0]] = getpass.getpass(" ")
                else:
                    prompt = opt[1]
                    if opt[2]:
                        prompt += " or press Enter for the default, %s" % opt[2]
                    prompt += ': '
                    self.opts[opt[0]] = input(prompt)
            if self.opts[opt[0]] in ["", "default"]:
                self.opts[opt[0]] = opt[2]
        if 'data_dir' in self.opts and self.opts['data_dir']:
            if self.opts['data_dir'] != DATA_DIR:
                if not os.path.exists(self.opts['data_dir']):
                    os.makedirs(self.opts['data_dir'])

    def insert_data_from_archive(self, url, filenames):
        """Insert data from files located in an online archive. This function
        extracts the file, inserts the data, and deletes the file if raw data
        archiving is not set."""
        self.download_files_from_archive(url, filenames)
        for filename in filenames:
            file_path = self.find_file(filename)
            if file_path:
                self.insert_data_from_file(file_path)
            else:
                raise Exception("File not found: %s" % filename)

    def insert_data_from_file(self, filename):
        """The default function to insert data from a file. This function
        simply inserts the data row by row. Database platforms with support
        for inserting bulk data from files can override this function."""
        data_source = (skip_rows,
                       (self.table.header_rows,
                        (self.load_data, (filename,))))
        self.add_to_table(data_source)

    def insert_data_from_url(self, url):
        """Insert data from a web resource, such as a text file."""
        filename = filename_from_url(url)
        find = self.find_file(filename)
        if find and self.use_cache:
            # Use local copy
            self.insert_data_from_file(find)
        else:
            # Save a copy of the file locally, then load from that file
            self.create_raw_data_dir()
            print("\nSaving a copy of " + filename + "...")
            self.download_file(url, filename)
            self.insert_data_from_file(self.find_file(filename))

    def insert_raster(self, path=None, srid=None):
        """Base function for installing raster data from path"""
        pass

    def insert_statement(self, values):
        """Return SQL statement to insert a set of values."""
        columns = self.table.get_insert_columns()
        types = self.table.get_column_datatypes()
        column_count = len(
            self.table.get_insert_columns(
                join=False, create=False))
        for row in values:
            row_length = len(row)
            # Add None with appropriate value type for empty cells
            for i in range(column_count - row_length):
                row.append(self.format_insert_value(
                    None, types[row_length + i]))

        insert_stmt = "INSERT INTO {table}".format(table=self.table_name())
        insert_stmt += " ( {columns} )".format(columns=columns)
        insert_stmt += " VALUES ("
        for i in range(0, column_count):
            insert_stmt += "{}, ".format(self.placeholder)
        insert_stmt = insert_stmt.rstrip(", ") + ")"

        if self.debug:
            print(insert_stmt)
        return insert_stmt

    def insert_vector(self, path=None, srid=None):
        """Base function for installing vector data from path"""
        pass

    def set_engine_encoding(self):
        """Set up the encoding to be used."""
        self.encoding = ENCODING.lower()
        if self.script and self.script.encoding:
                self.encoding = self.script.encoding.lower()

    def set_table_delimiter(self, file_path):
        """Get the delimiter from the data file and set it."""
        if os.name == "nt":
            dataset_file = open_fr(file_path)
        else:
            dataset_file = open_fr(file_path, encoding=self.encoding)
        self.auto_get_delimiter(dataset_file.readline())
        dataset_file.close()

    def supported_raster(self, path, ext=None):
        """"Spatial data is not currently supported for this database type
        or file format. PostgreSQL is currently the only supported output
        for spatial data."""
        if self:
            raise Exception("Not supported")

    def table_name(self, name=None, dbname=None):
        """Return full table name."""
        if not name:
            name = self.table.name
        if not dbname:
            dbname = self.database_name()
            if not dbname:
                dbname = ''
        return self.opts["table_name"].format(db=dbname, table=name)

    def to_csv(self, sort=True, path=None, select_columns=None):
        """Create a CSV file from the a data store.

        sort flag to create a sorted file,
        path to write the flag else write to the PWD,
        select_columns flag is used by large files to select
        columns data and has SELECT LIMIT 3.
        """
        # Due to Cyclic imports we can not move this import to the top
        from retriever.lib.engine_tools import sort_csv

        for table_name in self.script_table_registry[self.script.name]:

            csv_file_output = os.path.normpath(os.path.join(path if path else '',
                                                            table_name[0] + '.csv'))
            self.get_cursor()
            self.set_engine_encoding()
            csv_file = open_fw(csv_file_output, encoding=self.encoding)
            csv_writer = open_csvw(csv_file)

            limit = ""
            cols = "*"
            if select_columns:
                limit = "LIMIT 3"
                cols = ",".join(select_columns)
            sql_query = "SELECT {cols} FROM  {tab} {limit};"
            self.cursor.execute(sql_query.format(cols=cols, tab=table_name[0], limit=limit))
            row = self.cursor.fetchone()
            column_names = [u'{}'.format(tuple_i[0])
                            for tuple_i in self.cursor.description]
            csv_writer.writerow(column_names)
            while row is not None:
                csv_writer.writerow(row)
                row = self.cursor.fetchone()
            csv_file.close()
            if sort:
                sort_csv(csv_file_output)
        self.disconnect()

    def warning(self, warning):
        """Create a warning message using the current script and table."""
        new_warning = Warning('%s:%s' %
                              (self.script.name, self.table.name), warning)
        self.warnings.append(new_warning)

    def write_fileobject(self, archivedir_write_path,
                         file_name,
                         file_obj=None,
                         archive=None,
                         open_object=False):
        """Write a file object from a archive object to a given path

        open_object flag helps up with zip files, open the zip and the file
        """
        write_path = self.format_filename(os.path.join(archivedir_write_path,
                                                       file_name))
        write_path = os.path.normpath(write_path)
        if not os.path.exists(write_path):
            # If the directory does not exits, create it
            if not os.path.exists(os.path.dirname(write_path)):
                os.makedirs(os.path.dirname(write_path))
            unzipped_file = open(write_path, 'wb')
            if open_object:
                file_obj = archive.open(file_name, 'r')
            if file_obj:
                for line in file_obj:
                    unzipped_file.write(line)
                file_obj.close()
            unzipped_file.close()

    def load_data(self, filename):
        """Generator returning lists of values from lines in a data file.

        1. Works on both delimited (csv module)
        and fixed width data (extract_fixed_width)
        2. Identifies the delimiter if not known
        3. Removes extra line endings

        """
        if not self.table.delimiter:
            self.set_table_delimiter(filename)
        if os.name == "nt":
            dataset_file = open_fr(filename)
        else:
            dataset_file = open_fr(filename, encoding=self.encoding)
        if self.table.fixed_width:
            for row in dataset_file:
                yield self.extract_fixed_width(row)
        else:
            reg = re.compile("\\r\\n|\n|\r")
            for row in csv.reader(dataset_file,
                                  delimiter=self.table.delimiter):
                yield [reg.sub(" ", values) for values in row]

    def extract_fixed_width(self, line):
        """Split line based on the fixed width, returns list of the values."""
        pos = 0
        values = []
        for width in self.table.fixed_width:
            values.append(line[pos:pos + width].strip())
            pos += width
        return values


def skip_rows(rows, source):
    """Skip over the header lines by reading them before processing."""
    lines = gen_from_source(source)
    for _ in range(rows):
        next(lines)
    return lines


def file_exists(path):
    """Return true if a file exists and its size is greater than 0."""
    return os.path.isfile(path) and os.path.getsize(path) > 0


def filename_from_url(url):
    """Extract and returns the filename from the url."""
    return url.split('/')[-1].split('?')[0]


def gen_from_source(source):
    """Return generator from a source tuple.

    Source tuples are of the form (callable, args) where callable(\*args)
    returns either a generator or another source tuple.
    This allows indefinite regeneration of data sources.
    """
    while isinstance(source, tuple):
        gen, args = source
        source = gen(*args)
    return source


def reporthook(tqdm_inst, filename=None):
    """tqdm wrapper to generate progress bar for urlretriever"""
    last_block = [0]

    def update_to(count=1, block_size=1, total_size=None):
        if total_size is not None:
            tqdm_inst.total = total_size
        tqdm_inst.update((count - last_block[0]) * block_size)
        last_block[0] = count

    def update_rto(r, *args, **kwargs):
        if r.headers.get('Transfer-Encoding', None) != 'chunked':
            total_size = int(r.headers['content-length'])
            tqdm_inst.total = ceil(total_size // (2 * 1024))

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(2 * 1024):
                f.write(chunk)
                tqdm_inst.update(1)
        f.close()

    return update_rto if filename else update_to
