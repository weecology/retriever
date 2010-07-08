"""Database Toolkit for Breeding Bird Survey 

See dbtk_tools.py for usage

"""

import os
import urllib
import zipfile
from dbtk_tools import *
import dbtk_ui

class DbTk_BBS(DbTk):
    name = "USGS North American Breeding Bird Survey"
    url = "http://www.pwrc.usgs.gov/BBS/"
    required_opts = []
    def download(self, engine=None):    
        try:
            # Variables to get text file/create database
            engine = self.checkengine(engine)
            
            db = Database()
            db.dbname = "BBS"
            engine.db = db
            engine.get_cursor()
            engine.create_db()
            
            # Routes table
            table = Table()
            table.tablename = "routes"
            table.delimiter = ","
            
            table.columns=[("route_id"              ,   ("pk-auto",)    ),
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
            archivename = url.split('/')[-1]
            webFile = urllib.urlopen(url)    
            localFile = open(archivename, 'wb')
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
            

            # Weather table
            table = Table()
            table.tablename = "weather"
            table.delimiter = ","
            table.hasindex = True
            def weather_cleanup(value, engine):
                if value == "N":
                    return None
                elif ":" in value:
                    return value.translate(None, ":")             
                return value
            table.cleanup = Cleanup(weather_cleanup, None)
                
            
            table.columns=[("routedataid"           ,   ("pk-auto",)    ),
                           ("countrynum"            ,   ("int",)        ),
                           ("statenum"              ,   ("int",)        ),
                           ("Route"                 ,   ("int",)        ),
                           ("RPID"                  ,   ("int",)        ),
                           ("Year"                  ,   ("int",)        ),
                           ("Month"                 ,   ("int",)        ),
                           ("Day"                   ,   ("int",)        ),
                           ("ObsN"                  ,   ("int",)        ),
                           ("TotalSpp"              ,   ("int",)        ),
                           ("StartTemp"             ,   ("int",)        ),
                           ("EndTemp"               ,   ("int",)        ),                           
                           ("TempScale"             ,   ("char",1)      ),
                           ("StartWind"             ,   ("int",)        ),
                           ("EndWind"               ,   ("int",)        ),
                           ("StartSky"              ,   ("int",)        ),
                           ("EndSky"                ,   ("int",)        ),
                           ("StartTime"             ,   ("int",)        ),
                           ("EndTime"               ,   ("int",)        ),
                           ("Assistant"             ,   ("int",)        ),
                           ("RunType"               ,   ("int",)        )]
            engine.table = table
            engine.create_table()
            
            url = "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/CWeather.exe"
            archivename = url.split('/')[-1]
            webFile = urllib.urlopen(url)    
            localFile = open(archivename, 'wb')
            localFile.write(webFile.read())
            localFile.close()
            webFile.close()    
            
            
            localZip = zipfile.ZipFile(archivename)    
            filename = "weather.csv"
                    
            localFile = localZip.extract(filename)    
            engine.insert_data_from_file(filename)        
            localZip.close()
            
            if not engine.keep_raw_data:
                os.remove(filename)                                        
            os.remove(archivename)

            
            # Region_codes table
            table = Table()
            table.tablename = "region_codes"
            table.pk = False
            table.header_rows = 11
            def regioncodes_cleanup(value, engine):
                replace = {chr(225):"a", chr(233):"e", chr(237):"i", chr(243):"o"}
                newvalue = str(value)
                for key in replace.keys():
                    if key in newvalue:
                        newvalue = newvalue.replace(key, replace[key])
                return newvalue
            table.cleanup = Cleanup(regioncodes_cleanup, None)
            
            table.columns=[("countrynum"            ,   ("int",)        ),
                           ("regioncode"            ,   ("int",)        ),
                           ("regionname"            ,   ("char",30)     )]
            table.fixedwidth = [11, 11, 30]
            
            engine.table = table                        
            engine.table.source = engine.open_url("ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/RegionCodes.txt")
            
            engine.create_table()        
            engine.add_to_table()            
                        
            
            # Counts table
            table = Table()
            table.tablename = "counts"
            table.delimiter = ","
            
            table.columns=[("record_id"             ,   ("pk-auto",)    ),
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
                    localFile = open(archivename, 'wb')
                    localFile.write(webFile.read())
                    localFile.close()
                    webFile.close()    
                    
                    localZip = zipfile.ZipFile(archivename)    
                    filename = "C" + shortstate + ".csv"
                            
                    localFile = localZip.extract(filename)    
                    engine.insert_data_from_file(filename)        
                    localZip.close()
                    
                    if not engine.keep_raw_data:
                        os.remove(filename)                                        
                    os.remove(archivename)  
                            
                except:
                    print "There was an error in " + state + "."
            
            print 'Done!'
        except zipfile.BadZipfile:            
            print "There was an unexpected error in the Breeding Bird Survey archives."
            raise    
        
        
if __name__ == "__main__":
    me = DbTk_BBS()
    if len(sys.argv) == 1:                
        dbtk_ui.launch_wizard([me], all_engines)
    else:
        me.download()
