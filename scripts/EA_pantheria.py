"""Database Toolkit for Pantheria dataset

"""

from dbtk.lib.templates import BasicTextTemplate
from dbtk.lib.tools import DbTkTest

VERSION = '0.4.1'

SCRIPT = BasicTextTemplate(
                           name="Pantheria (Ecological Archives 2008)",
                           description="Kate E. Jones, Jon Bielby, Marcel Cardillo, Susanne A. Fritz, Justin O'Dell, C. David L. Orme, Kamran Safi, Wes Sechrest, Elizabeth H. Boakes, Chris Carbone, Christina Connolly, Michael J. Cutts, Janine K. Foster, Richard Grenyer, Michael Habib, Christopher A. Plaster, Samantha A. Price, Elizabeth A. Rigby, Janna Rist, Amber Teacher, Olaf R. P. Bininda-Emonds, John L. Gittleman, Georgina M. Mace, and Andy Purvis. 2009. PanTHERIA: a species-level database of life history, ecology, and geography of extant and recently extinct mammals. Ecology 90:2648.",
                           shortname="Pantheria",
                           urls={"species": "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"}
                           )


class EAPantheriaTest(DbTkTest):
    def test_EAPantheria(self):        
        DbTkTest.default_test(self,
                              main(),
                              [("species",
                                "4d2d9c2f57f6ae0987aafd140aace1e3",
                                "MSW05_Order, MSW05_Family, MSW05_Genus, MSW05_Species")
                              ])
