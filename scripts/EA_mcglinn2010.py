"""Daniel J. McGlinn, Peter G. Earls, and Michael W. Palmer. 2010. A 12-year 
study on the scaling of vascular plant composition in an Oklahoma tallgrass 
prairie. Ecology 91:1872.

"""

#TO DO - confirm column reversal with authors and correct

from dbtk.lib.templates import EcologicalArchives
from dbtk.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.3.1'


class main(EcologicalArchives):
    name = "Vascular plant composition - McGlinn, et al., 2010."
    shortname = "McGlinn2010"
    url = "http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv"
    tablename = "pres"
    
    def download(self, engine=None):
        EcologicalArchives.download(self, engine)
        
        other_urls = [("cover", "http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv"),
                      ("richness", "http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv"),
                      ("species", "http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv"),
                      ("environment", "http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv"),
                      ("climate", "http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv")]
        
        for url in other_urls:
            self.engine.auto_create_table(url[0], url=url[1],
                                          cleanup=Cleanup(correct_invalid_value, 
                                              {"nulls":self.nulls})
                                          )
            self.engine.insert_data_from_url(url[1])
            
        return self.engine
