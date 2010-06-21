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
import dbtk_tools
import datacleanup
import warnings
import sys

class db_info:
    """Information about database to be passed to dbtk_tools.setup"""
    dbname = ""
    tablename = ""
    pk = None
    url = ""
    delimiter = None
    dbcolumns = []
    cursor = None

def setup(dbinfo):
    """Creates a database based on settings supplied in dbinfo object"""
    warnings.filterwarnings("ignore")
    
    # Connect to the database    
    dbinfo.cursor.execute("DROP DATABASE IF EXISTS " + dbinfo.dbname)
    dbinfo.cursor.execute("CREATE DATABASE " + dbinfo.dbname)
    dbinfo.cursor.execute("USE " + dbinfo.dbname)
    
    # Create the table
    createstatement = "CREATE TABLE " + dbinfo.tablename + "("
    for item in dbinfo.dbcolumns:
        if (item[1] != "skip") and (item[1] != "combine"):
            createstatement += item[0] + " " + item[1] + ", "    
    if dbinfo.pk:
        createstatement += "PRIMARY KEY (" + dbinfo.pk + ")"
    else:
        createstatement = createstatement.rstrip(', ')    
    createstatement += ")"  
    
    print "Creating table " + dbinfo.tablename + " in database " + dbinfo.dbname + " . . ."
    dbinfo.cursor.execute(createstatement)
    
    main_table = urllib.urlopen(dbinfo.url)
    
    # Skip over the header line by reading it before processing
    line = main_table.readline()
    
    print "Inserting rows: "
    species_id = 0    
    for line in main_table:
        
        line = line.strip()
        if line:
            # If there is a primary key specified, add an auto-incrementing integer            
            if dbinfo.pk:
                species_id += 1
                linevalues = [species_id]
                column = 0
            else:
                linevalues = []
                column = -1 
            for value in line.split(dbinfo.delimiter):
                column += 1
                thiscolumn = dbinfo.dbcolumns[column][1]
                # If data type is "skip" ignore the value
                if thiscolumn != "skip":
                    if thiscolumn == "combine":
                        # If "combine" append value to end of previous column
                        linevalues[len(linevalues) - 1] += " " + value 
                    else: 
                        # Otherwise, add new value
                        linevalues.append(value)
            # Build insert statement with the correct # of values
            insertstatement = "INSERT INTO " + dbinfo.tablename + " VALUES ("
            for value in linevalues:
                insertstatement += "%s, "
            insertstatement = insertstatement.rstrip(", ") + ")"

            sys.stdout.write(str(species_id) + "\b" * len(str(species_id)))
            dbinfo.cursor.execute(insertstatement, 
                           # Run correct_invalid_value on each value before insertion
                           [datacleanup.correct_invalid_value(value) for value in linevalues])
            
    print "\n Done!"
    main_table.close()    
    
    
def get_cursor_mysql():
    """Get login information for MySQL database"""
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
        sqlport = raw_input("Enter your MySQL port (or press Enter for the default (3306): ")
        if sqlport == '':
            sqlport = 3306
        sqlport = int(sqlport)
    connection = dbapi.connect(host = hostname,
                               port = sqlport,
                               user = username,
                               passwd = password)    
    cursor = connection.cursor()
    return cursor