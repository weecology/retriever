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
import sys
import os
import getpass
import zipfile
import gzip
import tarfile
import csv
import re
import time
from tqdm import tqdm
from urllib.request import urlretrieve
from retriever.lib.tools import open_fr, open_fw, open_csvw
from retriever.lib.defaults import DATA_SEARCH_PATHS, DATA_WRITE_PATH, ENCODING
from retriever.lib.cleanup import no_cleanup
from retriever.lib.warning import Warning
from imp import reload

encoding = ENCODING.lower()
# sys removes the setdefaultencoding method at startup; reload to get it back
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(encoding)


class Engine(object):
    """A generic database system. Specific database platforms will inherit
    from this class."""

    name = ""
    instructions = "Enter your database connection information:"
    db = None
    table = None
    _connection = None
    _cursor = None
    datatypes = []
    required_opts = []
    pkformat = "%s PRIMARY KEY %s "
    script = None
    use_cache = True
    debug = False
    warnings = []

    def connect(self, force_reconnect=False):
        if force_reconnect:
            self.disconnect()

        if self._connection is None:
            self._connection = self.get_connection()

        return self._connection

    connection = property(connect)

    def disconnect(self):
        if self._connection:
            self.connection.close()
            self._connection = None
            self._cursor = None

    def get_connection(self):
        """This method should be overridden by specific implementations
        of Engine."""
        raise NotImplementedError

    def add_to_table(self, data_source):
        """This function adds data to a table from one or more lines specified
        in engine.table.source."""
        if self.table.columns[-1][1][0][:3] == "ct-":
            # cross-tab data
            real_line_length = self.get_ct_line_length(gen_from_source(data_source))
            real_lines = self.get_ct_data(gen_from_source(data_source))
        else:
            real_lines = gen_from_source(data_source)
            len_source = gen_from_source(data_source)
            real_line_length = sum(1 for _ in len_source)

        total = self.table.record_id + real_line_length
        count_iter = 1
        insert_limit = self.insert_limit
        types = self.table.get_column_datatypes()
        multiple_values = []
        progbar = tqdm(desc='Installing {}'.format(self.table_name()),
                       total=real_line_length,
                       unit='rows')
        for line in real_lines:
            if line:
                # Only process non empty lines
                self.table.record_id += 1
                linevalues = self.table.values_from_line(line)
                # Build insert statement with the correct number of values
                try:
                    cleanvalues = [self.format_insert_value(self.table.cleanup.function
                                                            (linevalues[n],
                                                             self.table.cleanup.args),
                                                            types[n])
                                   for n in range(len(linevalues))]
                except Exception as e:
                    self.warning('Exception in line %s: %s' % (self.table.record_id, e))
                    continue

            if line or count_iter == real_line_length:
                if count_iter % insert_limit == 0 or count_iter == real_line_length:
                    # Add values to the list multiple_values
                    # if multiple_values list is full or we reached the last value in real_line_length
                    # execute the values in multiple_values
                    multiple_values.append(cleanvalues)
                    try:
                        insert_stmt = self.insert_statement(multiple_values)
                    except:
                        if self.debug:
                            print(types)
                        if self.debug:
                            print(linevalues)
                        if self.debug:
                            print(cleanvalues)
                        raise
                    try:
                        self.executemany(insert_stmt, multiple_values, commit=False)
                        prompt = "Progress: {}/{} rows inserted into {} totaling {}:".format(
                            count_iter, real_line_length, self.table_name(), total)
                    except:
                        print(insert_stmt)
                        raise
                    multiple_values = []
                else:
                    multiple_values.append(cleanvalues)
            progbar.update()
            count_iter += 1
        progbar.close()
        self.connection.commit()

    def get_ct_line_length(self, lines):
        """Returns the number of real lines for cross-tab data"""
        real_line_length = 0
        for values in lines:
            initial_cols = len(self.table.columns) - \
                           (3 if hasattr(self.table, "ct_names") else 2)
            # add one if auto increment is not set to get the right initial columns
            if not self.table.columns[0][1][0] == "pk-auto":
                initial_cols += 1
            rest = values[initial_cols:]
            real_line_length = real_line_length + len(rest)

        return real_line_length

    def get_ct_data(self, lines):
        """Create cross tab data."""
        for values in lines:
            initial_cols = len(self.table.columns) - (3 if hasattr(self.table, "ct_names") else 2)
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

    def auto_create_table(self, table, url=None, filename=None, pk=None):
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

            columns, column_values = self.table.auto_get_columns(header)

            self.auto_get_datatypes(pk, lines, columns, column_values)

        if self.table.columns[-1][1][0][:3] == "ct-" \
                and hasattr(self.table, "ct_names") \
                and not self.table.ct_column in [c[0] for c in self.table.columns]:
            self.table.columns = self.table.columns[:-1] + \
                                 [(self.table.ct_column, ("char", 50))] + \
                                 [self.table.columns[-1]]

        self.create_table()

    def auto_get_datatypes(self, pk, source, columns, column_values):
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

                        if val is not None and val.strip() is not '':
                            if len(str(val)) + 100 > max_lengths[i]:
                                max_lengths[i] = len(str(val)) + 100

                            if column_types[i][0] in ('int', 'bigint'):
                                try:
                                    val = int(val)
                                    if column_types[i][0] == 'int' and hasattr(self, 'max_int') and val > self.max_int:
                                        column_types[i] = ['bigint', ]
                                except:
                                    column_types[i] = ['double', ]
                            if column_types[i][0] == 'double':
                                try:
                                    val = float(val)
                                    if "e" in str(val) or ("." in str(val) and len(str(val).split(".")[1]) > 10):
                                        column_types[i] = ["decimal", "50,30"]
                                except:
                                    column_types[i] = ['char', max_lengths[i]]
                            if column_types[i][0] == 'char':
                                if len(str(val)) + 100 > column_types[i][1]:
                                    column_types[i][1] = max_lengths[i]
                    except IndexError:
                        pass

        for i in range(len(columns)):
            column = columns[i]
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
        thispk = False
        if key[0:3] == "pk-":
            key = key[3:]
            thispk = True
        elif key[0:3] == "ct-":
            key = key[3:]

        # format the dataset type to match engine specific type
        thistype = ""
        if key in list(self.datatypes.keys()):
            thistype = self.datatypes[key]
            if isinstance(thistype, tuple):
                if datatype[0] == 'pk-auto':
                    pass
                elif len(datatype) > 1:
                    thistype = thistype[1] + "(" + str(datatype[1]) + ")"
                else:
                    thistype = thistype[0]
            else:
                if len(datatype) > 1:
                    thistype += "(" + str(datatype[1]) + ")"

        # set the PRIMARY KEY
        if thispk:
            if isinstance(thistype, tuple):
                thistype = self.pkformat % thistype
            else:
                thistype = self.pkformat % (thistype, "")
        return thistype

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
                except:
                    pass
                print("Couldn't create database (%s). Trying to continue anyway." % e)

    def create_db_statement(self):
        """Return SQL statement to create a database."""
        create_stmt = "CREATE DATABASE " + self.database_name()
        return create_stmt

    def create_raw_data_dir(self):
        """Check to see if the archive directory exists and creates it if
        necessary."""
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
        except:
            pass

        create_stmt = self.create_table_statement()
        if self.debug:
            print(create_stmt)
        try:
            self.execute(create_stmt)
        except Exception as e:
            try:
                self.connection.rollback()
            except:
                pass
            print("Couldn't create table (%s). Trying to continue anyway." % e)

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
                urlretrieve(url, path, reporthook=reporthook(progbar))
            except ImportError:
                # For some urls lacking filenames urlretrieve from the future
                # package seems to fail. This issue occurred in the PlantTaxonomy
                # script. If this happens, fall back to the standard Python 2 version.
                from urllib import urlretrieve as py2urlretrieve
                py2urlretrieve(url, path, reporthook=reporthook(progbar))
            finally:
                # Download is complete, set to prevent repeated downloads
                self.use_cache = True
                progbar.close()

    def download_files_from_archive(self, url, filenames, filetype="zip",
                                    keep_in_dir=False, archivename=None):
        """Download files from an archive into the raw data directory."""
        print()
        downloaded = False
        if archivename:
            archivename = self.format_filename(archivename)
        else:
            archivename = self.format_filename(filename_from_url(url))

        archivebase = ''
        if keep_in_dir:
            archivebase = os.path.splitext(os.path.basename(archivename))[0]
            archivedir = os.path.join(DATA_WRITE_PATH, archivebase)
            archivedir = archivedir.format(dataset=self.script.name)
            if not os.path.exists(archivedir):
                os.makedirs(archivedir)

        for filename in filenames:
            if not self.find_file(os.path.join(archivebase, filename)):
                # if no local copy, download the data
                self.create_raw_data_dir()
                if not downloaded:
                    self.download_file(url, archivename)
                    downloaded = True

                if filetype == 'zip':
                    try:
                        archive = zipfile.ZipFile(archivename)
                        if archive.testzip():
                            # This fixes an issue with the zip files that was causing errors on
                            # Python 3. testzip() returns the names of any files with issues so if
                            # it exists there is a problem. For details of the issue and the fix see:
                            # see """https://stackoverflow.com/questions/41492984/
                            # zipfile-testzip-returning-different-results-on-python-2-and-python-3"""
                            archive.getinfo(filename).file_size += (2 ** 64) - 1
                        open_archive_file = archive.open(filename, 'r')
                    except zipfile.BadZipFile as e:
                        print("\n{0} can't be extracted, may be corrupt \n{1}".format(filename, e))

                elif filetype == 'gz':
                    # gzip archives can only contain a single file
                    open_archive_file = gzip.open(archivename, 'r')
                elif filetype == 'tar':
                    archive = tarfile.open(filename, 'r')
                    open_archive_file = archive.extractfile(filename)

                fileloc = self.format_filename(os.path.join(archivebase, filename))
                fileloc = os.path.normpath(fileloc)
                if not os.path.exists(os.path.dirname(fileloc)):
                    os.makedirs(os.path.dirname(fileloc))

                unzipped_file = open(fileloc, 'wb')
                for line in open_archive_file:
                    unzipped_file.write(line)
                open_archive_file.close()
                unzipped_file.close()
                if 'archive' in locals():
                    archive.close()

    def drop_statement(self, objecttype, objectname):
        """Return drop table or database SQL statement."""
        dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
        return dropstatement

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

    def exists(self, script):
        """Check to see if the given table exists."""
        return all([self.table_exists(script.name, key)
                    for key in list(script.urls.keys()) if key])

    def final_cleanup(self):
        """Close the database connection."""
        if self.warnings:
            print('\n'.join(str(w) for w in self.warnings))

        self.disconnect()

    def find_file(self, filename):
        """Check for an existing datafile."""
        for search_path in DATA_SEARCH_PATHS:
            search_path = search_path.format(dataset=self.script.name)
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
        strvalue = str(value).strip()

        # Remove any quotes already surrounding the string
        quotes = ["'", '"']
        if len(strvalue) > 1 and strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
            strvalue = strvalue[1:-1]
        missing_values = ("null", "none")
        if strvalue.lower() in missing_values:
            return None
        elif datatype in ("int", "bigint", "bool"):
            if strvalue:
                intvalue = strvalue.split('.')[0]
                if intvalue:
                    return int(intvalue)
                else:
                    return None
            else:
                return None
        elif datatype in ("double", "decimal"):
            if strvalue.strip():
                try:
                    decimals = float(str(strvalue))
                    return decimals
                except:
                    return None
            else:
                return None
        elif datatype == "char":
            if strvalue.lower() in missing_values:
                return None
            else:
                return strvalue
        else:
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

    def insert_statement(self, values):
        """Return SQL statement to insert a set of values."""
        columns = self.table.get_insert_columns()
        types = self.table.get_column_datatypes()
        columncount = len(self.table.get_insert_columns(join=False, create=False))
        for row in values:
            row_length = len(row)
            # Add None with appropriate value type for empty cells
            for i in range(columncount - row_length):
                row.append(self.format_insert_value(None, types[row_length + i]))

        insert_stmt = "INSERT INTO " + self.table_name()
        insert_stmt += " (" + columns + ")"
        insert_stmt += " VALUES ("
        for i in range(0, columncount):
            insert_stmt += "{}, ".format(self.placeholder)
        insert_stmt = insert_stmt.rstrip(", ") + ")"

        if self.debug:
            print(insert_stmt)
        return insert_stmt

    def set_engine_encoding(self):
        pass

    def set_table_delimiter(self, file_path):
        dataset_file = open_fr(file_path)
        self.auto_get_delimiter(dataset_file.readline())
        dataset_file.close()

    def table_exists(self, dbname, tablename):
        """This can be overridden to return True if a table exists. It
        returns False by default."""
        return False

    def table_name(self, name=None, dbname=None):
        """Return full tablename."""
        if not name:
            name = self.table.name
        if not dbname:
            dbname = self.database_name()
            if not dbname:
                dbname = ''
        return self.opts["table_name"].format(db=dbname, table=name)

    def to_csv(self, sort=True):
        # Due to Cyclic imports we can not move this import to the top
        from retriever.lib.engine_tools import sort_csv
        for table_n in list(self.script.tables.keys()):
            table_name = self.table_name(name=table_n)
            csv_file_output = os.path.normpath(table_name + '.csv')
            csv_file = open_fw(csv_file_output)
            csv_writer = open_csvw(csv_file)
            self.get_cursor()
            self.set_engine_encoding()
            self.cursor.execute("SELECT * FROM  {};".format(table_name))
            row = self.cursor.fetchone()
            colnames = [u'{}'.format(tuple_i[0]) for tuple_i in self.cursor.description]
            csv_writer.writerow(colnames)
            while row is not None:
                csv_writer.writerow(row)
                row = self.cursor.fetchone()
            csv_file.close()
            if sort:
                sort_csv(csv_file_output)
        self.disconnect()

    def warning(self, warning):
        new_warning = Warning('%s:%s' % (self.script.name, self.table.name), warning)
        self.warnings.append(new_warning)

    def load_data(self, filename):
        """Generator returning lists of values from lines in a data file.

        1. Works on both delimited (csv module)
        and fixed width data (extract_fixed_width)
        2. Identifies the delimiter if not known
        3. Removes extra line endings

        """
        if not self.table.delimiter:
            self.set_table_delimiter(filename)

        dataset_file = open_fr(filename)

        if self.table.fixed_width:
            for row in dataset_file:
                yield self.extract_fixed_width(row)
        else:
            reg = re.compile("\\r\\n|\n|\r")
            for row in csv.reader(dataset_file, delimiter=self.table.delimiter):
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
    for i in range(rows):
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


def reporthook(tqdm_inst):
    """tqdm wrapper to generate progress bar for urlretriever"""
    last_block = [0]

    def update_to(count=1, block_size=1, total_size=None):
        if total_size is not None:
            tqdm_inst.total = total_size
        tqdm_inst.update((count - last_block[0]) * block_size)
        last_block[0] = count

    return update_to
