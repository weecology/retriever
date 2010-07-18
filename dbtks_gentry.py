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
        excel = Excel()
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "Gentry"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        url = "http://www.mobot.org/mobot/gentry/123/all_excel.zip"        
        engine.download_file(url, "all_excel.zip")
        local_zip = zipfile.ZipFile(engine.format_filename("all_excel.zip"))        
        filelist = local_zip.namelist()
        local_zip.close()
        engine.download_files_from_archive(url, filelist)
        
        filelist = [os.path.basename(filename) for filename in filelist]
        
        lines = []
        for filename in filelist:
            print "Extracting data from " + filename + " . . ."
            book = xlrd.open_workbook(engine.format_filename(filename))
            sh = book.sheet_by_index(0)
            rows = sh.nrows
            for i in range(1, rows):
                thisline = []
                row = sh.row(i)
                n = 0
                for cell in row:
                    n += 1
                    if n < 5 or n > 12:
                        if not excel.empty_cell(cell) or n == 13:
                            thisline.append(excel.cell_value(cell))
                    
                lines.append(thisline)
        
        print lines
        
        return engine
            
            
if __name__ == "__main__":
    me = Gentry()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())