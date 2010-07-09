"""Database Toolkit tools
Functions to create a database from a delimited text file.

Supported database engines: MySQL, PostgreSQL, SQLite

Usage: python dbtk_ernest2003.py [-e engine (mysql, postgresql, etc.)] [--engine=engine]
                                 [-u username] [--user=username] 
                                 [-p password] [--password=password]
                                 [-h {hostname} (default=localhost)] [--host=hostname] 
                                 [-o {port}] [--port=port]
                                 [-d {databasename}] [--db=databasename]

db variables:
    dbname - the name to use for the new database. If it exists, it will be dropped.
    drop - if the database already exists, should it be dropped?     
    opts - list of variables supplied from command line arguments or manually input
    engine - specifies the database engine (MySQL, PostgreSQL, etc.)    

table variables:
    tablename - the name to use for the new table.
    drop - if the table already exists, should it be dropped?
    pk - the name of the value to be used as primary key. If None, no primary key will
         be used. The primary key must be the first column in dbcolumns.
    hasindex - True if the database file already includes an index
    record_id - the number of rows already entered into a table
    source - the open file or url containing the data
    delimiter - the delimiter used in the text file. If None, whitespace will be assumed.
    header_rows - number of header rows to be skipped
    cleanup - the name of the cleanup function to be used (or no_cleanup for none)
    dbcolumns - a list of tuples, containing each column name and its data type.
                The number of values in each row of the text file must correspond with
                the number of columns defined.
                Data type is also a tuple, with the first value specifying the type.
                (The second part of the type specifies the length and is optional)
                    pk      - primary key
                    int     - integer
                    double  - double precision
                    char    - string
                    bit     - binary
                    skip    - ignore this row
                    combine - append this row's data to the data of the previous row 
"""

import getpass
import getopt
import urllib
import warnings
import os
import sys
import zipfile

warnings.filterwarnings("ignore")

raw_data_location = "raw_data"

class DbTk:
    """This class represents a database toolkit script. Scripts should inherit from this class
    and execute their code in the download method."""
    name = ""
    url = ""
    def download(self, engine=None):
        pass
    def checkengine(self, engine=None):
        if not engine:
            opts = get_opts()        
            engine = choose_engine(opts)
        return engine
    
class Cleanup:
    """This class represents a custom cleanup function and a dictionary of arguments
    to be passed to that function."""
    def __init__(self, function, args):
        self.function = function
        self.args = args

def no_cleanup(value, args):
    """Default cleanup function, returns the unchanged value."""
    return value        

class Database:
    """Information about a database."""
    dbname = ""
    drop = True
    opts = dict()
    
class Table:
    """Information about a database table."""
    tablename = ""
    pk = True
    hasindex = False
    record_id = 0
    delimiter = None
    columns = []
    drop = True
    header_rows = 1
    fixedwidth = False
    def __init__(self):        
        self.cleanup = Cleanup(no_cleanup, None)        
    
