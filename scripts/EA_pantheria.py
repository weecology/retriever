"""Database Toolkit for Pantheria dataset

"""

from dbtk.lib.templates import EcologicalArchives
from dbtk.lib.tools import DbTkTest


class main(EcologicalArchives):
    name = "Pantheria (Ecological Archives 2008)"
    shortname = "Pantheria"
    tablename = "species"
    url = "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"


class EAPantheriaTest(DbTkTest):
    def test_EAPantheria(self):        
        DbTkTest.default_test(self,
                              main(),
                              [("species",
                                "4d2d9c2f57f6ae0987aafd140aace1e3",
                                "MSW05_Order, MSW05_Family, MSW05_Genus, MSW05_Species")
                              ])
