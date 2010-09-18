"""Database Toolkit for Avian Body Size

Authors: Terje Lislevand, Jordi Figuerola, and Tamas Szekely
Published: Ecological Archives, 2007
 
"""

from .lib.ui import *

class main(DbTk):
    name = "Avian Body Size (Ecological Archives 2007)"
    shortname = "AvianBodySize"
    url = "http://esapubs.org/archive/ecol/E088/096/avian_ssd_jan07.txt"
    def download(self, engine=None):    
        DbTk.download(self, engine)
        self.engine.auto_create_table(self.url, "species")
        self.engine.insert_data_from_url(self.url)
        return self.engine
    
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
                              main(),
                              [("species",
                                "94220c1db99252ecf58ca2d9654d192a",
                                "record_id")
                              ])