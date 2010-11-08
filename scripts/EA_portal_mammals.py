"""Database Toolkit for the Portal Project mammals

Dataset published by Ernest et al. 2009 in Ecological Archives.

"""

#TO DO - confirm column reversal with authors and correct

from dbtk.lib.templates import BasicTextTemplate
from dbtk.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.4'


class main(BasicTextTemplate):
    def __init__(self, **kwargs):
        BasicTextTemplate.__init__(self, **kwargs)
        self.name = "Portal Project Mammals (Ecological Archives 2002)"
        self.shortname = "PortalMammals"
        self.ref = "http://esapubs.org/archive/ecol/E090/118/"
        self.tables = {
                       "plots": Table("plots", delimiter=',', contains_pk=True,
                                      header_rows=0,
                                      columns=[("PlotID"            , ("pk-auto",) ),
                                               ("PlotTypeAlphaCode" , ("char", 2)  ),
                                               ("PlotTypeNumCode"   , ("int",)     ),
                                               ("PlotTypeDescript"  , ("char", 30) )]
                                      ),
                        "main": Table("main", cleanup=Cleanup(correct_invalid_value,
                                                              nulls=[])
                                      ),
                       }
        self.urls = {
                     "main": "http://esapubs.org/archive/ecol/E090/118/Portal_rodent_19772002.csv",
                     "species": "http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt",
                     "plots": "http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt"
                     }
