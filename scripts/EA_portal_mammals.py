"""Database Toolkit for the Portal Project mammals

Dataset published by Ernest et al. 2009 in Ecological Archives.

"""

#TO DO - confirm column reversal with authors and correct

from dbtk.lib.templates import DbTk
from dbtk.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.3.2'


class main(DbTk):
    def __init__(self, **kwargs):
        DbTk.__init__(self, kwargs)
        self.name = "Portal Project Mammals (Ecological Archives 2002)"
        self.shortname = "PortalMammals"
        self.ref = "http://esapubs.org/archive/ecol/E090/118/"
        self.urls = [("main", "http://esapubs.org/archive/ecol/E090/118/Portal_rodent_19772002.csv"),
                     ("species", "http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt"),
                     ("plots", "http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt")]
    def download(self, engine=None):
        DbTk.download(self, engine)
        
        # Plots table
        table = Table()
        table.tablename = self.urls[2][0]
        table.hasindex = True
        table.delimiter = ","
        table.header_rows = 0
        table.columns=[("PlotID"                ,   ("pk-auto",)    ),
                       ("PlotTypeAlphaCode"     ,   ("char", 2)     ),
                       ("PlotTypeNumCode"       ,   ("int",)        ),
                       ("PlotTypeDescript"      ,   ("char", 30)    )]
        self.engine.table = table
        self.engine.create_table()
        
        self.engine.insert_data_from_url(self.urls[2][1])
        
        # Species table        
        self.engine.auto_create_table(self.urls[1][0], self.urls[1][1], 
                                      cleanup=Cleanup())
        self.engine.insert_data_from_url(self.urls[1][1])
        
        # Main table
        self.engine.auto_create_table(self.urls[0][0], url=self.urls[0][1], 
                                 cleanup=Cleanup(correct_invalid_value, 
                                                 {"nulls":('', 0, '0')} ),
                                 pk="ID")
        self.engine.insert_data_from_url(self.urls[0][1])
        
        return self.engine
