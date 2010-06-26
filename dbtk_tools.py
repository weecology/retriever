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
    cursor - a cursor from the database connection    

table variables:
    tablename - the name to use for the new table.
    drop - if the table already exists, should it be dropped?
    pk - the name of the value to be used as primary key. If None, no primary key will
         be used. The primary key must be the first column in dbcolumns.
    hasindex - True if the database file already includes an index
    startindex - the number of rows already entered into a table
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

def no_cleanup(value):
    """Default cleanup function, returns the unchanged value"""
    return value 

class Database:
    """Information about database to be passed to dbtk_tools.create_table"""
    dbname = ""
    engine = "MySQL"
    cursor = None
    drop = True
    opts = dict()
    
class Table:
    """Information about table to be passed to dbtk_tools.create_table"""
    tablename = ""
    pk = None
    hasindex = False
    startindex = 0
    lines = []
    delimiter = None
    columns = []
    drop = True
    header_rows = 1
    cleanup = no_cleanup
    nullindicators = set(["-999", "-999.00", -999])

def create_database(db):
    """Creates a database/schema based on settings supplied in table object"""
    # Create the database/schema
    if db.engine == "postgresql":
        object = "SCHEMA"
    else:
        object = "DATABASE"
    
    if db.engine != "sqlite":   
        if db.drop:
            db.cursor.execute(drop_statement(db.engine, object, db.dbname))
            db.cursor.execute("CREATE " + object + " " + db.dbname)
        else:
            db.cursor.execute("CREATE " + object + " IF NOT EXISTS " + db.dbname)    

def create_table(db, table):
    """Creates a table based on settings supplied in table object"""
    warnings.filterwarnings("ignore")        
    
    # Create the table
    if table.drop:
        db.cursor.execute(drop_statement(db.engine, "TABLE", tablename(db, table)))
        createstatement = "CREATE TABLE " + tablename(db, table) + "("
    else:
        createstatement = "CREATE TABLE IF NOT EXISTS " + tablename(db, table) + "("    
    for item in table.columns:
        if (item[1][0] != "skip") and (item[1][0] != "combine"):
            createstatement += item[0] + " " + convert_data_type(db.engine, item[1]) + ", "    
    if table.pk and db.engine == "mysql":
        createstatement += "PRIMARY KEY (" + table.pk + ")"
    else:
        createstatement = createstatement.rstrip(', ')    
    createstatement += ")"  
    
    print "Creating table " + table.tablename + " in database " + db.dbname + " . . ."
    db.cursor.execute(createstatement)
    #return add_to_table(db, table)

def add_to_table(db, table):
    print "Inserting rows: "
    
    record_id = table.startindex    
    for line in table.source:
        
        line = line.strip()
        if line:
            record_id += 1            
            linevalues = []
            if table.pk:
                column = 0
            else:
                column = -1
             
            for value in line.split(table.delimiter):
                column += 1
                thiscolumn = table.columns[column][1][0]
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
            columns = get_insert_columns(db, table)
            columncount = len(get_insert_columns(db, table, False))
            insertstatement = "INSERT INTO " + tablename(db, table)
            insertstatement += " (" + columns + ")"  
            insertstatement += " VALUES ("
            for i in range(0, columncount):
                insertstatement += "%s, "
            insertstatement = insertstatement.rstrip(", ") + ");"
            sys.stdout.write(str(record_id) + "\b" * len(str(record_id)))
            # Run correct_invalid_value on each value before insertion
            cleanvalues = [format_insert_value(table.cleanup(value, db, table)) for value in linevalues]
            insertstatement %= tuple(cleanvalues)
            db.cursor.execute(insertstatement)
            
    print "\n Done!"
    table.source.close()
    return record_id

def format_insert_value(value):
    print value
    if value:
        return "'" + str(value) + "'"
    else:
        return "null"
    
def insert_data_from_file(db, table, filename):
    print "Inserting data from " + filename + " . . ."
        
    columns = get_insert_columns(db, table)    
    
    if db.engine == "mysql":   
        statement = """        
LOAD DATA LOCAL INFILE '""" + filename + """'
INTO TABLE """ + tablename(db, table) + """
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\\n'
IGNORE 1 LINES 
(""" + columns + ")"
    elif db.engine == "postgresql":
        filename = os.path.abspath(filename)
        statement = """
COPY """ + tablename(db, table) + " (" + variables + """)
FROM '""" + filename + """'
WITH DELIMITER ','
CSV HEADER"""
    
    db.cursor.execute(statement)    
    
def tablename(db, table):
    if db.engine == "mysql" or db.engine=="postgresql":
        return db.dbname + "." + table.tablename
    elif db.engine == "sqlite":
        return table.tablename
    
def get_insert_columns(db, table, join=True):
    columns = ""
    for item in table.columns:
        if (item[1][0] != "skip") and (item[1][0] !="combine") and (item[1][0] != 
                                                        "pk" or table.hasindex == True):
            columns += item[0] + ", "            
    columns = columns.rstrip(', ')
    if join:
        return columns
    else:
        return columns.lstrip("(").rstrip(")").split(",")    
    
def open_url(table, url):
    """Returns an opened file from a URL, skipping the header lines"""
    source = urllib.urlopen(url)
    source = skip_rows(table.header_rows, source)
    return source

def skip_rows(rows,source):
    """Skip over the header line by reading it before processing"""
    if rows > 0:
        for i in range(rows):
            line = source.readline()
    return source
    
