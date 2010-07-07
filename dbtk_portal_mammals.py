"""Database Toolkit for the Portal Project mammals

Dataset published by Ernest et al. 2009 in Ecological Archives.

"""

#TO DO - confirm column reversal with authors and correct

import datacleanup
from dbtk_tools import *
import dbtk_ui

class DbTk_Portal_Mammals(DbTk):
    name = "Portal Project Mammals"
    required_opts = []
    def download(self, engine=None):
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "PortalProjectMammals"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        #Plots table
        table = Table()
        table.tablename = "Plots"
        table.pk = "PlotID"
        table.hasindex = True
        table.delimiter = ","
        table.header_rows = 0
        table.columns=[("PlotID"                ,   ("pk-auto",)    ),
                       ("PlotTypeAlphaCode"     ,   ("char", 2)     ),
                       ("PlotTypeNumCode"       ,   ("int",)        ),
                       ("PlotTypeDescript"      ,   ("char", 30)    )]
        engine.table = table
        engine.table.source = engine.open_url("http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt")
        engine.create_table()
        engine.add_to_table()
        
        #Species table
        table = Table()
        table.tablename = "Species"
        table.pk = "SpeciesID"
        table.hasindex = True
        table.delimiter = ";"
        table.header_rows = 1
        table.columns=[("SpeciesCode"           ,   ("pk-char", 2)  ),
                       ("OldSpeciesIDs"         ,   ("char", 20)    ),
                       ("ScientificName"        ,   ("char", 50)    ),
                       ("Taxon"                 ,   ("char", 30)    ),
                       ("CommonName"            ,   ("char", 50)    ),
                       ("Unknown"               ,   ("int",)        ),
                       ("Rodent"                ,   ("int",)        ),
                       ("ShrublandAffiliated"   ,   ("int",)        )]
        engine.table = table
        engine.table.source = engine.open_url("http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt")
        engine.create_table()
        engine.add_to_table()
        
        # Main table
        table = Table()
        table.tablename = "main"
        table.pk = "ID"
        table.hasindex = True
        table.delimiter = ","
        table.cleanup = datacleanup.correct_invalid_value
        table.nullindicators = set(['', 0, '0'])
        table.columns=[("ID"                    ,   ("pk-auto",)    ),
                       ("month"                 ,   ("int",)        ),
                       ("day"                   ,   ("int",)        ),
                       ("year"                  ,   ("int",)        ),
                       ("period"                ,   ("double",)     ),
                       ("plot"                  ,   ("int",)        ),
                       ("note1"                 ,   ("int",)        ),
                       ("stake"                 ,   ("int",)        ),
                       ("species"               ,   ("char", 2)     ),
                       ("sex"                   ,   ("char", 2)     ),
                       ("age"                   ,   ("char", 2)     ),
                       ("reproduction"          ,   ("char", 2)     ),
                       ("testes"                ,   ("char", 2)     ),
                       ("vagina"                ,   ("char", 2)     ),
                       ("pregnant"              ,   ("char", 2)     ),
                       ("nipples"               ,   ("char", 2)     ),
                       ("lactation"             ,   ("char", 2)     ),
                       ("hindfoot"              ,   ("int",)        ),
                       ("weight"                ,   ("int",)        ),
                       ("tag"                   ,   ("char", 10)    ),
                       ("newtag"                ,   ("char", 2)     ),
                       ("secondtag"             ,   ("char", 8)     ),
                       ("newsecondtag"          ,   ("char", 2)     ),
                       ("prevrighttag"          ,   ("char", 8)     ),
                       ("prevlefttag"           ,   ("char", 8)     ),
                       ("nestdirection"         ,   ("char", 2)     ),
                       ("neststake"             ,   ("char", 2)     ),
                       ("note4"                 ,   ("char", 2)     ),
                       ("note5"                 ,   ("char", 1)     )]
        engine.table = table
        engine.table.source = engine.open_url("http://esapubs.org/archive/ecol/E090/118/Portal_rodent_19772002.csv")
        engine.create_table()
        engine.add_to_table()

if __name__ == "__main__":
    me = DbTk_Portal_Mammals()
    if len(sys.argv) == 1:
        dbtk_ui.launch_wizard([me], all_engines)
    else:
        me.download()