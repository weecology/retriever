"""Database Toolkit for Ernest 2003 Ecological Archives
Mammalian Life History Database

Usage: python dbtk_ernest2003.py [-u username] [--user=username] 
                                 [-p password] [--password=password]
                                 [-h {hostname} (default=localhost)] [--host=hostname] 
                                 [-o {port} (default=3306)] [--port=port]

"""

import dbtk_tools

# Variables to get text file/create database
dbinfo = dbtk_tools.db_info()
dbinfo.dbname = "MammalLifeHistory"
dbinfo.tablename = "species"
dbinfo.pk = "species_id"
dbinfo.url = "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"

# Database column names and their data types. Use data type "skip" to skip the value, and
# "combine" to merge a string value into the previous column
dbinfo.dbcolumns=[("species_id"        ,   "INT(5) NOT NULL AUTO_INCREMENT"),
                  ("sporder"           ,   "CHAR(20)"),
                  ("family"            ,   "CHAR(20)"),
                  ("genus"             ,   "CHAR(20)"),
                  ("species"           ,   "CHAR(20)"),
                  ("mass"              ,   "DECIMAL(11,2)"),
                  ("gestation_period"  ,   "DECIMAL(5,2)"),
                  ("newborn_mass"      ,   "DECIMAL(9,2)"),
                  ("wean_age"          ,   "DECIMAL(5,2)"),
                  ("wean_mass"         ,   "DECIMAL(10,2)"),
                  ("afr"               ,   "DECIMAL(5,2)"),
                  ("max_lifespan"      ,   "DECIMAL(6,2)"),
                  ("litter_size"       ,   "DECIMAL(5,2)"),
                  ("litters_peryear"   ,   "DECIMAL(5,2)"),
                  ("refs"              ,   "CHAR(30)")]
    
dbinfo.cursor = dbtk_tools.get_cursor_mysql()
dbtk_tools.setup(dbinfo)