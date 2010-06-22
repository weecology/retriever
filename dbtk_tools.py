"""Database Toolkit tools
Call the Setup function to create a database from a delimited text file.

db_info variables:
    dbname - the name to use for the new database. If it exists, it will be dropped.
    tablename - the name to use for the new table.
    pk - the name of the value to be used as primary key. If None, no primary key will
         be used. The primary key must be the first column in dbcolumns.
    url - the URL of the text file.
    delimiter - the delimiter used in the text file. If None, whitespace will be assumed.
    dbcolumns - a list of tuples, containing each column name and its MySQL data type.
                The number of values in each row of the text file must correspond with
                the number of columns defined. Use "skip" as data type to not create a
                column for the value, and "combine" to append a string to the value of
                the previous column (instead of creating a new column).
"""

import getpass
import getopt
import urllib
import datacleanup
import warnings
import sys

class db_info:
    """Information about database to be passed to dbtk_tools.create_table"""
    dbname = ""
    engine = "MySQL"
    cursor = None
    drop = True
    
class table_info:
    """Information about table to be passed to dbtk_tools.create_table"""
    tablename = ""
    pk = None
    sourceurl = ""
    delimiter = None
    columns = []
    drop = True

def create_table(db, table):
    """Creates a database based on settings supplied in dbinfo object"""
    warnings.filterwarnings("ignore")
    
    # Connect to the database
    if db.engine == "postgresql":
        object = "SCHEMA"
    else:
        object = "DATABASE"
            
    if db.drop:
        db.cursor.execute(drop_statement(db.engine, object, db.dbname))
        db.cursor.execute("CREATE " + object + " " + db.dbname)
    else:
        db.cursor.execute("CREATE " + object + " IF NOT EXISTS " + db.dbname)        
    
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
    
    main_table = urllib.urlopen(table.sourceurl)
    
    # Skip over the header line by reading it before processing
    line = main_table.readline()
    
    print "Inserting rows: "
    species_id = 0    
    for line in main_table:
        
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
                           [datacleanup.correct_invalid_value(value) for value in linevalues])
            
    print "\n Done!"
    main_table.close()
    
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
                                 "integer", 
                                 "double precision", 
                                 "varchar(%s)", 
                                 "bit"]
    mydatatypes = dbdatatypes[engine.lower()]
    type = mydatatypes[datatypes[datatype[0]]]
    if len(datatype) > 1 and "%s" in type:
        type = type % datatype[1]    
    return type

def choose_engine():
    print "Choose a database engine:"
    print "    (m) MySQL"
    print "    (p) PostgreSQL"
    engine = raw_input(": ")
    engine = engine.lower()
    if engine == "m":
        engine = "mysql"
    elif engine == "p":
        engine = "postgresql"
    print "Using " + engine + " database."
    return engine
    
def get_cursor(db):
    engine = db.engine
    if engine == "mysql":
        return get_cursor_mysql()
    elif engine == "postgresql": 
        return get_cursor_pgsql()
    
def get_cursor_mysql():
    """Get login information for MySQL/PostgreSQL database"""
    import MySQLdb as dbapi
        
    username = ""
    password = ""
    hostname = ""
    sqlport = 0
    
    # Check for command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:ho", ["user=", "password=", "host=", "port="])        
        for opt, arg in opts:                
            if opt in ("-u", "--user"):      
                username = arg                            
                print "User: " + username
            elif opt in ("-p", "--password"):     
                password = arg
                print "Password: " + "*" * len(password)
            elif opt in ("-h", "--host"): 
                hostname = arg
                if arg == "":
                    hostname = "localhost"
                print "Host: " + hostname
            elif opt in ("-o", "--port"): 
                try:
                    sqlport = int(arg)
                except ValueError:
                    sqlport = 3306
                print "Port: " + str(sqlport) 
    except getopt.GetoptError:
        pass
                    
    # If any parameters are missing, input them manually
    if username == "":
        username = raw_input("Enter your MySQL username: ")
    if password == "":
        password = getpass.getpass("Enter your MySQL password: ")
    if hostname == "":
        hostname = raw_input("Enter your MySQL host or press Enter for the default (localhost): ")
        if hostname == '':
            hostname = 'localhost'
    if sqlport == 0:
        sqlport = raw_input("Enter your MySQL port or press Enter for the default (3306): ")
        if sqlport == '':
            sqlport = 3306
        sqlport = int(sqlport)
    connection = dbapi.connect(host = hostname,
                               port = sqlport,
                               user = username,
                               passwd = password)    
    cursor = connection.cursor()
    return cursor

def get_cursor_pgsql():
    """Get login information for PostgreSQL database"""
    import psycopg2 as dbapi    
        
    username = ""
    password = ""
    hostname = ""
    database = ""
    sqlport = 0
    
    # Check for command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:hod", ["user=", "password=", "host=", "port=", "db="])        
        for opt, arg in opts:                
            if opt in ("-u", "--user"):      
                username = arg                            
                print "User: " + username
            elif opt in ("-p", "--password"):     
                password = arg
                print "Password: " + "*" * len(password)
            elif opt in ("-h", "--host"): 
                hostname = arg
                if arg == "":
                    hostname = "localhost"
                print "Host: " + hostname
            elif opt in ("-o", "--port"): 
                try:
                    sqlport = int(arg)
                except ValueError:
                    sqlport = 5432
                print "Port: " + str(sqlport)
            elif opt in ("-d", "--db"): 
                hostname = arg
                if arg == "":
                    database = "postgres"
                print "Database: " + database 
    except getopt.GetoptError:
        pass
                    
    # If any parameters are missing, input them manually
    if username == "":
        username = raw_input("Enter your PostgreSQL username: ")
    if password == "":
        password = getpass.getpass("Enter your PostgreSQL password: ")
    if hostname == "":
        hostname = raw_input("Enter your PostgreSQL host or press Enter for the default (localhost): ")
        if hostname == '':
            hostname = 'localhost'
    if sqlport == 0:
        sqlport = raw_input("Enter your PostgreSQL port or press Enter for the default (5432): ")
        if sqlport == '':
            sqlport = 5432
        sqlport = int(sqlport)
    if database == "":
        database = raw_input("Enter your PostgreSQL database name or press Enter for the default (postgres): ")
        if database == '':
            database = "postgres"        
    connection = dbapi.connect(host = hostname,
                               port = sqlport,
                               user = username,
                               password = password,
                               database = database)    
    connection.set_isolation_level(0)
    cursor = connection.cursor()
    return cursor