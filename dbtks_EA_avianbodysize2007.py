"""Database Toolkit for Avian Body Size

Authors: Terje Lislevand, Jordi Figuerola, and Tamas Szekely
Published: Ecological Archives, 2007
 
"""

from dbtk_ui import *

class EAAvianBodySize2007(DbTk):
    name = "Avian Body Size - Ecological Archives 2007"
    shortname = "AvianBodySize"
    url = ""
    required_opts = []
    def download(self, engine=None):    
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "AvianBodySize"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "species"
        table.delimiter = "\t"
        table.cleanup = Cleanup(correct_invalid_value, {"nulls":("-999", "-999.00", -999,
                                                                 Decimal("-999.0"))} )
        
        # Database column names and their data types. Use data type "skip" to skip the value, and
        # "combine" to merge a string value into the previous column
        table.columns=[("record_id"             ,   ("pk-auto",)    ),
                       ("family_id"             ,   ("int",)        ),
                       ("species_id"            ,   ("int",)        ),
                       ("species_name"          ,   ("char",50)     ),
                       ("common_name"           ,   ("char",50)     ),
                       ("subspecies"            ,   ("char",50)     ),
                       ("M_mass"                ,   ("double",)     ),
                       ("M_mass_N"              ,   ("double",)     ),
                       ("F_mass"                ,   ("double",)     ),
                       ("F_mass_N"              ,   ("double",)     ),
                       ("unsexed_mass"          ,   ("double",)     ),
                       ("unsexed_mass_N"        ,   ("double",)     ),
                       ("M_wing"                ,   ("double",)     ),
                       ("M_wing_N"              ,   ("double",)     ),
                       ("F_wing"                ,   ("double",)     ),
                       ("F_wing_N"              ,   ("double",)     ),
                       ("unsexed_wing"          ,   ("double",)     ),
                       ("unsexed_wing_N"        ,   ("double",)     ),
                       ("M_tarsus"              ,   ("double",)     ),
                       ("M_tarsus_N"            ,   ("double",)     ),
                       ("F_tarsus"              ,   ("double",)     ),
                       ("F_tarsus_N"            ,   ("double",)     ),
                       ("unsexed_tarsus"        ,   ("double",)     ),
                       ("unsexed_tarsus_N"      ,   ("double",)     ),                       
                       ("M_bill"                ,   ("double",)     ),
                       ("M_bill_N"              ,   ("double",)     ),
                       ("F_bill"                ,   ("double",)     ),
                       ("F_bill_N"              ,   ("double",)     ),
                       ("unsexed_bill"          ,   ("double",)     ),
                       ("unsexed_bill_N"        ,   ("double",)     ),
                       ("M_tail"                ,   ("double",)     ),
                       ("M_tail_N"              ,   ("double",)     ),
                       ("F_tail"                ,   ("double",)     ),
                       ("F_tail_N"              ,   ("double",)     ),
                       ("unsexed_tail"          ,   ("double",)     ),
                       ("unsexed_tail_N"        ,   ("double",)     ),
                       ("clutch_size"           ,   ("double",)     ),
                       ("egg_mass"              ,   ("double",)     ),
                       ("mating_system"         ,   ("double",)     ),
                       ("display"               ,   ("double",)     ),                       
                       ("resource"              ,   ("double",)     ),                       
                       ("refs"                  ,   ("char",30)     )]
        engine.table = table
        engine.create_table()
        
        engine.insert_data_from_url("http://esapubs.org/archive/ecol/E088/096/avian_ssd_jan07.txt")
        
        return engine
    
    
class EAAvianBodySize2007Test(DbTkTest):
    def strvalue(self, value, col_num):
        a = DbTkTest.strvalue(self, value, col_num)
        # Some integer columns end in .00, but the following do not,
        # so the trailing zeroes need to be removed
        if col_num in (0,1,6,8,10,12,14,16,18,20,22,
                       24,26,27,28,30,32,37,38,39):
            if a[-3:] == ".00":
                a = a[0:-3]
        return a
    
    def test_EAAvianBodySize2007(self):        
        DbTkTest.default_test(self,
                              EAAvianBodySize2007(),
                              [("species",
                                "94220c1db99252ecf58ca2d9654d192a",
                                "species_id")
                              ])
        
        
if __name__ == "__main__":
    me = EAAvianBodySize2007()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())