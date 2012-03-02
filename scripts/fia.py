#retriever
"""Retriever script for Forest Inventory and Analysis
 
"""

import os
import urllib
import zipfile
from decimal import Decimal
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, no_cleanup

VERSION = '0.5'


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Forest Inventory and Analysis"
        self.shortname = "FIA"
        self.ref = "http://fia.fs.fed.us/"
        self.urls = {"main": "http://apps.fs.fed.us/fiadb-downloads/"}
        self.tags = ["Taxon > Plants", "Spatial Scale > Continental",
                     "Data Type > Observational"]
        self.description = """WARNING: This dataset requires downloading many large files and will probably take several hours to finish installing."""
        self.addendum = """This dataset requires downloading many large files - please be patient."""

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        
        engine = self.engine
        
        # State abbreviations with the year annual inventory began for that state
        stateslist = [('AL', 2001), ('AK', 2004), ('AZ', 2001), ('AR', 2000), 
                      ('CA', 2001), ('CO', 2002), ('CT', 2003), ('DE', 2004), 
                      ('FL', 2003), ('GA', 1998), ('ID', 2004), ('IL', 2001), 
                      ('IN', 1999), ('IA', 1999), ('KS', 2001), ('KY', 1999), 
                      ('LA', 2001), ('ME', 1999), ('MD', 2004), ('MA', 2003), 
                      ('MI', 2000), ('MN', 1999), ('MO', 1999), ('MT', 2003), 
                      ('NE', 2001), ('NV', 2004), ('NH', 2002), ('NJ', 2004), 
                      ('NY', 2002), ('NC', 2003), ('ND', 2001), ('OH', 2001), 
                      ('OK', 2008), ('OR', 2001), ('PA', 2000), ('RI', 2003), 
                      ('SC', 1999), ('SD', 2001), ('TN', 2000), ('TX', 2001), 
                      ('UT', 2000), ('VT', 2003), ('VA', 1998), ('WA', 2002), 
                      ('WV', 2004), ('WI', 2000), ('PR', 2001)]
        
        tablelist = ["SURVEY", "PLOT", "COND", "SUBPLOT", "SUBP_COND", "TREE", "SEEDLING"]
        
        for table in tablelist:
            for state in stateslist:
                engine.download_files_from_archive(self.urls["main"] + state[0] + "_" + table + ".ZIP", 
                                                   [state[0] + "_" + table + ".CSV"])
        
        for table in tablelist:
            print "Scanning data for table %s..." % table
            prep_file_name = "%s.csv" % table
            prep_file = open(engine.format_filename(prep_file_name), "wb")
            this_file = open(engine.format_filename(stateslist[0][0] + "_" + table + ".CSV"), "rb")
            prep_file.write(this_file.readline())
            this_file.close()
            for state in stateslist:
                this_file = open(engine.format_filename(state[0] + "_" + table + ".CSV"), "rb")
                this_file.readline()
                for line in this_file:
                    prep_file.write(line.replace('"', ''))
            prep_file.close()
            engine.auto_create_table(Table(table), filename=prep_file_name)

            engine.insert_data_from_file(engine.format_filename(prep_file_name))
            
            try:
                os.remove(engine.format_filename(prep_file_name))
            except:
                pass
        
        return engine
        
        
SCRIPT = main()
