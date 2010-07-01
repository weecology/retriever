"""Database Toolkit for Mammalian Life History Database
Setup and install the Mammalian Life History Database published by Ernest
(2003) in Ecological Archives. 

See dbtk_tools.py for usage

"""

import datacleanup
from dbtk_tools import *
import dbtk_ui

class DbTk_Ernest(DbTk):
    name = "Mammalian Life History Database"
    url = ""
    required_opts = []
    def download(self, engine=None):    
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "MammalLifeHistory"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "species"
        table.pk = "species_id"        
        table.cleanup = datacleanup.correct_invalid_value
        table.nullindicators = ["-999", "-999.00", -999]
        
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
        engine.table = table
        engine.table.source = engine.open_url("http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt")
        
        engine.create_table()
        engine.add_to_table()
        
        
if __name__ == "__main__":
    me = DbTk_Ernest()
    if len(sys.argv) == 1:                
        dbtk_ui.launch_wizard([me], all_engines)
    else:
        me.download()