"""Database Toolkit for Breeding Bird Survey 

See dbtk_tools.py for usage

"""

import os
import urllib
import zipfile
from dbtk_tools import *
import dbtk_ui
import platform

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
            table.pk = "route_id"
            table.delimiter = ","
            
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
            table.pk = "weather_id"
            table.delimiter = ","
            table.hasindex = True
            def weather_cleanup(value, engine):
                if value == "N":
                    return None
                elif ":" in value:
                    return value.translate(None, ":")             
                return value
            table.cleanup = weather_cleanup
                
            
            table.columns=[("routedataid"           ,   ("pk",)         ),
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
            
            os.remove(filename)                                        
            os.remove(archivename)
            
            """# Species table
            table = Table()
            table.tablename = "species"
            table.pk = "species_id"
            table.delimiter = ","
            table.hasindex = True
            table.cleanup = datacleanup.correct_invalid_value
            
            table.columns=[("routedataid"           ,   ("pk",)         ),
                           ("countrynum"            ,   ("int",)        ),
                           ("statenum"              ,   ("int",)        )]
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
            
            os.remove(filename)                                        
            os.remove(archivename)
            """
            
            # Counts table
            table = Table()
            table.tablename = "counts"
            table.pk = "record_id"
            table.delimiter = ","
            
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
                    localFile = open(archivename, 'wb')
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
        except zipfile.BadZipfile:            
            print "There was an unexpected error in the Breeding Bird Survey archives."
            raise    
        
        
if __name__ == "__main__":
    me = DbTk_BBS()
    if len(sys.argv) == 1:                
        dbtk_ui.launch_wizard([me], all_engines)
    else:
        me.download()
