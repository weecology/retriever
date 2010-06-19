# Database Toolkit from text file
# Run the setup function to create a MySQL database from a delimited text file.
# Usage: python dbtk_script.py [-u username] [--user=username] [-p password] [--password=password]
#                              [-h {hostname} (default=localhost)] [--host=hostname] [-o {port} (default=3306) [--port=port]
#
# Variables:
#     dbname - the name to use for the new database. If it exists, it will be dropped.
#     tablename - the name to use for the new table.
#     pk - the name of the value to be used as primary key. If None, no primary key will
#          be used. The primary key must be the first column in dbcolumns.
#     url - the URL of the text file.
#     delimiter - the delimiter used in the text file. If None, whitespace will be assumed.
#     dbcolumns - a list of tuples, containing each column name and its MySQL data type.
#                 The number of values in each row of the text file must correspond with
#                 the number of columns defined. Use "skip" as data type to not create a
#                 column for the value, and "combine" to append a string to the value of
#                 the previous column (instead of creating a new column).

import urllib
import MySQLdb as dbapi
import dbtk_tools
import datacleanup
import warnings
import sys

def setup(dbname, tablename, pk, url, delimiter, dbcolumns):
    warnings.filterwarnings("ignore")
    
    # Connect to the database
    databaseinfo = dbtk_tools.get_database_info()
    connection = dbapi.connect(host = databaseinfo[2],
                               port = databaseinfo[3],
                               user = databaseinfo[0],
                               passwd = databaseinfo[1])
    cursor = connection.cursor() 
    cursor.execute("DROP DATABASE IF EXISTS " + dbname)
    cursor.execute("CREATE DATABASE " + dbname)
    cursor.execute("USE " + dbname)
    
    # Create the table
    createstatement = "CREATE TABLE " + tablename + "("
    for item in dbcolumns:
        if (item[1] != "skip") and (item[1] != "combine"):
            createstatement += item[0] + " " + item[1] + ", "    
    if pk:
        createstatement += "PRIMARY KEY (" + pk + ")"
    else:
        createstatement = createstatement.rstrip(', ')    
    createstatement += ")"  
    
    print "Creating table " + tablename + " in database " + dbname + " . . ."
    cursor.execute(createstatement)
    
    main_table = urllib.urlopen(url)
    
    # Skip over the header line by reading it before processing
    line = main_table.readline()
    
    print "Inserting rows: "
    species_id = 0    
    for line in main_table:
        
        line = line.strip()
        if line:
            # If there is a primary key specified, add an auto-incrementing integer            
            if pk:
                species_id += 1
                linevalues = [species_id]
                column = 0
            else:
                linevalues = []
                column = -1            
            for value in line.split(delimiter):
                column += 1
                thiscolumn = dbcolumns[column][1]
                # If data type is "skip" ignore the value
                if thiscolumn != "skip":
                    if thiscolumn == "combine":
                        # If "combine" append value to end of previous column
                        linevalues[len(linevalues) - 1] += " " + value 
                    else: 
                        # Otherwise, add new value
                        linevalues.append(value)
            # Build insert statement with the correct # of values
            insertstatement = "INSERT INTO " + tablename + " VALUES ("
            for value in linevalues:
                insertstatement += "%s, "
            insertstatement = insertstatement.rstrip(", ") + ")"
                        
            sys.stdout.write(str(species_id) + "\b" * len(str(species_id)))
            cursor.execute(insertstatement, 
                           # Run correct_invalid_value on each value before insertion
                           [datacleanup.correct_invalid_value(value) for value in linevalues])
            
    print "\n Done!"
    main_table.close()    