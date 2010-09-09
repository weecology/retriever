"""Database Toolkit for Alwyn H. Gentry Forest Transact Dataset

"""

import os
import zipfile
from dbtk_ui import *
from dbtk_excel import *

class Gentry(DbTk):
    name = "Alwyn H. Gentry Forest Transact Dataset"
    shortname = "Gentry"
    url = "http://www.mobot.org/mobot/gentry/123/all_Excel.zip"
    def download(self, engine=None):
        DbTk.download(self, engine)
                
        self.engine.download_file(self.url, "all_Excel.zip")
        local_zip = zipfile.ZipFile(self.engine.format_filename("all_Excel.zip"))        
        filelist = local_zip.namelist()
        local_zip.close()
        self.engine.download_files_from_archive(self.url, filelist)
        
        filelist = [os.path.basename(filename) for filename in filelist]
        
        lines = []
        tax = []
        for filename in filelist:
            print "Extracting data from " + filename + " . . ."
            book = xlrd.open_workbook(self.engine.format_filename(filename))
            sh = book.sheet_by_index(0)
            rows = sh.nrows
            for i in range(1, rows):
                thisline = []
                row = sh.row(i)
                n = 0
                cellcount = 0
                for cell in row:
                    if not Excel.empty_cell(cell):
                        cellcount += 1 
                if cellcount > 4 and not Excel.empty_cell(row[0]):
                    try:
                        a = int(Excel.cell_value(row[0]).split('.')[0])
                        for cell in row:
                            n += 1
                            if n < 5 or n > 12:
                                if not Excel.empty_cell(cell) or n == 13:
                                    thisline.append(Excel.cell_value(cell))
                        
                        newline = [str(value).title().replace("\\", "/") for value in thisline] 
                        lines.append(newline)
                        tax.append((newline[1], newline[2], newline[3]))
                    except:
                        pass                    
        
        unique_tax = []
        tax_dict = dict()
        tax_count = 0
        
        # Get all unique families/genera/species        
        for group in tax:
            if not (group in unique_tax):
                unique_tax.append(group)
                tax_count += 1
                tax_dict[group] = tax_count
                msg = "Generating taxonomic groups: " + str(tax_count)
                print msg + "\b" * len(msg)
        
        # Create species table
        table = Table()
        table.tablename = "species"
        table.columns=[("species_id"            ,   ("pk-auto",)    ),
                       ("family"                ,   ("char", 50)    ),
                       ("genus"                 ,   ("char", 50)    ),
                       ("species"               ,   ("char", 50)    )]

        table.source = ['::'.join([group[i] for i in range(3)]) 
                        for group in unique_tax]
        table.delimiter = '::'
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table()        
        
        # Create stems table
        table = Table()
        table.tablename = "stems"
        table.columns=[("stem_id"               ,   ("pk-auto",)    ),
                       ("line"                  ,   ("int",)        ),
                       ("species_id"            ,   ("int",)        ),
                       ("liana"                 ,   ("char", 10)    ),
                       ("stem"                  ,   ("double",)     )]
        table.hasindex = False
        stems = []
        for line in lines:
            species_info = [str(line[0]).split('.')[0], 
                            tax_dict[(line[1], line[2], line[3])],
                            line[4]
                            ]
            stem_count = len(line) - 5
            for i in range(stem_count):
                stem = species_info + [line[(i + 1) * -1]]
                stems.append([str(value) for value in stem])
            
        table.source = ['::'.join(stem) for stem in stems]
        table.delimiter = '::'
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table()
            
        return self.engine
            
            
if __name__ == "__main__":
    me = Gentry()
    if len(sys.argv) == 1:
        launch_wizard([me], ALL_ENGINES)
    else:
        final_cleanup(me.download())