"""Database Toolkit for Breeding Bird Survey 

See dbtk_tools.py for usage

"""

from dbtk_tools import *
import os
import urllib
import zipfile
import datacleanup

class DbTk_BBS(DbTk):
    name = "USGS North American Breeding Bird Survey"
    url = "http://www.pwrc.usgs.gov/BBS/"
    def Download(self, engine=None):    
        # Variables to get text file/create database
        opts = get_opts()
        if not engine:        
            engine = choose_engine(opts)
        engine.opts = opts
        
        db = Database()
        db.dbname = "BBS"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        # Routes table
        table = Table()
        table.tablename = "routes"
        table.pk = "route_id"
        table.delimiter = ","
        table.cleanup = datacleanup.correct_invalid_value
        
        table.columns=[("route_id"              ,   ("pk",)         ),
                       ("countrynum"            ,   ("int",)        ),
                       ("statenum"              ,   ("int",)        ),
                       ("Route"                 ,   ("int",)        ),
                       ("Active"                ,   ("int",)        ),
                       ("Latitude"              ,   ("double",)     ),
                       ("Longitude"             ,   ("double",)     ),
                       ("Stratum"               ,   ("int",)        ),
                       ("BCR"                   ,   ("int",)        ),
                       ("LandTypeId"            ,   ("int",)        ),
                       ("RouteTypeId"           ,   ("int",)        ),
                       ("RouteTypeDetailId"     ,   ("int",)        )]
        engine.table = table
        engine.create_table()
        
        url = "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/CRoutes.exe"
        archivename = "CRoutes.exe"
        webFile = urllib.urlopen(url)    
        localFile = open("CRoutes.exe", 'w')
        localFile.write(webFile.read())
        localFile.close()
        webFile.close()    
        
        localZip = zipfile.ZipFile(archivename)    
        filename = "routes.csv"
                
        localFile = localZip.extract(filename)    
        engine.insert_data_from_file(filename)        
        localZip.close()
        
        os.remove(filename)                                        
        os.remove(archivename)  
        
        # Species table
        """table = Table()
        table.tablename = "species"
        table.pk = "species_id"
        table.hasindex = True
        table.cleanup = datacleanup.correct_invalid_value
        
        table.columns=[("seq"                   ,   ("skip",)       ),
                       ("species_id"            ,   ("pk",)         ),
                       ("enname"                ,   ("char",)       ),
                       ("frname"                ,   ("char",)       ),
                       ("spname"                ,   ("char",)       )]
        engine.table = table
        engine.create_table()
        
        url = "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/SpeciesList.txt"
        webFile = urllib.urlopen(url)    
        localFile = open("SpeciesList.txt", 'w')
        localFile.write(webFile.read())
        localFile.close()
        webFile.close()    
        
        filename = "SpeciesList.txt"            
        engine.insert_data_from_file(filename)        
        
        os.remove(filename)"""
        
        # Counts table
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
                      "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                      ["West Virginia", "W_Virgi"], "Wisconsin", "Wyoming", "Alberta", 
                      ["British Columbia", "BritCol"], "Manitoba", ["New Brunswick", "NBrunsw"], 
                      ["Northwest Territories", "NWTerri"], "Newfoundland", 
                      ["Nova Scotia", "NovaSco"], "Nunavut", "Ontario", 
                      ["Prince Edward Island", "PEI"], "Quebec", "Saskatchewan", "Yukon"]
        
        state = ""
        shortstate = ""
        
        engine.table = table
        engine.create_table()
        
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
                        
                localFile = localZip.extract(filename)    
                engine.insert_data_from_file(filename)        
                localZip.close()
                
                os.remove(filename)                                        
                os.remove(archivename)  
                        
            except:
                print "There was an error in " + state + "."
        
        print 'Done!'    
        
        
if __name__ == "__main__":
    me = DbTk_BBS()
    me.Download()        