"""Database Toolkit for Mammalian Life History Database

Setup and install the Mammalian Life History Databased published by Ernest
(2003) in Ecological Archives.

Usage: python /file/path/to/dbtk_ernest2003.py

"""
import dbtk_from_txt

# Variables to get text file/create database
dbname = "MammalLifeHistory"
tablename = "species"
pk = "species_id"
url = "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
delimiter = None

# Database column names and their data types. Use data type "skip" to skip the value, and
# "combine" to merge a string value into the previous column
dbcolumns=[("species_id"        ,   "INT(5) NOT NULL AUTO_INCREMENT"),
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

dbtk_from_txt.setup(dbname, tablename, pk, url, delimiter, dbcolumns)