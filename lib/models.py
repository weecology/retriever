"""Database Toolkit Data Model

This module contains basic class definitions for the Database Toolkit platform.

"""

import sys
import os
import getpass
import getopt
import zipfile
import urllib
from decimal import Decimal
from hashlib import md5

    
def no_cleanup(value, args):
    """Default cleanup function, returns the unchanged value."""
    return value

def correct_invalid_value(value, args):
    """This cleanup function replaces null indicators with None."""
    try:
        if float(value) in [float(item) for item in args["nulls"]]:            
            return None
        else:
            return value
    except ValueError:
        return value
    
class Cleanup:
    """This class represents a custom cleanup function and a dictionary of 
    arguments to be passed to that function."""
    def __init__(self, function=no_cleanup, args=None):
        self.function = function
        self.args = args    


class Database:
    """Information about a database."""
    dbname = ""
    opts = dict()
    
class Table:
    """Information about a database table."""
    tablename = ""
    pk = True
    hasindex = False
    record_id = 0
    delimiter = "\t"
    columns = []
    header_rows = 1
    fixedwidth = False
    def __init__(self):        
        self.cleanup = Cleanup(no_cleanup, None)        
    
class Engine():
    """A generic database system. Specific database platforms will inherit 
    from this class."""
    name = ""
    db = None
    table = None
    connection = None
    cursor = None
    keep_raw_data = True
    use_local = True
    datatypes = []
    required_opts = []
    pkformat = "%s PRIMARY KEY"
    script = None
    RAW_DATA_LOCATION = os.path.join("raw_data", "{dataset}")    
    def add_to_table(self):
        """This function adds data to a table from one or more lines specified 
        in engine.table.source."""   
        for line in self.table.source:
            line = line.strip()
            if line:
                self.table.record_id += 1            
                linevalues = []
                if (self.table.pk and self.table.hasindex == False):
                    column = 0
                else:
                    column = -1
                 
                for value in self.extract_values(line):
                    column += 1
                    thiscolumn = self.table.columns[column][1][0]
                    # If data type is "skip" ignore the value
                    if thiscolumn == "skip":
                        pass
                    elif thiscolumn == "combine":
                        # If "combine" append value to end of previous column
                        linevalues[len(linevalues) - 1] += " " + value 
                    else:
                        # Otherwise, add new value
                        linevalues.append(value) 
                            
                # Build insert statement with the correct # of values                
                cleanvalues = [self.format_insert_value(self.table.cleanup.function
                                                        (value, 
                                                         self.table.cleanup.args)) 
                               for value in linevalues]
                insertstatement = self.insert_statement(cleanvalues)
                prompt = "Inserting rows to " + self.tablename() + ": "
                sys.stdout.write(prompt + str(self.table.record_id) + "\b" *
                                 (len(str(self.table.record_id)) + 
                                  len(prompt)))
                self.cursor.execute(insertstatement)
                
        print "\n Done!"
        self.connection.commit()
    def auto_create_table(self, url, tablename,
                          cleanup=Cleanup(correct_invalid_value, 
                                          {"nulls":(-999,)} 
                                          ),
                          pk=None):
        """Creates a table automatically by analyzing a data source and 
        predicting column names, data types, delimiter, etc."""
        filename = url.split('/')[-1]
        self.create_raw_data_dir()
        need_to_delete = False
        self.table = Table()
        self.table.tablename = tablename
        self.table.cleanup = cleanup
        
        if not (self.use_local and 
                os.path.isfile(self.format_filename(filename))):
            # If the file doesn't exist, download it
            self.create_raw_data_dir()                        
            print "Saving a copy of " + filename + " . . ."
            self.download_file(url, filename)
            if not self.keep_raw_data:
                need_to_delete = True
                
        source = open(self.format_filename(filename), "rb")
        header = source.readline()
        
        # Determine the delimiter by finding out which of a set of common
        # delimiters occurs most in the header line
        self.table.delimiter = "\t"
        for other_delimiter in [",", ";"]:
            if header.count(other_delimiter) > header.count(self.table.delimiter):
                self.table.delimiter = other_delimiter
        
        # Get column names from header row
        column_names = header.split(self.table.delimiter)
        if pk is None:
            self.table.columns = [("record_id", ("pk-auto",))]
        else:
            self.table.columns = []
            self.table.hasindex = True
        columns = []
        column_values = dict()
        
        for column_name in column_names:
            this_column = column_name
            for c in [")", "\n", "\r"]:
                this_column = this_column.strip(c)
            for c in ["."]:
                this_column = this_column.replace(c, "")
            for c in [" ", "(", "/", ".", "-"]:
                this_column = this_column.replace(c, "_")
            while "__" in this_column:
                this_column = this_column.replace("__", "_")
            this_column = this_column.lstrip("0123456789_").rstrip("_")
                
            if this_column.lower() == "order":
                this_column = "sporder"
            if this_column.lower() == "references":
                this_column = "refs"
            
            if this_column:
                columns.append([this_column, None])
                column_values[this_column] = []
        
        # Get all values for each column
        for line in source:
            if line.replace("\t", "").strip():
                values = line.strip("\n").strip("\r").split(self.table.delimiter)
                for i in range(len(columns)):
                    try:
                        column_values[columns[i][0]].append(values[i])
                    except IndexError:
                        column_values[columns[i][0]].append(None)
        
        # Check the values for each column to determine data type
        # Priority: decimal - float - integer - string
        for column in columns:
            values = column_values[column[0]]
            try:
                float_values = [float(value) for value in values
                                if value]
                try:
                    int_values = [int(value) == float(value) for value in values
                                  if value]
                    if all(int_values):
                        datatype = "int"
                    else:
                        datatype = "float"
                except:
                    datatype = "float"
            except:
                # Column is a string
                datatype = "char"
        
            if datatype is "char":
                max_length = max([len(s) for s in values if s])
                column[1] = ["char", max_length]
            elif datatype is "int":
                column[1] = ["int",]
            elif datatype is "float":
                column[1] = ["double",]
                for value in values:
                    if "e" in str(value) or ("." in str(value) and
                                             len(str(value).split(".")[1]) > 10):
                        column[1] = ["decimal","30,20"]
                                
            if pk == column[0]:
                column[1][0] = "pk-" + column[1][0]
            
        for column in columns:
            self.table.columns.append((column[0], tuple(column[1])))
        
        print self.table.columns
        self.create_table()
    def convert_data_type(self, datatype):
        """Converts DBTK generic data types to database platform specific data
        types"""
        datatypes = dict()
        thistype = datatype[0]
        thispk = False
        if thistype[0:3] == "pk-":
            thistype = thistype.lstrip("pk-")
            thispk = True
        customtypes = ("auto", "int", "double", "decimal", "char", "bool")
        for i in range(0, len(customtypes)):
            datatypes[customtypes[i]] = i
        datatypes["combine"], datatypes["skip"] = [-1, -1]        
        mydatatypes = self.datatypes
        thisvartype = datatypes[thistype]
        if thisvartype > -1:
            type = mydatatypes[thisvartype]
            if len(datatype) > 1:
                type += "(" + str(datatype[1]) + ")"
        else:
            type = ""
        if thispk:
            type = self.pkformat % type
        return type
    def create_db(self):
        """Creates a new database based on settings supplied in Database object
        engine.db"""
        print "Creating database " + self.db.dbname + " . . ."
        # Create the database    
        self.cursor.execute(self.create_db_statement())
    def create_db_statement(self):
        """Returns a SQL statement to create a database."""
        createstatement = "CREATE DATABASE " + self.db.dbname
        return createstatement
    def create_raw_data_dir(self):
        """Checks to see if the archive directory exists and creates it if 
        necessary."""
        path = self.format_data_dir()
        if not os.path.exists(path):
            os.makedirs(path)            
    def create_table(self):
        """Creates a new database table based on settings supplied in Table 
        object engine.table."""
        print "Creating table " + self.table.tablename + ". . ."
        createstatement = self.create_table_statement()
        self.cursor.execute(createstatement)
    def create_table_statement(self):
        """Returns a SQL statement to create a table."""
        self.cursor.execute(self.drop_statement("TABLE", self.tablename()))
        createstatement = "CREATE TABLE " + self.tablename() + " ("
        
        for item in self.table.columns:
            if (item[1][0] != "skip") and (item[1][0] != "combine"):
                createstatement += (item[0] + " "
                                    + self.convert_data_type(item[1]) + ", ")    

        createstatement = createstatement.rstrip(', ')    
        createstatement += " );"
        return createstatement
    def download_file(self, url, filename):
        """Downloads a file to the raw data directory."""
        self.create_raw_data_dir()
        if not self.use_local or not os.path.isfile(self.format_filename(filename)):
            print "Downloading " + filename + " . . ."
            file = urllib.urlopen(url) 
            local_file = open(self.format_filename(filename), 'wb')
            local_file.write(file.read())
            local_file.close()
            file.close()
    def download_files_from_archive(self, url, filenames):
        """Downloads one or more files from an archive into the raw data
        directory."""
        downloaded = False
        archivename = self.format_filename(url.split('/')[-1])
        
        for filename in filenames:
            if self.use_local and os.path.isfile(self.format_filename(filename)):
                # Use local copy
                print "Using local copy of " + filename
            else:
                self.create_raw_data_dir()
                
                if not downloaded:
                    self.download_file(url, url.split('/')[-1])
                    downloaded = True     
                        
                local_zip = zipfile.ZipFile(archivename)
                fileloc = self.format_filename(os.path.basename(filename))
                        
                open_zip = local_zip.open(filename)
                unzipped_file = open(fileloc, 'wb')
                unzipped_file.write(open_zip.read())
                unzipped_file.close()
                open_zip.close()
                
                local_zip.close()                                            
        if not self.keep_raw_data:
            try:
                os.remove(archivename)
            except:
                pass            
    def drop_statement(self, objecttype, objectname):
        """Returns a drop table or database SQL statement."""
        dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
        return dropstatement
    def extract_values(self, line):
        """Given a line of data, this function returns a list of the individual
        data values."""
        if self.table.fixedwidth:
            pos = 0
            values = []
            for width in self.table.fixedwidth:
                values.append(line[pos:pos+width].strip())
                pos += width
            return values
        else:
            return line.split(self.table.delimiter)
    def format_data_dir(self):
        """Returns the correctly formatted raw data directory location."""
        return self.RAW_DATA_LOCATION.replace("{dataset}", self.script.shortname)
    def format_filename(self, filename):
        """Returns the full path of a file in the archive directory."""
        return os.path.join(self.format_data_dir(), filename)
    def format_insert_value(self, value):
        """Formats a value for an insert statement, for example by surrounding
        it in single quotes."""
        if isinstance(value, basestring):
            value = value.decode("utf-8", "ignore")
        strvalue = str(value).strip()
        if strvalue.lower() == "null":
            return "null"
        elif value:
            quotes = ["'", '"']            
            if strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
                strvalue = strvalue.strip(''.join(quotes)) 
        else:
            return "null"
        strvalue = strvalue.replace("'", "''")
        return "'" + strvalue + "'"
    def get_input(self):
        """Manually get user input for connection information when script is 
        run from terminal."""
        for opt in self.required_opts:
            if not (opt[0] in self.opts.keys()):
                if opt[0] == "password":
                    print opt[1]
                    self.opts[opt[0]] = getpass.getpass(" ")                
                else:
                    self.opts[opt[0]] = raw_input(opt[1])
            if self.opts[opt[0]] in ["", "default"]:
                self.opts[opt[0]] = opt[2]    
    def get_insert_columns(self, join=True):
        """Gets a set of column names for insert statements."""
        columns = ""
        for item in self.table.columns:
            thistype = item[1][0]
            if ((thistype != "skip") and (thistype !="combine") and 
                (self.table.hasindex == True or thistype[0:3] != "pk-")):
                columns += item[0] + ", "
        columns = columns.rstrip(', ')
        if join:
            return columns
        else:
            return columns.lstrip("(").rstrip(")").split(", ")
    def insert_data_from_archive(self, url, filenames):
        """Insert data from files located in an online archive. This function
        extracts the file, inserts the data, and deletes the file if raw data 
        archiving is not set."""
        self.download_files_from_archive(url, filenames)
        for filename in filenames:
            fileloc = self.format_filename(filename)
            self.insert_data_from_file(fileloc)
            if not self.keep_raw_data:
                try:
                    os.remove(fileloc)
                except:
                    pass
    def insert_data_from_file(self, filename):
        """The default function to insert data from a file. This function 
        simply inserts the data row by row. Database platforms with support
        for inserting bulk data from files can override this function."""
        self.table.source = self.skip_rows(self.table.header_rows, 
                                           open(filename, "r"))        
        self.add_to_table()
        self.table.source.close()
    def insert_data_from_url(self, url):
        """Insert data from a web resource, such as a text file."""
        filename = url.split('/')[-1]
        self.create_raw_data_dir()
        if self.use_local and os.path.isfile(self.format_filename(filename)):
            # Use local copy
            print "Using local copy of " + filename
            self.insert_data_from_file(self.format_filename(filename))            
        else:
            if self.keep_raw_data:
                # Save a copy of the file locally, then load from that file
                self.create_raw_data_dir()                        
                print "Saving a copy of " + filename + " . . ."
                self.download_file(url, filename)
                self.insert_data_from_file(self.format_filename(filename))
            else:
                # Don't save the file, just load it from the web resource
                self.table.source = self.skip_rows(self.table.header_rows, 
                                                   urllib.urlopen(url))
                self.add_to_table()
                self.table.source.close()
    def insert_statement(self, values):
        """Returns a SQL statement to insert a set of values."""
        columns = self.get_insert_columns()
        columncount = len(self.get_insert_columns(False))
        insertstatement = "INSERT INTO " + self.tablename()
        insertstatement += " (" + columns + ")"  
        insertstatement += " VALUES ("
        for i in range(0, columncount):
            insertstatement += "%s, "
        insertstatement = insertstatement.rstrip(", ") + ");"
        while len(values) < insertstatement.count("%s"):
            values.append(self.format_insert_value(None))
        insertstatement %= tuple(values)
        return insertstatement        
    def skip_rows(self, rows, source):
        """Skip over the header lines by reading them before processing."""
        if rows > 0:
            for i in range(rows):
                line = source.readline()
        return source
    def tablename(self):
        """Returns the full tablename in the format db.table."""        
        return self.db.dbname + "." + self.table.tablename