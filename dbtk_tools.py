"""Database Toolkit tools
Call the Setup function to create a database from a delimited text file.

Supported database engines: MySQL, PostgreSQL

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
                    but     - binary
                    skip    - ignore this row
                    combine - append this row's data to the data of the previous row 
"""

import getpass
import getopt
import urllib
import warnings
import sys

def no_cleanup(value):
    return value 

class db_info:
    """Information about database to be passed to dbtk_tools.create_table"""
    dbname = ""
    engine = "MySQL"
    cursor = None
    drop = True
    opts = dict()
    
class table_info:
    """Information about table to be passed to dbtk_tools.create_table"""
    tablename = ""
    pk = None
    lines = []
    delimiter = None
    columns = []
    drop = True
    header_rows = 1
    cleanup = no_cleanup

def create_table(db, table):
    """Creates a database based on settings supplied in dbinfo object"""
    warnings.filterwarnings("ignore")        
    
    # Create the table
    if table.drop:
        db.cursor.execute(drop_statement(db.engine, "TABLE", db.dbname + "." + table.tablename))
        createstatement = "CREATE TABLE " + db.dbname + "." + table.tablename + "("
    else:
        createstatement = "CREATE TABLE IF NOT EXISTS " + db.dbname + "." + table.tablename + "("    
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
    
    print "Inserting rows: "
    species_id = 0    
    for line in table.source:
        
        line = line.strip()
        if line:
            # If there is a primary key specified, add an auto-incrementing integer            
            if table.pk:
                species_id += 1
                linevalues = [species_id]
                column = 0
            else:
                linevalues = []
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
            insertstatement = "INSERT INTO " + db.dbname + "." + table.tablename + " VALUES ("
            for value in linevalues:
                insertstatement += "%s, "
            insertstatement = insertstatement.rstrip(", ") + ");"

            sys.stdout.write(str(species_id) + "\b" * len(str(species_id)))
            db.cursor.execute(insertstatement, 
                           # Run correct_invalid_value on each value before insertion
                           [table.cleanup(value) for value in linevalues])
            
    print "\n Done!"
    table.source.close()
    
def open_url(table, url):
    source = urllib.urlopen(url)
    
    # Skip over the header line by reading it before processing
    if table.header_rows > 0:
        for i in range(table.header_rows):
            line = source.readline()
    return source
    
def drop_statement(engine, objecttype, objectname):
    dropstatement = "DROP %s IF EXISTS %s" % (objecttype, objectname)
    if engine == "postgresql":
        dropstatement += " CASCADE"
    return dropstatement
    
def convert_data_type(engine, datatype):
    datatypes = dict()
    datatypes["pk"], datatypes["int"], datatypes["double"], datatypes["char"], datatypes["bit"] = range(5)
    datatypes["combine"], datatypes["skip"] = [-1, -1]
    dbdatatypes = dict()    
    dbdatatypes["mysql"] = ["INT(5) NOT NULL AUTO_INCREMENT", 
                            "INT(%s)", 
                            "DOUBLE", 
                            "VARCHAR(%s)", 
                            "BIT"]
    dbdatatypes["postgresql"] = ["integer PRIMARY KEY", 
                                 "integer(%s)", 
                                 "double precision", 
                                 "varchar(%s)", 
                                 "bit"]
    mydatatypes = dbdatatypes[engine.lower()]
    thisvartype = datatypes[datatype[0]]
    if thisvartype > -1:
        type = mydatatypes[thisvartype]
        if len(datatype) > 1 and "%s" in type:
            type = type % datatype[1]
    else:
        type = datatype[0]    
    return type

def get_opts():
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
    engine= db.opts["engine"]
    
    if engine == "":
        print "Choose a database engine:"
        print "    (m) MySQL"
        print "    (p) PostgreSQL"
        engine = raw_input(": ")
        engine = engine.lower()
    
    if engine == "m" or engine == "":
        engine = "mysql"
    elif engine == "p":
        engine = "postgresql"
        
    print "Using " + engine + " database."
    return engine
    
def get_cursor(db):
    engine = db.engine
    if engine == "mysql":
        return get_cursor_mysql(db)
    elif engine == "postgresql": 
        return get_cursor_pgsql(db)
    
def create_database(db):
    # Create the database/schema
    if db.engine == "postgresql":
        object = "SCHEMA"
    else:
        object = "DATABASE"
            
    if db.drop:
        db.cursor.execute(drop_statement(db.engine, object, db.dbname))
        db.cursor.execute("CREATE " + object + " " + db.dbname)
    else:
        db.cursor.execute("CREATE " + object + " IF NOT EXISTS " + db.dbname)    
    
def get_cursor_mysql(db):
    """Get login information for MySQL database"""
    import MySQLdb as dbapi
                    
    # If any parameters are missing, input them manually
    if db.opts["username"] == "":
        db.opts["username"] = raw_input("Enter your MySQL username: ")
    if db.opts["password"] == "":
        db.opts["password"] = getpass.getpass("Enter your MySQL password: ")
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
        db.opts["password"] = getpass.getpass("Enter your PostgreSQL password: ")
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