def drop_statement(engine, objecttype, objectname):
    """Returns a db engine specific drop statement"""
    dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
    if engine == "postgresql":
        dropstatement += " CASCADE"
    return dropstatement
    
def convert_data_type(engine, datatype):
    """Converts DBTK generic data types to db engine specific data types"""
    datatypes = dict()
    datatypes["pk"], datatypes["int"], datatypes["double"], datatypes["char"], datatypes["bit"] = range(5)
    datatypes["combine"], datatypes["skip"] = [-1, -1]
    dbdatatypes = dict()    
    dbdatatypes["mysql"] = ["INT(5) NOT NULL AUTO_INCREMENT", 
                            "INT", 
                            "DOUBLE", 
                            "VARCHAR", 
                            "BIT"]
    dbdatatypes["postgresql"] = ["SERIAL PRIMARY KEY", 
                                 "integer", 
                                 "double precision", 
                                 "varchar", 
                                 "bit"]
    dbdatatypes["sqlite"] = ["INTEGER PRIMARY KEY",
                             "INTEGER",
                             "REAL",
                             "TEXT",
                             "INTEGER"
                             ]
    mydatatypes = dbdatatypes[engine.lower()]
    thisvartype = datatypes[datatype[0]]
    if thisvartype > -1:
        type = mydatatypes[thisvartype]
        if len(datatype) > 1:
            type += "(" + str(datatype[1]) + ")"
    else:
        type = ""    
    return type

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

def choose_engine(db):
    """Prompts the user to select a database engine"""    
    engine= db.opts["engine"]
    
    if engine == "":
        print "Choose a database engine:"
        print "    (m) MySQL"
        print "    (p) PostgreSQL"
        print "    (s) SQLite"
        engine = raw_input(": ")
        engine = engine.lower()
    
    if engine == "m" or engine == "":
        engine = "mysql"
    elif engine == "p":
        engine = "postgresql"
    elif engine == "s":
        engine = "sqlite"
        
    print "Using " + engine + " database."
    return engine
    
def get_cursor(db):
    """Returns a db cursor based on the selected db engine"""
    engine = db.engine
    if engine == "mysql":
        return get_cursor_mysql(db)
    elif engine == "postgresql": 
        return get_cursor_pgsql(db)
    elif engine == "sqlite":
        return get_cursor_sqlite(db)
    
    
def get_cursor_mysql(db):
    """Get login information for MySQL database"""
    import MySQLdb as dbapi
                    
    # If any parameters are missing, input them manually
    if db.opts["username"] == "":
        db.opts["username"] = raw_input("Enter your MySQL username: ")
    if db.opts["password"] == "":
        print "Enter your MySQL password: "
        db.opts["password"] = getpass.getpass(" ")
    if db.opts["hostname"] == "":
        db.opts["hostname"] = raw_input("Enter your MySQL host or press Enter for the default (localhost): ")
    if db.opts["sqlport"] == "":
        db.opts["sqlport"] = raw_input("Enter your MySQL port or press Enter for the default (3306): ")
        
    if db.opts["hostname"] in ["", "default"]:
        db.opts["hostname"] = "localhost"
    if db.opts["sqlport"] in ["", "default"]:
        db.opts["sqlport"] = "3306"        
    db.opts["sqlport"] = int(db.opts["sqlport"])
        
    connection = dbapi.connect(host = db.opts["hostname"],
                               port = db.opts["sqlport"],
                               user = db.opts["username"],
                               passwd = db.opts["password"])    
    cursor = connection.cursor()
    return cursor

def get_cursor_pgsql(db):
    """Get login information for PostgreSQL database"""
    import psycopg2 as dbapi    
        
    # If any parameters are missing, input them manually
    if db.opts["username"] == "":
        db.opts["username"] = raw_input("Enter your PostgreSQL username: ")
    if db.opts["password"] == "":
        print "Enter your PostgreSQL password: "
        db.opts["password"] = getpass.getpass(" ")
    if db.opts["hostname"] == "":
        db.opts["hostname"] = raw_input("Enter your PostgreSQL host or press Enter for the default (localhost): ")
    if db.opts["sqlport"] == "":
        db.opts["sqlport"] = raw_input("Enter your PostgreSQL port or press Enter for the default (5432): ")
    if db.opts["database"] == "":
        db.opts["database"] = raw_input("Enter your PostgreSQL database name or press Enter for the default (postgres): ")
    
    if db.opts["hostname"] in ["", "default"]:
        db.opts["hostname"] = "localhost"
    if db.opts["sqlport"] in ["", "default"]:
        db.opts["sqlport"] = "5432"        
    db.opts["sqlport"] = int(db.opts["sqlport"])
    if db.opts["database"] in ["", "default"]:
        db.opts["database"] = "postgres"
        
    
    connection = dbapi.connect(host = db.opts["hostname"],
                               port = db.opts["sqlport"],
                               user = db.opts["username"],
                               password = db.opts["password"],
                               database = db.opts["database"])
    connection.set_isolation_level(0)    
    cursor = connection.cursor()    
    return cursor

def get_cursor_sqlite(db):
    """Get login information for SQLite database"""
    import sqlite3 as dbapi    
        
    # If any parameters are missing, input them manually
    if db.opts["database"] == "":
        db.opts["database"] = raw_input("Enter the filename of your SQLite database: ")
    
    if db.opts["database"] in ["", "default"]:
        db.opts["database"] = "sqlite"        
    
    connection = dbapi.connect(db.opts["database"])    
    cursor = connection.cursor()    
    return cursor