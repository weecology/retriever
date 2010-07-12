"""Database Toolkit for CRC Handbook of Avian Bird Masses companion CD

NOTE: This data is not publicly available. To download the data, you'll need
the CRC Avian Body Masses CD. Create a new directory at 
raw_data/AvianBodyMass and copy the contents of the CD there before running
this script.

"""

from dbtk_ui import *
import xlrd

class AvianBodyMass(DbTk):
    name = "CRC Avian Body Masses"
    shortname = "AvianBodyMass"
    public = False
    required_opts = []
    def download(self, engine=None):    
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "AvianBodyMass"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "mass"
        table.cleanup = Cleanup(no_cleanup, None)
        
        # Database column names and their data types. Use data type "skip" to skip the value, and
        # "combine" to merge a string value into the previous column
        table.columns=[("record_id"             ,   ("pk-auto",)    ),
                       ("scientific_name"       ,   ("char", 50)    ),
                       ("common_name"           ,   ("char", 50)    ),
                       ("sex"                   ,   ("char", 20)    ),
                       ("N"                     ,   ("char", 20)    ),
                       ("mean"                  ,   ("double",)     ),
                       ("std_dev"               ,   ("double",)     ),
                       ("min"                   ,   ("double",)     ),
                       ("max"                   ,   ("double",)     ),
                       ("season"                ,   ("char",2)      ),
                       ("location"              ,   ("char",50)     ),
                       ("source_num"            ,   ("char",50)     )]
        engine.table = table
        engine.create_table()
        
        class RawDataError(Exception):
            pass
        
        file_list = ["broadbills - tapaculos", "cotingas - NZ wrens",
                     "HA honeycreepers - icterids", "honeyeaters - corvids",
                     "jacanas - doves", "larks - accentors",
                     "muscicapids - babblers", "ostrich - waterfowl",
                     "parrotbills - sugarbirds", "parrots - nightjars",
                     "starlings - finches", "swifts - woodpeckers",
                     "thrushes - gnatcatchers", "vultures - bustards"]
        
        lines = []        
        
        for file in file_list:            
            filename = file + ".xls"
            full_filename = engine.format_filename(filename)
            
            # Make sure file exists
            if not os.path.isfile(full_filename):
                raise RawDataError("Missing raw data file: " + 
                                   full_filename)
            
            # Open excel file with xlrd
            book = xlrd.open_workbook(full_filename)
            sh = book.sheet_by_index(0)
            
            def empty(cell):
                if cell.ctype == 0:
                    return True
                if str(cell.value).strip() == "":
                    return True
                return False
            
            def cellvalue(cell):
                return str(cell.value).strip()

            print "Inserting data from " + filename + " . . ."
            rows = sh.nrows
            cols = 11
            lines = []
            for n in range(rows):
                row = sh.row(n)
                empty_cols = len([cell for cell in row[0:11] if empty(cell)])
                
                # Skip this row if all cells or all cells but one are empty
                # or if it's the legend row
                if (empty_cols >= cols - 1 or cellvalue(row[0]) == "Scientific Name"
                    or cellvalue(row[0])[0:7] == "Species"):
                    pass
                else:
                    values = []
                    # If the first two columns are empty, but the third isn't,
                    # use the first two columns from the previous row
                    if empty(row[0]) and empty(row[1]) and not empty(row[2]):
                        values.append(cellvalue(lastrow[0]))
                        values.append(cellvalue(lastrow[1]))
                    else:
                        if len(cellvalue(row[0]).split()) == 1:
                            # If the scientific name is missing genus, fill it
                            # in from the previous row
                            values.append(cellvalue(lastrow[0]).split()[0]
                                          + " " + cellvalue(row[0]))
                        else:
                            values.append(cellvalue(row[0]))
                        values.append(cellvalue(row[1]))
                        
                    if cellvalue(row[2]) == "M":
                        values.append("Male")
                    elif cellvalue(row[2]) == "F":
                        values.append("Female")
                    elif cellvalue(row[2]) == "B":
                        values.append("Both")
                    elif cellvalue(row[2]) == "U":
                        values.append("Unknown")
                    else:
                        values.append(cellvalue(row[2]))
                        
                    for i in range(3, cols):
                        values.append(cellvalue(row[i]))
                    
                    lines.append(',,'.join(values))
                    lastrow = row
            
            if lines:
                table.source = lines
                table.delimiter = ",,"
                engine.add_to_table()
                        
                    


if __name__ == "__main__":
    me = AvianBodyMass()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:
        me.download()
        final_cleanup()