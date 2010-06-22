"""Database Toolkit for Mammalian Life History Database
Setup and install the Mammalian Life History Database published by Ernest
(2003) in Ecological Archives. 

Usage: python dbtk_ernest2003.py [-e engine (mysql, postgresql, etc.)] [--engine=engine]
                                 [-u username] [--user=username] 
                                 [-p password] [--password=password]
                                 [-h {hostname} (default=localhost)] [--host=hostname] 
                                 [-o {port} (default=3306)] [--port=port]

"""

import dbtk_tools

# Variables to get text file/create database
db = dbtk_tools.db_info()
table = dbtk_tools.table_info()
db.dbname = "MammalLifeHistory"
table.tablename = "species"
table.pk = "species_id"
table.sourceurl = "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"

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

db.opts = dbtk_tools.get_opts()
db.engine = dbtk_tools.choose_engine(db)
db.cursor = dbtk_tools.get_cursor(db)
dbtk_tools.create_table(db, table)