from dbtk.lib.templates import BasicTextTemplate
from dbtk.lib.tools import DbTkTest

VERSION = '0.4.2'

SCRIPT = BasicTextTemplate(
                           name="Avian Body Size (Ecological Archives 2007)",
                           description="Terje Lislevand, Jordi Figuerola, and Tamas Szekely. 2007. Avian body sizes in relation to fecundity, mating system, display behavior, and resource sharing. Ecology 88:1605.",
                           shortname="AvianBodySize",
                           urls={"species": "http://esapubs.org/archive/ecol/E088/096/avian_ssd_jan07.txt"}
                           )


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
