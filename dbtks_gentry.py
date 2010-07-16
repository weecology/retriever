"""Database Toolkit for Alwyn H. Gentry Forest Transact Dataset

"""

from dbtk_ui import *
import os
import zipfile

class Gentry(DbTk):
    name = "Alwyn H. Gentry Forest Transact Dataset"
    shortname = "Gentry"
    url = ""
    required_opts = []
    def download(self, engine=None):    
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "Gentry"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        url = "http://www.mobot.org/mobot/gentry/text/all_text.zip"        
        engine.download_file(url, "all_text.zip")
        local_zip = zipfile.ZipFile(engine.format_filename("all_text.zip"))        
        filelist = local_zip.namelist()
        local_zip.close()
        engine.download_files_from_archive(url, filelist)
        print filelist
        
        
        
if __name__ == "__main__":
    me = Gentry()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:
        me.download()
        final_cleanup()