class Engine():
    """A generic database system. Specific database platforms will inherit from this class."""
    name = ""
    db = None
    table = None
    connection = None
    cursor = None
    keep_raw_data = False
    use_local = True
    datatypes = []
    required_opts = []
    pkformat = "%s PRIMARY KEY"
    def add_to_table(self):
        """This function adds data to a table from one or more lines specified in engine.table.source."""        
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
                cleanvalues = [self.format_insert_value(self.table.cleanup.function(value, 
                                                                                    self.table.cleanup.args)) 
                               for value in linevalues]
                insertstatement = self.insert_statement(cleanvalues)
                inserting = "Inserting rows: "
                sys.stdout.write(inserting + str(self.table.record_id) + "\b" * (len(str(self.table.record_id)) + len(inserting)))
                self.cursor.execute(insertstatement)
                
        print "\n Done!"
        self.connection.commit()
        self.table.source.close()
    def convert_data_type(self, datatype):
        """Converts DBTK generic data types to database platform specific data types"""
        datatypes = dict()
        thistype = datatype[0]
        thispk = False
        if thistype[0:3] == "pk-":
            thistype = thistype.lstrip("pk-")
            thispk = True
        datatypes["auto"], datatypes["int"], datatypes["double"], datatypes["char"], datatypes["bit"] = range(5)
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
        """Creates a new database based on settings supplied in Database object engine.db"""
        print "Creating database " + self.db.dbname + " . . ."
        # Create the database    
        self.cursor.execute(self.create_db_statement())
    def create_db_statement(self):
        """Returns a SQL statement to create a database."""
        if self.db.drop:
            self.cursor.execute(self.drop_statement("DATABASE", self.db.dbname))
            createstatement = "CREATE DATABASE " + self.db.dbname
        else:
            createstatement = "CREATE DATABASE IF NOT EXISTS " + db.dbname
        return createstatement
    def create_raw_data_dir(self):
        """Checks to see if the archive directory exists and creates it if necessary."""
        if not os.path.exists(raw_data_location):
            os.makedirs(raw_data_location)
    def create_table(self):
        """Creates a new database table based on settings supplied in Table object engine.table."""
        print "Creating table " + self.table.tablename + " in database " + self.db.dbname + " . . ."
        createstatement = self.create_table_statement()
        self.cursor.execute(createstatement)
    def create_table_statement(self):
        """Returns a SQL statement to create a table."""
        if self.table.drop:
            self.cursor.execute(self.drop_statement("TABLE", self.tablename()))
            createstatement = "CREATE TABLE " + self.tablename() + " ("
        else:
            createstatement = "CREATE TABLE IF NOT EXISTS " + self.tablename() + " ("    
        for item in self.table.columns:
            if (item[1][0] != "skip") and (item[1][0] != "combine"):
                createstatement += item[0] + " " + self.convert_data_type(item[1]) + ", "    

        createstatement = createstatement.rstrip(', ')    
        createstatement += " );"
        return createstatement
    def drop_statement(self, objecttype, objectname):
        """Returns a drop table or database SQL statement."""
        dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
        return dropstatement
    def extract_values(self, line):
        """Given a line of data, this function returns a list of the individual data values."""
        if self.table.fixedwidth:
            pos = 0
            values = []
            for width in self.table.fixedwidth:
                values.append(line[pos:pos+width].strip())
                pos += width
            return values
        else:
            return line.split(self.table.delimiter)
    def format_filename(self, filename):
        """Returns the full path of a file in the archive directory."""
        return os.path.join(raw_data_location, self.scriptname + " - " + filename)
    def format_insert_value(self, value):
        """Formats a value for an insert statement, for example by surrounding it in single quotes."""
        strvalue = str(value)
        if strvalue.lower() == "null":
            return "null"
        elif value:
            quotes = ["'", '"']            
            if strvalue[0] == strvalue[-1] and strvalue[0] in quotes:
                return "'" + strvalue.strip(''.join(quotes)) + "'" 
            else:
                return "'" + strvalue + "'" 
        else:
            return "null"
    def get_input(self):
        """Manually get user input for connection information when script is run from terminal."""
        for opt in self.required_opts:
            if self.opts[opt[0]] == "":
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
            if (thistype != "skip") and (thistype !="combine") and (self.table.hasindex == True
                                                                    or thistype[0:3] != "pk-"):
                columns += item[0] + ", "
        columns = columns.rstrip(', ')
        if join:
            return columns
        else:
            return columns.lstrip("(").rstrip(")").split(", ")
    def insert_data_from_archive(self, url, filename):
        """Insert data from a file located in an online archive. This function extracts the
        file, inserts the data, and deletes the file if raw data archiving is not set."""
        if self.use_local and os.path.isfile(self.format_filename(filename)):
            # Use local copy
            print "Using local copy of " + filename
            self.insert_data_from_file(self.format_filename(filename))            
        else:
            self.create_raw_data_dir()
            
            archivename = os.path.join(raw_data_location, url.split('/')[-1])
            web_file = urllib.urlopen(url)    
            local_zip = open(archivename, 'wb')
            local_zip.write(web_file.read())
            local_zip.close()
            web_file.close()    
                    
            local_zip = zipfile.ZipFile(archivename)
            fileloc = self.format_filename(filename)
                    
            open_zip = local_zip.open(filename)
            unzipped_file = open(fileloc, 'wb')
            unzipped_file.write(open_zip.read())
            unzipped_file.close()
            open_zip.close()
            
            local_zip.close()
            os.remove(archivename)
                
            self.insert_data_from_file(fileloc)            
            
            if not self.keep_raw_data:
                os.remove(fileloc)            
    def insert_data_from_file(self, filename):
        """The default function to insert data from a file. This function simply inserts the 
        data row by row. Database platforms with support for inserting bulk data from files
        can override this function."""
        self.table.source = self.skip_rows(self.table.header_rows, open(filename, "r"))        
        self.add_to_table()
    def insert_data_from_url(self, url):
        """Insert data from a web resource, such as a text file."""
        filename = url.split('/')[-1]
        if self.use_local and os.path.isfile(self.format_filename(filename)):
            # Use local copy
            print "Using local copy of " + filename
            self.insert_data_from_file(self.format_filename(filename))            
        else:
            if self.keep_raw_data:
                # Save a copy of the file locally, then load from that file
                self.create_raw_data_dir()                        
                print "Saving a copy of " + filename + " . . ."
                webFile = urllib.urlopen(url)   
                localFile = open(self.format_filename(filename), 'wb')
                localFile.write(webFile.read())
                localFile.close()
                self.insert_data_from_file(self.format_filename(filename))
            else:
                # Don't save the file, just load it from the web resource
                self.table.source = self.skip_rows(self.table.header_rows, urllib.urlopen(url))
                self.add_to_table()
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
        # Run correct_invalid_value on each value before insertion
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


