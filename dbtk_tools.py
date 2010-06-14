"""Database Toolkit tools"""

import getpass
import MySQLdb as dbapi

def get_database_info():
    """Get login information for MySQL database"""
    username = raw_input("Enter your MySQL username: ")
    password = getpass.getpass("Enter your MySQL password: ")
    hostname = raw_input("Enter your MySQL host or press Enter for the default (localhost): ")
    if hostname == '':
        hostname = 'localhost'
    mysqlport = raw_input("Enter your MySQL port (or press Enter for the default (3306): ")
    if mysqlport == '':
        mysqlport = 3306
    mysqlport = int(mysqlport)
    return [username, password, hostname, mysqlport]