"""Database Toolkit for Breeding Bird Survey 

See dbtk_tools.py for usage

"""

from dbtk_tools import *
import os
import urllib
import zipfile
import datacleanup

# Variables to get text file/create database
db = Database()
db.dbname = "BBS"
db.opts = get_opts()
db.engine = choose_engine(db)
db.cursor = get_cursor(db)
create_database(db)

table = Table()
table.tablename = "counts"
table.pk = "record_id"
table.delimiter = ","
table.cleanup = datacleanup.correct_invalid_value

table.columns=[("record_id"             ,   ("pk",)         ),
               ("countrynum"            ,   ("int",)        ),
               ("statenum"              ,   ("int",)        ),
               ("Route"                 ,   ("int",)        ),
               ("RPID"                  ,   ("int",)        ),
               ("Year"                  ,   ("int",)        ),
               ("Aou"                   ,   ("int",)        ),
               ("Count10"               ,   ("int",)        ),
               ("Count20"               ,   ("int",)        ),
               ("Count30"               ,   ("int",)        ),
               ("Count40"               ,   ("int",)        ),
               ("Count50"               ,   ("int",)        ),
               ("StopTotal"             ,   ("int",)        ),
               ("SpeciesTotal"          ,   ("int",)        )]

stateslist = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
              "Connecticut", "Delaware", "Florida", "Georgia", "Idaho",
              "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
              "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
              "Missouri", "Montana", "Nebraska", "Nevada", 
              ["New Hampshire", "NHampsh"], ["New Jersey", "NJersey"],
              ["New Mexico", "NMexico"], ["New York", "NYork"], 
              ["North Carolina", "NCaroli"], ["North Dakota", "NDakota"], "Ohio", 
              "Oklahoma", "Oregon", "Pennsylvania", ["Rhode Island", "RhodeIs"], 
              ["South Carolina", "SCaroli"], ["South Dakota", "SDakota"], "Tennessee", 
              "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
              "Wisconsin", "Wyoming", "Alberta", ["British Columbia", "BritCol"], "Manitoba",
              ["New Brunswick", "NBrunsw"], ["Northwest Territories", "NWTerri"],
              ["Newfoundland", "Newfound"], ["Nova Scotia", "NovaSco"], "Nunavut",
              "Ontario", ["Prince Edward Island", "PEI"], "Quebec", "Saskatchewan",
              "Yukon"]

state = ""
shortstate = ""
create_table(db, table)

for state in stateslist:
    try:
        if len(state) > 2:
            shortstate = state[0:7]
        else:        
            state, shortstate = state[0], state[1]
            
        print "Downloading and decompressing data from " + state + " . . ."
        url = "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/States/C" + shortstate + ".exe"
        archivename = url.split('/')[-1]
        webFile = urllib.urlopen(url)    
        localFile = open(archivename, 'w')
        localFile.write(webFile.read())
        localFile.close()
        webFile.close()    
        
        localZip = zipfile.ZipFile(archivename)    
        filename = "C" + shortstate + ".csv"
        if db.engine == "mysql":
            db.cursor.execute("USE " + db.dbname)
        
            localFile = localZip.extract(filename)    
            insert_data_from_file(db, table, filename)        
            localZip.close()
        
            os.remove(filename)            
        else:
            localFile = localZip.open(filename)
            table.source = localFile
            skip_rows(1, table.source)
        
            rows = add_to_table(db, table)
    
            localFile.close()
            localZip.close()  
        
            table.startindex = rows
        
        os.remove(archivename)  
                
    except:
        print "There was an error in " + state + "."
    