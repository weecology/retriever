"""Database Toolkit for Mammalian Life History Database

Setup and install the Mammalian Life History Database published by Ernest
(2003) in Ecological Archives.
 
"""

from dbtk.lib.tools import DbTk, DbTkTest

class main(DbTk):
    name = "Mammal Life History Database (Ecological Archives 2003)"
    shortname = "MammalLH"
    url = "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
    def download(self, engine=None):
        DbTk.download(self, engine)
        self.engine.auto_create_table(self.url, "species")
        self.engine.insert_data_from_url(self.url)
        return self.engine
    
class EAErnest2003Test(DbTkTest):
    def test_EAErnest2003(self):        
        DbTkTest.default_test(self,
                              main(),
                              [("species",
                                "afa09eed4ca4ce5db31d15c4daa49ed3",
                                "sporder, family, genus, species")
                              ])