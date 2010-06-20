"""Database Toolkit tools"""

import getpass
import MySQLdb as dbapi
import sys
import getopt

def get_database_info():
    """Get login information for MySQL database"""
    username = ""
    password = ""
    hostname = ""
    sqlport = 0
    
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
                    
    return manual_input(username, password, hostname, sqlport)
    
def manual_input(username, password, hostname, sqlport):    
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
    return [username, password, hostname, sqlport]

def connect_to_database():
    """Connect to a database management system and return the cursor"""
    databaseinfo = get_database_info()
    connection = dbapi.connect(host = databaseinfo[2],
                               port = databaseinfo[3],
                               user = databaseinfo[0],
                               passwd = databaseinfo[1])
    cursor = connection.cursor()
    return cursor