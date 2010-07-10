"""Database Toolkit Tools
This module contains functions used to run database toolkits.
"""

import getpass
import getopt
import warnings
import os
import sys

warnings.filterwarnings("ignore")

raw_data_location = "raw_data"

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

def final_cleanup():
    """Perform final cleanup operations after all scripts have run."""
    try:
        os.rmdir(raw_data_location)
    except OSError:
        pass