class MySQLEngine(Engine):
    """Engine instance for MySQL."""
    name = "MySQL"
    datatypes = ["INT(5) NOT NULL AUTO_INCREMENT", 
                 "INT", 
                 "DOUBLE", 
                 "VARCHAR", 
                 "BIT"]
    required_opts = [["username", "Enter your MySQL username: ", "root"],
                     ["password", "Enter your password: ", ""],
                     ["hostname", "Enter your MySQL host or press Enter for the default (localhost): ", "localhost"],
                     ["sqlport", "Enter your MySQL port or press Enter for the default (3306): ", 3306]]
    def insert_data_from_file(self, filename):
        """Calls MySQL "LOAD DATA LOCAL INFILE" statement to perform a bulk insert."""
        if self.table.cleanup.function == no_cleanup:
            print "Inserting data from " + filename + " . . ."
                
            columns = self.get_insert_columns()            
            statement = """        
LOAD DATA LOCAL INFILE '""" + filename + """'
INTO TABLE """ + self.tablename() + """
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\\n'
IGNORE """ + str(self.table.header_rows) + """ LINES 
(""" + columns + ")"
            
            self.cursor.execute(statement)
        else:
            return Engine.insert_data_from_file(self, filename)            
    def get_cursor(self):
        """Gets the db connection and cursor."""
        import MySQLdb as dbapi
        self.get_input()                
        self.connection = dbapi.connect(host = self.opts["hostname"],
                                        port = int(self.opts["sqlport"]),
                                        user = self.opts["username"],
                                        passwd = self.opts["password"])     
        self.cursor = self.connection.cursor()    


