"""Database Toolkit for Mammalian Life History Database
Setup and install the Mammalian Life History Database published by Ernest
(2003) in Ecological Archives. 

See dbtk_tools.py for usage

"""

from dbtk_tools import *
import datacleanup

# Variables to get text file/create database
db = Database()
db.dbname = "MammalLifeHistory"
db.opts = get_opts()
db.engine = choose_engine(db)
db.cursor = get_cursor(db)
create_database(db)

table = Table()
table.tablename = "species"
table.pk = "species_id"
table.source = open_url(table, "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt")
table.cleanup = datacleanup.correct_invalid_value

# Database column names and their data types. Use data type "skip" to skip the value, and
# "combine" to merge a string value into the previous column
table.columns=[("species_id"            ,   ("pk",)         ),
               ("sporder"               ,   ("char", 20)    ),
               ("family"                ,   ("char", 20)    ),
               ("genus"                 ,   ("char", 20)    ),
               ("species"               ,   ("char", 20)    ),
               ("mass"                  ,   ("double",)     ),
               ("gestation_period"      ,   ("double",)     ),
               ("newborn_mass"          ,   ("double",)     ),
               ("wean_age"              ,   ("double",)     ),
               ("wean_mass"             ,   ("double",)     ),
               ("afr"                   ,   ("double",)     ),
               ("max_lifespan"          ,   ("double",)     ),
               ("litter_size"           ,   ("double",)     ),
               ("litters_peryear"       ,   ("double",)     ),
               ("refs"                  ,   ("char", 30)    )]
create_table(db, table)