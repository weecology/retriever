"""Database Toolkit for CRC Handbook of Avian Bird Masses companion CD

NOTE: This data is not publicly available. To download the data, you'll need
the CRC Avian Body Masses CD. Create a new directory at 
raw_data/AvianBodyMass and copy the contents of the CD there before running
this script.

"""

from dbtk_ui import *

class CRCAvianBodyMass(DbTk):
    name = "CRC Avian Body Masses"
    shortname = "AvianBodyMass"
    public = False
    required_opts = []    
    def download(self, engine=None):    
        # Variables to get text file/create database
        excel = Excel()
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "AvianBodyMass"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "mass"
        table.delimiter = ",,"
        table.cleanup = Cleanup(no_cleanup, None)
        
        # Database column names and their data types. Use data type "skip" to skip the value, and
        # "combine" to merge a string value into the previous column
        table.columns=[("record_id"             ,   ("pk-auto",)    ),
                       ("family"                ,   ("char", 20)    ),
                       ("genus"                 ,   ("char", 20)    ),
                       ("species"               ,   ("char", 20)    ),
                       ("subspecies"            ,   ("char", 20)    ),
                       ("common_name"           ,   ("char", 50)    ),
                       ("sex"                   ,   ("char", 20)    ),
                       ("N"                     ,   ("double",)     ),
                       ("mean"                  ,   ("double",)     ),
                       ("std_dev"               ,   ("double",)     ),
                       ("min"                   ,   ("double",)     ),
                       ("max"                   ,   ("double",)     ),
                       ("season"                ,   ("char",2)      ),
                       ("location"              ,   ("char",50)     ),
                       ("source_num"            ,   ("char",50)     )]
        engine.table = table
        engine.create_table()
        
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
                raise DbtkError("Missing raw data file: " + 
                                   full_filename)
            
            # Open excel file with xlrd
            book = xlrd.open_workbook(full_filename)
            sh = book.sheet_by_index(0)
            
            def sci_name(value):
                """Returns genus/species/subspecies list from a scientific name"""
                values = value.split()
                list = []
                if len(values) >= 2:
                    [list.append(value) for value in values[0:2]]                    
                if len(values) == 3:
                    list.append(values[2])
                while len(list) < 3:
                    list.append('')
                return list 

            print "Inserting data from " + filename + " . . ."
            rows = sh.nrows
            cols = 11
            lines = []
            lastrow = None
            lastvalues = None
            family = ""
            for n in range(rows):
                row = sh.row(n)
                if len(row) == 0:
                    continue
                
                empty_cols = len([cell for cell in row[0:11] if excel.empty_cell(cell)])
                
                # Skip this row if all cells or all cells but one are empty
                # or if it's the legend row
                if ((empty_cols == cols)                             
                            or excel.cell_value(row[0]) == "Scientific Name"
                            or excel.cell_value(row[0])[0:7] == "Species"):
                    pass
                elif empty_cols == cols - 1:
                    if "Family" in excel.cell_value(row[0]):
                        family = excel.cell_value(row[0]).lstrip("Family ").title()
                        continue
                    else:
                        if not excel.empty_cell(row[0]):
                            lastvalues[3] = excel.cell_value(row[0])
                else:
                    # Values: 0=Family 1=Genus 2=Species 3=Subspecies 4=common name 5=sex
                    # 6=N 7=Mean 8=std_dev 9=min 10=max 11=season 12=location 13=source_num
                    values = []
                    values.append(family)
                    # If the first two columns are empty, but not all of them are,
                    # use the first two columns from the previous row
                    if excel.empty_cell(row[0]) and excel.empty_cell(row[1]):                        
                        [values.append(value) for value in sci_name(excel.cell_value(lastrow[0]))]
                        values.append(excel.cell_value(lastrow[1]))
                    else:
                        if len(excel.cell_value(row[0]).split()) == 1:
                            # If the scientific name is missing genus/species, fill it
                            # in from the previous row
                            values.append(lastvalues[1])
                            values.append(lastvalues[2])
                            values.append(lastvalues[3])
                            for i in range(0, 3):
                                if not values[3-i]:                                    
                                    values[3-i] = excel.cell_value(row[0])
                                    break
                            # Add new information to the previous scientific name
                            if lastvalues:
                                lastvalues[1:4] = values[1:4]                                
                        else:
                            [values.append(value) for value in sci_name(excel.cell_value(row[0]))]
                        values.append(excel.cell_value(row[1]))
                        
                    if excel.cell_value(row[2]) == "M":
                        values.append("Male")
                    elif excel.cell_value(row[2]) == "F":
                        values.append("Female")
                    elif excel.cell_value(row[2]) == "B":
                        values.append("Both")
                    elif excel.cell_value(row[2]) == "U":
                        values.append("Unknown")
                    else:
                        values.append(excel.cell_value(row[2]))
                        
                    # Enter remaining values from cells 
                    for i in range(3, cols):
                        values.append(excel.cell_value(row[i]))
                        
                    # If there isn't a common name or location, get it from 
                    # the previous row
                    if not values[4]:
                        values[4] = lastvalues[4]
                    if not values[12]:
                        if lastvalues:
                            if lastvalues[5]:
                                if lastvalues[5] == "Male" and values[5] == "Female":
                                    values[12] = lastvalues[12]
                    
                    # Insert the previous row into the database
                    if lastvalues:
                        lines.append(',,'.join(lastvalues))
                        
                    lastrow = row
                    lastvalues = values
            
            if lines:
                lines.append(',,'.join(lastvalues))
                table.source = lines                
                engine.add_to_table()
                        
        return engine


if __name__ == "__main__":
    me = CRCAvianBodyMass()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())