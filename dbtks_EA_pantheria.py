"""Database Toolkit for Pantheria dataset

"""

from dbtk_ui import *

class EAPantheria(DbTk):
    name = "Pantheria"
    shortname = "Pantheria"
    url = ""
    required_opts = []
    def download(self, engine=None):            
        # Variables to get text file/create database        
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "Pantheria"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "pantheria"
        table.delimiter = "\t"
        table.cleanup = Cleanup(correct_invalid_value, {"nulls":("-999", "-999.00", -999)} )
        
        engine.table = table
        engine.auto_insert_from_url("http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt")
        
        return engine
    
    
class EAPantheriaTest(DbTkTest):
    def test_EAPantheria(self):        
        DbTkTest.default_test(self,
                              EAPantheria(),
                              [("pantheria",
                                "4d2d9c2f57f6ae0987aafd140aace1e3",
                                "sporder, family, genus, species")
                              ])
        
        
if __name__ == "__main__":
    me = EAPantheria()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())