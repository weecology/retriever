import sys
import os
import getpass
import zipfile
import gzip
import tarfile
import urllib
import csv
import itertools
from decimal import Decimal
from retriever import DATA_SEARCH_PATHS, DATA_WRITE_PATH
from retriever.lib.cleanup import no_cleanup
from retriever.lib.warning import Warning


proxy = ["http_proxy","https_proxy","ftp_proxy","HTTP_PROXY","HTTPS_PROXY","FTP_PROXY"]

flag = 0

for i in range(len(proxy)):
    if flag == 0:
        if os.getenv(proxy[i], 0) != 0:
            if len(os.environ[proxy[i]]) != 0:
                flag = 1
                for j in range(len(proxy)):
                    os.environ[proxy[j]] = os.environ[proxy[i]]

class Engine():
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
    pkformat = "%s PRIMARY KEY"
    script = None
    debug = False
    warnings = []
    
    def connect(self, force_reconnect=False):
        if force_reconnect: self.disconnect()
        
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
        '''This method should be overloaded by specific implementations
        of Engine.'''
        pass
    
    def add_to_table(self, data_source):
        """This function adds data to a table from one or more lines specified 
        in engine.table.source."""
        if self.table.columns[-1][1][0][:3] == "ct-":        
            # cross-tab data
            
            lines = gen_from_source(data_source)
            real_lines = []
            for line in lines:
                split_line = line.strip('\n\r\t ').split(self.table.delimiter)
                initial_cols = len(self.table.columns) - (3 if hasattr(self.table, "ct_names") else 2)
                begin = split_line[:initial_cols]
                rest = split_line[initial_cols:]
                n = 0
                for item in rest:
                    if hasattr(self.table, "ct_names"):
                        name = [self.table.ct_names[n]]
                        n += 1
                    else:
                        name = []
                    real_lines.append(self.table.delimiter.join(begin + name + [item]))
            real_line_length = len(real_lines)
        else:
            # this function returns a generator that iterates over the lines in
            # the source data
            def source_gen():
                return (line for line in gen_from_source(data_source)
                         if line.strip('\n\r\t '))
            # use one generator to compute the length of the input
            real_lines, len_source = source_gen(), source_gen()
            real_line_length = sum(1 for _ in len_source)
            
        total = self.table.record_id + real_line_length
        for line in real_lines:
            if not self.table.fixed_width: line = line.strip()
            if line:
                self.table.record_id += 1            
                linevalues = self.table.values_from_line(line)
                
                types = self.table.get_column_datatypes()
                # Build insert statement with the correct # of values
                try: 
                    cleanvalues = [self.format_insert_value(self.table.cleanup.function
                                                            (linevalues[n], 
                                                            self.table.cleanup.args),
                                                            types[n]) 
                                   for n in range(len(linevalues))]
                except Exception as e:
                    self.warning('Exception in line %s: %s' % (self.table.record_id, e))
                    continue
                try:
                    insert_stmt = self.insert_statement(cleanvalues)
                except:
                    if self.debug: print types
                    if self.debug: print linevalues
                    if self.debug: print cleanvalues
                    raise
                
                try:
                    update_frequency = int(self.update_frequency)
                except:
                    update_frequency = 100
                    
                if (self.table.record_id % update_frequency == 0 
                    or self.table.record_id == 1 
                    or self.table.record_id == total):
                    prompt = "Inserting rows to " + self.table_name() + ": "
                    prompt += str(self.table.record_id) + " / " + str(total)
                    sys.stdout.write(prompt + "\b" * len(prompt))
                
                try:
                    self.execute(insert_stmt, commit=False)
                except:
                    print insert_stmt
                    raise
        
        print
        self.connection.commit()
    
    def auto_create_table(self, table, url=None, filename=None, pk=None):
        """Creates a table automatically by analyzing a data source and 
        predicting column names, data types, delimiter, etc."""
        if url and not filename:
            filename = filename_from_url(url)
        self.table = table
        
        if url and not self.find_file(filename):
            # If the file doesn't exist, download it
            self.download_file(url, filename)
        file_path = self.find_file(filename)
        
        source = (skip_rows,
                  (self.table.column_names_row - 1, 
                   (open, (file_path, "rb"))))
        lines = gen_from_source(source)
        
        header = lines.next()
        lines.close()
        
        source = (skip_rows,
                  (self.table.header_rows, 
                   (open, (file_path, "rb"))))
                   
        if not self.table.delimiter:
            self.auto_get_delimiter(header)
        
        if not self.table.columns:            
            lines = gen_from_source(source)
            
            if pk is None:
                self.table.columns = [("record_id", ("pk-auto",))]
            else:
                self.table.columns = []
                self.table.contains_pk = True
                
            columns, column_values = self.table.auto_get_columns(header)
            
            self.auto_get_datatypes(pk, lines, columns, column_values)
        
        if self.table.columns[-1][1][0][:3] == "ct-" and hasattr(self.table, "ct_names") and not self.table.ct_column in [c[0] for c in self.table.columns]:
            self.table.columns = self.table.columns[:-1] + [(self.table.ct_column, ("char", 20))] + [self.table.columns[-1]]
        
        self.create_table()

    def auto_get_datatypes(self, pk, source, columns, column_values):
        """Determines data types for each column."""
        # Get all values for each column
        if hasattr(self, 'scan_lines'):
            lines = int(self.scan_lines)
            lines_to_scan = []
            n = 0
            while n < lines:
                lines_to_scan.append(source.next())
                n += 1
        else:
            lines_to_scan = source
            
        column_types = [('int',) for i in range(len(columns))]
        max_lengths = [0 for i in range(len(columns))]
            
        # Check the values for each column to determine data type
        for line in lines_to_scan:
            if line.replace("\t", "").strip():
                values = self.table.extract_values(line.strip("\n"))
                for i in range(len(columns)):
                    try:
                        value = values[i]
                        
                        if self.table.cleanup.function != no_cleanup:
                            value = self.table.cleanup.function(value, self.table.cleanup.args)
                            
                        if value != None and value != '':
                            if len(str(value)) > max_lengths[i]:
                                max_lengths[i] = len(str(value))
                            
                            if column_types[i][0] in ('int', 'bigint'):
                                try:
                                    value = int(value)
                                    if column_types[i][0] == 'int' and hasattr(self, 'max_int') and value > self.max_int:
                                        column_types[i] = ['bigint',]
                                except:
                                    column_types[i] = ['double',]
                            if column_types[i][0] == 'double':
                                try:
                                    value = float(value)
                                    if "e" in str(value) or ("." in str(value) and
                                                             len(str(value).split(".")[1]) > 10):
                                        column_types[i] = ["decimal","30,20"]
                                except:
                                    column_types[i] = ['char',max_lengths[i]]
                            if column_types[i][0] == 'char':
                                if len(str(value)) > column_types[i][1]:
                                    column_types[i][1] = max_lengths[i]
                
                    except IndexError:
                        pass
                    
        
        for i in range(len(columns)):
            column = columns[i]
            column[1] = column_types[i]
            if pk == column[0]:
                column[1][0] = "pk-" + column[1][0]
            
        for column in columns:
            self.table.columns.append((column[0], tuple(column[1])))

    def auto_get_delimiter(self, header):
        # Determine the delimiter by finding out which of a set of common
        # delimiters occurs most in the header line
        self.table.delimiter = "\t"
        for other_delimiter in [",", ";"]:
            if header.count(other_delimiter) > header.count(self.table.delimiter):
                self.table.delimiter = other_delimiter

    def convert_data_type(self, datatype):
        """Converts Retriever generic data types to database platform specific 
        data types"""
        thistype = datatype[0]
        thispk = False
        if thistype[0:3] == "pk-":
            thistype = thistype.lstrip("pk-")
            thispk = True
        elif thistype[0:3] == "ct-":
            thistype = thistype[3:]
            
        if thistype in self.datatypes.keys():
            thistype = self.datatypes[thistype]
            
            if isinstance(thistype, tuple):
                if len(datatype) > 1 and datatype[1] > 0:
                    thistype = thistype[1] + "(" + str(datatype[1]) + ")"
                else:
                    thistype = thistype[0]
            else:
                if len(datatype) > 1 and datatype[1] > 0:
                    thistype += "(" + str(datatype[1]) + ")"
        else:
            thistype = ""
            
        if thispk:
            thistype = self.pkformat % thistype
            
        return thistype
        
    def create_db(self):
        """Creates a new database based on settings supplied in Database object
        engine.db"""
        db_name = self.database_name()
        if db_name:
            print "Creating database " + db_name + "..."
            # Create the database    
            create_stmt = self.create_db_statement()
            if self.debug: print create_stmt
            try:
                self.execute(create_stmt)
            except Exception as e:
                try: self.connection.rollback()
                except: pass
                print "Couldn't create database (%s). Trying to continue anyway." % e

    def create_db_statement(self):
        """Returns a SQL statement to create a database."""
        create_stmt = "CREATE DATABASE " + self.database_name()
        return create_stmt
        
    def create_raw_data_dir(self):
        """Checks to see if the archive directory exists and creates it if 
        necessary."""
        path = self.format_data_dir()
        if not os.path.exists(path):
            os.makedirs(path)
            
    def create_table(self):
        """Creates a new database table based on settings supplied in Table 
        object engine.table."""
        print "Creating table " + self.table_name() + "..."

        # Try to drop the table if it exists; this may cause an exception if it
        # doesn't exist, so ignore exceptions
        try:
            self.execute(self.drop_statement("TABLE", self.table_name()))
        except:
            pass
        
        create_stmt = self.create_table_statement()
        if self.debug: print create_stmt
        try:
            self.execute(create_stmt) 
        except Exception as e:
            try: self.connection.rollback()
            except: pass
            print "Couldn't create table (%s). Trying to continue anyway." % e
        
    def create_table_statement(self):
        """Returns a SQL statement to create a table."""
        create_stmt = "CREATE TABLE " + self.table_name() + " ("
        
        columns = self.table.get_insert_columns(join=False)
        
        types = []
        for column in self.table.columns:
            for column_name in columns:
                if column[0] == column_name:
                    types.append(self.convert_data_type(column[1]))                    
        
        if self.debug: print columns

        column_strings = []
        for c, t in zip(columns, types):
            column_strings.append(c + ' ' + t)
        
        create_stmt += ', '.join(column_strings)
        create_stmt += " );"

        return create_stmt
        
    def database_name(self, name=None):
        if not name:
            try:
                name = self.script.shortname
            except AttributeError:
                name = "{db}"
        
        try:
            db_name = self.opts["database_name"].replace('{db}', name)
        except KeyError:
            db_name = name
        
        return db_name
                
    def download_file(self, url, filename, clean_line_endings=True):
        """Downloads a file to the raw data directory."""
        if not self.find_file(filename):
            path = self.format_filename(filename)
            self.create_raw_data_dir()
            print "Downloading " + filename + "..."
            file = urllib.urlopen(url) 
            local_file = open(path, 'wb')
            if clean_line_endings and (filename.split('.')[-1].lower() not in ["exe", "zip"]):
                local_file.write(file.read().replace("\r\n", "\n").replace("\r", "\n"))
            else:
                local_file.write(file.read())
            local_file.close()
            file.close()

    def download_files_from_archive(self, url, filenames, filetype="zip"):
        """Downloads one or more files from an archive into the raw data
        directory."""
        downloaded = False
        archivename = self.format_filename(filename_from_url(url))
        
        for filename in filenames:
            if self.find_file(filename):
                # Use local copy
                pass
            else:
                self.create_raw_data_dir()
                
                if not downloaded:
                    self.download_file(url, filename_from_url(url))
                    downloaded = True     

                if filetype == 'zip':
                    archive = zipfile.ZipFile(archivename)
                    open_archive_file = archive.open(filename)
                elif filetype == 'gz':
                    #gzip archives can only contain a single file 
                    open_archive_file = gzip.open(archivename)
                elif filetype == 'tar':
                    archive = tarfile.open(filename)
                    open_archive_file = archive.extractfile(filename)

                fileloc = self.format_filename(os.path.basename(filename))
                unzipped_file = open(fileloc, 'wb')
                for line in open_archive_file:
                    unzipped_file.write(line)
                open_archive_file.close()
                unzipped_file.close()
                if 'archive' in locals(): archive.close()

    def drop_statement(self, objecttype, objectname):
        """Returns a drop table or database SQL statement."""
        dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
        return dropstatement

    def escape_single_quotes(self, value):
        return value.replace("'", "\\'")
        
    def escape_double_quotes(self, value):
        return value.replace('"', '\\"')
        
    def execute(self, statement, commit=True):
        self.cursor.execute(statement)
        if commit:
            self.connection.commit()
            
    def exists(self, script):            
        return all([self.table_exists(
                    script.shortname,
                    key
                    )
                    for key in script.urls.keys() if key])

    def final_cleanup(self):
        """Close the database connection."""
        
        if self.warnings:
            print '\n'.join(str(w) for w in self.warnings)
            
        self.disconnect()

    def find_file(self, filename):
        for search_path in DATA_SEARCH_PATHS:
            search_path = search_path.replace("{dataset}", self.script.shortname)
            file_path = os.path.join(search_path, filename)
            if file_exists(file_path):
                return file_path
        return False

    def format_data_dir(self):
        """Returns the correctly formatted raw data directory location."""
        return DATA_WRITE_PATH.replace("{dataset}", self.script.shortname)

    def format_filename(self, filename):
        """Returns the full path of a file in the archive directory."""
        return os.path.join(self.format_data_dir(), filename)

    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement, for example by surrounding
        it in single quotes."""
        datatype = datatype.split('-')[-1]
        strvalue = str(value).strip()
        
        # Remove any quotes already surrounding the string
        quotes = ["'", '"']
        if len(strvalue) > 1 and strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
            strvalue = strvalue[1:-1]        
        nulls = ("null", "none")
        
        if strvalue.lower() in nulls:
            return "null"
        elif datatype in ("int", "bigint", "bool"):
            if strvalue:
                intvalue = strvalue.split('.')[0]
                if intvalue:
                    return int(intvalue)
                else:
                    return "null"
            else:
                return "null"
        elif datatype in ("double", "decimal"):
            if strvalue:
                return strvalue
            else:
                return "null"
        elif datatype=="char":
            if strvalue.lower() in nulls:
                return "null"
                
            # automatically escape quotes in string fields
            if hasattr(self.table, "escape_double_quotes") and self.table.escape_double_quotes:
                strvalue = self.escape_double_quotes(strvalue)
            if hasattr(self.table, "escape_single_quotes") and self.table.escape_single_quotes:
                strvalue = self.escape_single_quotes(strvalue)
                
            return "'" + strvalue + "'"
        #elif datatype=="bool":
            #return "'true'" if value else "'false'"
        else:
            return "null"

    def get_cursor(self):
        """Gets the db cursor."""
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor
        
    cursor = property(get_cursor)
        
    def get_input(self):
        """Manually get user input for connection information when script is 
        run from terminal."""
        for opt in self.required_opts:
            if not (opt[0] in self.opts.keys()):
                if opt[0] == "password":
                    print opt[1]
                    self.opts[opt[0]] = getpass.getpass(" ")                
                else:
                    prompt = opt[1]
                    if opt[2]:
                        prompt += " or press Enter for the default, %s" % opt[2]
                    prompt += ': '
                    self.opts[opt[0]] = raw_input(prompt)
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
                       (open, (filename, 'r'))))
        self.add_to_table(data_source)

    def insert_data_from_url(self, url):
        """Insert data from a web resource, such as a text file."""
        filename = filename_from_url(url)
        find = self.find_file(filename)
        if find:
            # Use local copy
            self.insert_data_from_file(find)
        else:
            # Save a copy of the file locally, then load from that file
            self.create_raw_data_dir()                        
            print "Saving a copy of " + filename + "..."
            self.download_file(url, filename)
            self.insert_data_from_file(self.find_file(filename))

    def insert_statement(self, values):
        """Returns a SQL statement to insert a set of values."""
        columns = self.table.get_insert_columns()
        types = self.table.get_column_datatypes()
        columncount = len(self.table.get_insert_columns(False))
        insert_stmt = "INSERT INTO " + self.table_name()
        insert_stmt += " (" + columns + ")"
        insert_stmt += " VALUES ("
        for i in range(0, columncount):
            insert_stmt += "%s, "
        insert_stmt = insert_stmt.rstrip(", ") + ");"
        n = 0
        while len(values) < insert_stmt.count("%s"):
            values.append(self.format_insert_value(None,
                                                   types[n]))
            n += 1
        insert_stmt %= tuple([str(value) for value in values])
        if self.debug: print insert_stmt
        return insert_stmt

    def table_exists(self, dbname, tablename):
        """This can be overridden to return True if a table exists. It
        returns False by default."""
        return False

    def table_name(self, name=None, dbname=None):
        """Returns the full tablename."""
        if not name:
            name = self.table.name
        if not dbname:
            dbname = self.database_name()
            if not dbname: dbname = ''
        return (self.opts["table_name"]
                .replace('{db}', dbname)
                .replace('{table}', name))
        
    def warning(self, warning):
        new_warning = Warning('%s:%s' % (self.script.shortname, self.table.name), warning)
        self.warnings.append(new_warning)
        
        
def skip_rows(rows, source):
    """Skip over the header lines by reading them before processing."""
    lines = gen_from_source(source)
    for i in range(rows):
        lines.next()
    return lines
    

def file_exists(path):
    """Returns true if a file exists and its size is greater than 0."""
    return (os.path.isfile(path) and os.path.getsize(path) > 0)    
        
        
def filename_from_url(url):
    return url.split('/')[-1].split('?')[0]
    
    
def gen_from_source(source):
    """Returns a generator from a source tuple.        
    Source tuples are of the form (callable, args) where callable(*args) 
    returns either a generator or another source tuple. 
    This allows indefinite regeneration of data sources."""
    while isinstance(source, tuple):
        gen, args = source
        source = gen(*args)
    return source