class PostgreSQLEngine(Engine):
    """Engine instance for PostgreSQL."""
    name = "PostgreSQL"
    datatypes = ["serial", 
                 "integer", 
                 "double precision", 
                 "varchar", 
                 "bit"]    
    required_opts = [["username", "Enter your PostgreSQL username: ", "postgres"],
             ["password", "Enter your password: ", ""],
             ["hostname", "Enter your PostgreSQL host or press Enter for the default (localhost): ", "localhost"],
             ["sqlport", "Enter your PostgreSQL port or press Enter for the default (5432): ", 5432],
             ["database", "Enter your PostgreSQL database name or press Enter for the default (postgres): ", "postgres"]]
    def create_db_statement(self):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        return Engine.create_db_statement(self).replace(" DATABASE ", " SCHEMA ")
    def create_table(self):
        """PostgreSQL needs to commit operations individually."""
        Engine.create_table(self)
        self.connection.commit()
    def drop_statement(self, objecttype, objectname):
        """In PostgreSQL, the equivalent of a SQL database is a schema."""
        dropstatement = Engine.drop_statement(self, objecttype, objectname) + " CASCADE;"
        return dropstatement.replace(" DATABASE ", " SCHEMA ")    
    def insert_data_from_file(self, filename):
        """Use PostgreSQL's "COPY FROM" statement to perform a bulk insert."""
        if ([self.table.cleanup.function, self.table.delimiter, self.table.header_rows] == 
                                                        [no_cleanup, ",", 1]):        
            print "Inserting data from " + filename + " . . ."
                
            columns = self.get_insert_columns()    
            filename = os.path.abspath(filename)
            statement = """
COPY """ + self.tablename() + " (" + columns + """)
FROM '""" + filename + """'
WITH DELIMITER ','
CSV HEADER"""
            try:
                self.cursor.execute(statement)
                self.connection.commit()
            except:
                self.connection.rollback()
                return Engine.insert_data_from_file(self, filename)
        else:
            return Engine.insert_data_from_file(self, filename)                
    def get_cursor(self):
        """Gets the db connection and cursor."""
        import psycopg2 as dbapi    
        self.get_input()            
        self.connection = dbapi.connect(host = self.opts["hostname"],
                                        port = int(self.opts["sqlport"]),
                                        user = self.opts["username"],
                                        password = self.opts["password"],
                                        database = self.opts["database"])        
        self.cursor = self.connection.cursor()    


class SQLiteEngine(Engine):
    """Engine instance for SQLite."""
    name = "SQLite"
    datatypes = ["INTEGER",
                 "INTEGER",
                 "REAL",
                 "TEXT",
                 "INTEGER"]
    required_opts = [["database", "Enter the filename of your SQLite database: ", "sqlite.db"]]
    def create_db(self):
        """SQLite doesn't create databases; each database is a file and needs a separate connection."""
        return None
    def tablename(self):
        """The database file is specifically connected to, so database.table is not necessary."""        
        return "'" + self.table.tablename + "'"    
    def get_cursor(self):
        """Gets the db connection and cursor."""
        import sqlite3 as dbapi    
        self.get_input()
        self.connection = dbapi.connect(self.opts["database"])
        self.cursor = self.connection.cursor()               


def get_opts():
    """Checks for command line arguments"""
    optsdict = dict()
    for i in ["engine", "username", "password", "hostname", "sqlport", "database"]:
        optsdict[i] = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:u:p:hod", ["engine=", "user=", "password=", "host=", "port=", "database="])        
        for opt, arg in opts:            
            if opt in ("-e", "--engine"):      
                optsdict["engine"] = arg                            
            if opt in ("-u", "--user"):      
                optsdict["username"] = arg                            
            elif opt in ("-p", "--password"):     
                optsdict["password"] = arg
            elif opt in ("-h", "--host"):                 
                if arg == "":
                    optsdict["hostname"] = "default"
                else:
                    optsdict["hostname"] = arg
            elif opt in ("-o", "--port"): 
                try:
                    optsdict["sqlport"] = int(arg)
                except ValueError:
                    optsdict["sqlport"] = "default"                 
            elif opt in ("-d", "--database"): 
                if arg == "":
                    optsdict["database"] = "default"
                else:
                    optsdict["database"] = arg                                 
                 
    except getopt.GetoptError:
        pass
    
    return optsdict   


def choose_engine(opts):
    """Prompts the user to select a database engine"""    
    enginename = opts["engine"]
    
    if enginename == "":
        print "Choose a database engine:"
        print "    (m) MySQL"
        print "    (p) PostgreSQL"
        print "    (s) SQLite"
        enginename = raw_input(": ")
        enginename = enginename.lower()
    
    engine = Engine()
    if enginename == "mysql" or enginename == "m" or enginename == "":
        engine = MySQLEngine()
    elif enginename == "postgresql" or enginename == "p":
        engine = PostgreSQLEngine()
    elif enginename == "sqlite" or enginename == "s":
        engine = SQLiteEngine()
        
    engine.opts = opts
    return engine

all_engines = [MySQLEngine(), PostgreSQLEngine(), SQLiteEngine()]

def final_cleanup():
    """Perform final cleanup operations after all scripts have run."""
    try:
        os.rmdir(raw_data_location)
    except OSError:
        pass