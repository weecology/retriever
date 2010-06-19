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
            elif opt in ("-p", "--password"):     
                password = arg
            elif opt in ("-h", "--host"): 
                hostname = arg
                if arg == "":
                    hostname = "localhost"
            elif opt in ("-o", "--port"): 
                try:
                    sqlport = int(arg)
                except ValueError:
                    sqlport = 3306 
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