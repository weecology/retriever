"""Database Toolkit for Mammalian Life History Database
Setup and install the Mammalian Life History Database published by Ernest
(2003) in Ecological Archives.
 
"""

from dbtk_ui import *

class EAMammalLifeHistory2003(DbTk):
    name = "Mammalian Life History Database"
    shortname = "MammalLH"
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
        table.cleanup = Cleanup(correct_invalid_value, {"nulls":("-999", "-999.00", -999)} )
        
        # Database column names and their data types. Use data type "skip" to skip the value, and
        # "combine" to merge a string value into the previous column
        table.columns=[("species_id"            ,   ("pk-auto",)    ),
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
        engine.create_table()
        
        engine.insert_data_from_url("http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt")
        
        return engine
    
    
class EAMammalLifeHistory2003Test(DbTkTest):
    def test_EAMammalLifeHistory2003(self):        
        DbTkTest.default_test(self,
                              EAMammalLifeHistory2003(),
                              [("species",
                                "afa09eed4ca4ce5db31d15c4daa49ed3",
                                "sporder, family, genus, species")
                              ])
    
        
if __name__ == "__main__":
    me = EAMammalLifeHistory2003()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())