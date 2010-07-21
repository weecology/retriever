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
                if not excel.empty_cell(row[0]):
                    for cell in row:
                        n += 1
                        if n < 5 or n > 12:
                            if not excel.empty_cell(cell) or n == 13:
                                thisline.append(excel.cell_value(cell))
                    
                    lines.append([str(value).title().replace("\\", "/") for value in thisline])
        
        # Get family/genus/species lists
        print "Generating species list . . ."
        tax = []
        for line in lines:
            tax.append([line[1], line[2], line[3]])
        
        families = dict()
        genera = dict()
        species = dict()
        familycount = 0
        genuscount = 0
        speciescount = 0
        for group in tax:
            family = group[0]
            if not (family in families.keys()):
                familycount += 1
                families[family] = familycount
            genus = (group[1], group[0])
            if not (genus in genera.keys()):
                genuscount += 1
                genera[genus] = genuscount
            thisspecies = (group[2], group[1], group[0])
            if not (thisspecies in species.keys()):
                speciescount += 1
                species[thisspecies] = speciescount
        
        # Create family table
        table = Table()
        table.tablename = "family"
        table.columns=[("family_id"             ,   ("pk-int",)     ),
                       ("family"                ,   ("char", 20)    )]
        table.hasindex = True
        table.source = [',,'.join([
                                   str(families[family]),
                                   family
                                   ]) for family in families.keys()]
        table.delimiter = ',,'
        engine.table = table
        engine.create_table()        
        engine.add_to_table()
        
        
        # Create genus table
        table = Table()
        table.tablename = "genus"
        table.columns=[("genus_id"              ,   ("pk-int",)     ),
                       ("genus"                 ,   ("char", 20)    ),
                       ("family_id"             ,   ("int", )       )]
        table.hasindex = True
        table.source = [',,'.join([
                                   str(genera[genus]),
                                   genus[0], 
                                   str(families[genus[1]])
                                   ]) for genus in genera.keys()]
        table.delimiter = ',,'
        engine.table = table
        engine.create_table()        
        engine.add_to_table()
        
        
        # Create species table
        table = Table()
        table.tablename = "species"
        table.columns=[("species_id"            ,   ("pk-int",)     ),
                       ("species"               ,   ("char", 20)    ),
                       ("genus_id"              ,   ("int", )       )]
        table.hasindex = True
        table.source = [',,'.join([
                                   str(species[thisspecies]),
                                   thisspecies[0], 
                                   str(genera[(thisspecies[1], thisspecies[2])])
                                   ]) for thisspecies in species.keys()]
        table.delimiter = ',,'
        engine.table = table
        engine.create_table()        
        engine.add_to_table()        
        
            
        
        return engine
            
            
if __name__ == "__main__":
    me = Gentry()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())