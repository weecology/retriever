"""Database Toolkit auto-generator

Runs an automatic DbTk based on an input URL.
 
"""

from dbtk_ui import *

if __name__ == "__main__":
    url = raw_input("URL:")
    dbname = raw_input("Database:")
    tablename = raw_input("Table:")
    me = AutoDbTk(dbname + "." + tablename, dbname, tablename, url)
    
    final_cleanup(me.download())