"""Database Toolkit for the Portal Project mammals

Dataset published by Ernest et al. 2009 in Ecological Archives.

"""

#TO DO - confirm column reversal with authors and correct

from dbtk_ui import *

class EAPortalMammals(DbTk):
    name = "Portal Project Mammals"
    shortname = "PortalMammals"
    url = "http://esapubs.org/archive/ecol/E090/118/Portal_rodent_19772002.csv"
    url_species = "http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt"
    def download(self, engine=None):
        DbTk.download(self, engine)
        
        # Plots table
        table = Table()
        table.tablename = "Plots"
        table.hasindex = True
        table.delimiter = ","
        table.header_rows = 0
        table.columns=[("PlotID"                ,   ("pk-auto",)    ),
                       ("PlotTypeAlphaCode"     ,   ("char", 2)     ),
                       ("PlotTypeNumCode"       ,   ("int",)        ),
                       ("PlotTypeDescript"      ,   ("char", 30)    )]
        self.engine.table = table
        self.engine.create_table()
        
        self.engine.insert_data_from_url("http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt")        
        
        # Species table        
        self.engine.auto_create_table(self.url_species, "species", 
                                      cleanup=Cleanup())
        self.engine.insert_data_from_url(self.url_species)
        
        # Main table
        self.engine.auto_create_table(self.url, "main", 
                                 cleanup=Cleanup(correct_invalid_value, 
                                                 {"nulls":('', 0, '0')} ),
                                 pk="ID")
        self.engine.insert_data_from_url(self.url)
        
        return self.engine
        

if __name__ == "__main__":
    me = EAPortalMammals()
    if len(sys.argv) == 1:
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())