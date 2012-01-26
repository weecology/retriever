import sys
import os
import getpass
import zipfile
import urllib
import csv
from decimal import Decimal


class Engine():
    """A generic database system. Specific database platforms will inherit 
    from this class."""
    name = ""
    instructions = "Enter your database connection information:"
    db = None
    table = None
    connection = None
    cursor = None
    datatypes = []
    required_opts = []
    pkformat = "%s PRIMARY KEY"
    script = None
    debug = False
    RAW_DATA_LOCATION = os.path.join("raw_data", "{dataset}")

    
    def add_to_table(self):
        """This function adds data to a table from one or more lines specified 
        in engine.table.source."""
        lines = self.table.source
        self.get_cursor()

        if self.table.columns[-1][1][0][:3] == "ct-":
            # cross-tab data
            real_lines = []
            for line in lines:
                split_line = line.strip('\n\r\t').split(self.table.delimiter)
                begin = split_line[:len(self.table.columns) - (3 if hasattr(self.table, "ct_names") else 2)]
                rest = split_line[len(self.table.columns) - 2:]
                n = 0
                for item in rest:
                    if hasattr(self.table, "ct_names"):
                        name = [self.table.ct_names[n]]
                        n += 1
                    else:
                        name = []
                    real_lines.append(self.table.delimiter.join(begin + name + [item]))
        else:        
            real_lines = [line for line in lines 
                          if line.strip('\n\r\t ')]
                          
        total = self.table.record_id + len(real_lines)
        for line in real_lines:
            line = line.strip()
            if line:
                self.table.record_id += 1            
                linevalues = self.values_from_line(line)

                types = self.get_column_datatypes()            
                # Build insert statement with the correct # of values                
                cleanvalues = [self.format_insert_value(self.table.cleanup.function
                                                        (linevalues[n], 
                                                         self.table.cleanup.args),
                                                        types[n]) 
                               for n in range(len(linevalues))]
                insert_stmt = self.insert_statement(cleanvalues)

                if self.table.record_id % 10 == 0 or self.table.record_id == total:
                    prompt = "Inserting rows to " + self.tablename() + ": "
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
        self.create_raw_data_dir()
        self.table = table
        
        if url and not file_exists(self.format_filename(filename)):
            # If the file doesn't exist, download it
            self.download_file(url, filename)

        source = self.skip_rows(self.table.column_names_row - 1, 
                                open(self.format_filename(filename), "rb"))
        header = source.readline()
        source.close()

        if not self.table.delimiter:
            self.auto_get_delimiter(header)
        
        if not self.table.columns:            
            source = self.skip_rows(self.table.header_rows, 
                                    open(self.format_filename(filename), "rb"))
            
            if pk is None:
                self.table.columns = [("record_id", ("pk-auto",))]
            else:
                self.table.columns = []
                self.table.contains_pk = True
                
            columns, column_values = self.auto_get_columns(header)
            
            self.auto_get_datatypes(pk, source, columns, column_values)

        if self.table.columns[-1][1][0][:3] == "ct-" and hasattr(self.table, "ct_names") and not self.table.ct_column in [c[0] for c in self.table.columns]:
            self.table.columns = self.table.columns[:-1] + [(self.table.ct_column, ("char", 20))] + [self.table.columns[-1]]

        
        self.create_table()

                
    def auto_get_columns(self, header):
        """Finds the delimiter and column names from the header row."""        
        if self.table.fixed_width:
            column_names = self.extract_values(header)
        else:
            # Get column names from header row
            values = self.split_on_delimiter(header)
            column_names = [name.strip() for name in values]
        
        columns = []
        column_values = dict()
        
        for column_name in column_names:
            this_column = column_name.lower()
            
            replace = [
                       ("%", "percent"),
                       ("&", "and"),
                       ("\xb0", "degrees"),
                       ("group", "grp"),
                       ("order", "sporder"),
                       ("references", "refs"),
                       ("long", "lon"),
                       ("date", "record_date")
                       ] + self.table.replace_columns
            for combo in replace:
                if this_column == combo[0].lower():
                    this_column = combo[1]
                this_column = this_column.replace(combo[0], combo[1])
            
            
            for c in [")", "\n", "\r"]:
                this_column = this_column.strip(c)
            for c in [".", '"', "'"]:
                this_column = this_column.replace(c, "")
            for c in [" ", "(", "/", ".", "-"]:
                this_column = this_column.replace(c, "_")
            while "__" in this_column:
                this_column = this_column.replace("__", "_")
            this_column = this_column.lstrip("0123456789_").rstrip("_")
            
            
            if this_column:
                columns.append([this_column, None])
                column_values[this_column] = []

        return columns, column_values

        
    def auto_get_datatypes(self, pk, source, columns, column_values):
        """Determines data types for each column."""
        # Get all values for each column
        if hasattr(self, 'scan_lines'):
            lines = int(self.scan_lines)
            lines_to_scan = source.readlines(lines)
        else:
            lines_to_scan = source.readlines()
        for line in lines_to_scan:
            if line.replace("\t", "").strip():
                values = self.extract_values(line.strip("\n"))
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
                    int_values = [int(value) == value for value in float_values]
                    if all(int_values):
                        if max(values) > 32767:
                            datatype = "bigint"
                        else:
                            datatype = "int"
                    else:
                        datatype = "float"
                except:
                    datatype = "float"
            except:
                # Column is a string
                datatype = "char"
        
            if datatype is "char":
                max_length = max([len(s) for s in values if s]) + 5
                column[1] = ["char", max_length]
            elif datatype in ["int", "bigint"]:
                column[1] = [datatype,]
            elif datatype is "float":
                column[1] = ["double",]
                for value in values:
                    if "e" in str(value) or ("." in str(value) and
                                             len(str(value).split(".")[1]) > 10):
                        column[1] = ["decimal","30,20"]
                        break
                        
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
                if len(datatype) > 1:
                    thistype = thistype[1] + "(" + str(datatype[1]) + ")"
                else:
                    thistype = thistype[0]
            else:
                if len(datatype) > 1:
                    thistype += "(" + str(datatype[1]) + ")"
        else:
            thistype = ""
            
        if thispk:
            thistype = self.pkformat % thistype
            
        return thistype

        
    def create_db(self):
        """Creates a new database based on settings supplied in Database object
        engine.db"""
        print "Creating database " + self.db_name + "..."
        # Create the database    
        self.get_cursor()
        create_stmt = self.create_db_statement()
        if self.debug: print create_stmt
        self.execute(create_stmt)

        
    def create_db_statement(self):
        """Returns a SQL statement to create a database."""
        create_stmt = "CREATE DATABASE " + self.db_name
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
        print "Creating table " + self.table.name + "..."
        self.get_cursor()
        
        # Try to drop the table if it exists; this may cause an exception if it
        # doesn't exist, so ignore exceptions
        try:
            self.execute(self.drop_statement("TABLE", self.tablename()))
        except:
            pass
        
        create_stmt = self.create_table_statement()
        if self.debug: print create_stmt
        self.execute(create_stmt)        

        
    def create_table_statement(self):
        """Returns a SQL statement to create a table."""
        create_stmt = "CREATE TABLE " + self.tablename() + " ("
        
        columns = self.get_insert_columns(join=False)
        
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

        
    def download_file(self, url, filename):
        """Downloads a file to the raw data directory."""
        self.create_raw_data_dir()
        path = self.format_filename(filename)
        if (not file_exists(path)):
            print "Downloading " + filename + "..."
            file = urllib.urlopen(url) 
            local_file = open(path, 'wb')
            if not filename.split('.')[-1].lower() in ["exe", "zip"]:
                local_file.write(file.read().replace("\r\n", "\n").replace("\r", "\n"))
            else:
                local_file.write(file.read())
            local_file.close()
            file.close()

            
    def download_files_from_archive(self, url, filenames):
        """Downloads one or more files from an archive into the raw data
        directory."""
        downloaded = False
        archivename = self.format_filename(filename_from_url(url))
        
        for filename in filenames:
            if file_exists(self.format_filename(filename)):
                # Use local copy
                pass
            else:
                self.create_raw_data_dir()
                
                if not downloaded:
                    self.download_file(url, filename_from_url(url))
                    downloaded = True     
                        
                local_zip = zipfile.ZipFile(archivename)
                fileloc = self.format_filename(os.path.basename(filename))
                        
                open_zip = local_zip.open(filename)
                unzipped_file = open(fileloc, 'wb')
                unzipped_file.write(open_zip.read())
                unzipped_file.close()
                open_zip.close()
                
                local_zip.close()                                            

                
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

        
    def extract_values(self, line):
        """Given a line of data, this function returns a list of the individual
        data values."""
        if self.table.fixed_width:
            pos = 0
            values = []
            for width in self.table.fixed_width:
                values.append(line[pos:pos+width].strip())
                pos += width
            return values
        else:
            return self.split_on_delimiter(line)

            
    def final_cleanup(self):
        """Close the database connection."""
        self.connection.close()

        
    def format_column_name(self, column):
        return column

        
    def format_data_dir(self):
        """Returns the correctly formatted raw data directory location."""
        return self.RAW_DATA_LOCATION.replace("{dataset}", self.script.shortname)

        
    def format_filename(self, filename):
        """Returns the full path of a file in the archive directory."""
        return os.path.join(self.format_data_dir(), filename)

        
    def format_insert_value(self, value, datatype):
        """Formats a value for an insert statement, for example by surrounding
        it in single quotes."""
        strvalue = str(value).strip()
        quotes = ["'", '"']
        if len(strvalue) > 0 and strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
            strvalue = strvalue[1:-1]        
        nulls = ("null", "none")
        # Remove any quotes already surrounding the string
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
                return 0
        elif datatype in ("double", "decimal"):
            if strvalue:
                return strvalue
            else:
                return 0
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


    def get_column_datatypes(self):
        """Gets a set of column names for insert statements."""
        columns = []
        for item in self.get_insert_columns(False):
            for column in self.table.columns:
                if item == column[0]:
                    columns.append(column[1][0])
        return columns
        
        
    def get_cursor(self):
        """Gets the db cursor."""
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor()

        
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
                (self.table.contains_pk == True or thistype[0:3] != "pk-")):
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

                    
    def insert_data_from_file(self, filename):
        """The default function to insert data from a file. This function 
        simply inserts the data row by row. Database platforms with support
        for inserting bulk data from files can override this function."""
        source = self.skip_rows(self.table.header_rows, 
                                open(filename, "r"))
        self.table.source = source.readlines()
        self.add_to_table()
        source.close()

        
    def insert_data_from_url(self, url):
        """Insert data from a web resource, such as a text file."""
        filename = filename_from_url(url)
        self.create_raw_data_dir()
        if file_exists(self.format_filename(filename)):
            # Use local copy            
            self.insert_data_from_file(self.format_filename(filename))            
        else:
            # Save a copy of the file locally, then load from that file
            self.create_raw_data_dir()                        
            print "Saving a copy of " + filename + "..."
            self.download_file(url, filename)
            self.insert_data_from_file(self.format_filename(filename))

                
    def insert_statement(self, values):
        """Returns a SQL statement to insert a set of values."""
        columns = self.get_insert_columns()
        types = self.get_column_datatypes()
        columncount = len(self.get_insert_columns(False))
        insert_stmt = "INSERT INTO " + self.tablename()
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

        
    def skip_rows(self, rows, source):
        """Skip over the header lines by reading them before processing."""
        if rows > 0:
            for i in range(rows):
                line = source.readline()
        return source


    def split_on_delimiter(self, line):
        dialect = csv.excel
        dialect.escapechar = "\\"
        r = csv.reader([line], dialect=dialect, delimiter=self.table.delimiter)
        return r.next()

        
    def table_exists(self, dbname, tablename):
        """This can be overridden to return True if a table exists. It
        returns False by default."""
        return False

        
    def tablename(self):
        """Returns the full tablename in the format db.table."""        
        return self.db_name + "." + self.table.name

        
    def values_from_line(self, line):
        linevalues = []
        if (self.table.pk and self.table.contains_pk == False):
            column = 0
        else:
            column = -1
        
        for value in self.extract_values(line):
            column += 1
            try:
                this_column = self.table.columns[column][1][0]

                # If data type is "skip" ignore the value
                if this_column == "skip":
                    pass
                elif this_column == "combine":
                    # If "combine" append value to end of previous column
                    linevalues[-1] += " " + value 
                else:
                    # Otherwise, add new value
                    linevalues.append(value)
            except:
                # too many values for columns; ignore
                pass

        return linevalues
        
    
    
def file_exists(path):
    """Returns true if a file exists and its size is greater than 0."""
    return (os.path.isfile(path) and os.path.getsize(path) > 0)    
        
        
def filename_from_url(url):
    return url.split('/')[-1].split('?')[0]
