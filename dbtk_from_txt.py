# Database Toolkit for Ernest 2003 Ecological Archives
# Mammalian Life History Database

# Usage: python /file/path/to/dbtk_ernest2003.py

import urllib
import MySQLdb as dbapi
import dbtk_tools
import datacleanup

def setup(dbname, tablename, pk, url, delimiter, dbcolumns):
    databaseinfo = dbtk_tools.get_database_info()
    connection = dbapi.connect(host = databaseinfo[2],
                               port = databaseinfo[3],
                               user = databaseinfo[0],
                               passwd = databaseinfo[1])
    cursor = connection.cursor() 
    cursor.execute("DROP DATABASE IF EXISTS " + dbname)
    cursor.execute("CREATE DATABASE " + dbname)
    cursor.execute("USE " + dbname)
    
    createstatement = "CREATE TABLE " + tablename + "("
    for item in dbcolumns:
        if (item[1] != "skip") and (item[1] != "combine"):
            createstatement += item[0] + " " + item[1] + ", "    
    if pk:
        createstatement += "PRIMARY KEY (" + pk + ")"
    else:
        createstatement = createstatement.rstrip(', ')    
    createstatement += ")"  
        
    cursor.execute(createstatement)
    
    main_table = urllib.urlopen(url)
    
    # Skip over the header line by reading it before processing
    line = main_table.readline()
    
    species_id = 0
    for line in main_table:
        line = line.strip()
        if line:            
            species_id += 1
            linevalues = [species_id]
            column = 0
            for value in line.split(delimiter):
                column += 1
                thiscolumn = dbcolumns[column][1]
                if thiscolumn != "skip":
                    if thiscolumn == "combine":
                        linevalues[len(linevalues) - 1] += " " + value 
                    else: 
                        linevalues.append(value)
            insertstatement = "INSERT INTO " + tablename + " VALUES ("
            for value in linevalues:
                insertstatement += "%s, "
            insertstatement = insertstatement.rstrip(", ") + ")"        
            cursor.execute(insertstatement, 
                           [datacleanup.correct_invalid_value(value) for value in linevalues])
    main_table.close()    