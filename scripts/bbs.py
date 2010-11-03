"""Database Toolkit for Breeding Bird Survey
 
"""

import os
import urllib
import zipfile
from decimal import Decimal
from dbtk.lib.templates import DbTk
from dbtk.lib.models import Table, Cleanup, no_cleanup

VERSION = '0.3.2'


class main(DbTk):
    def __init__(self, **kwargs):
        DbTk.__init__(self, kwargs)
        self.name = "USGS North American Breeding Bird Survey"
        self.shortname = "BBS"
        self.ref = "http://www.pwrc.usgs.gov/BBS/"
        self.urls = {"counts": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/States/",
                     "routes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/CRoutes.exe",
                     "weather": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/CWeather.exe",
                     "region_codes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/RegionCodes.txt",
                     "species": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/SpeciesList.txt"}
    def download(self, engine=None):
        try:
            DbTk.download(self, engine)
            
            engine = self.engine
            
            # Routes table
            if not os.path.isfile(engine.format_filename("routes_new.csv")):
                engine.download_files_from_archive(self.urls["routes"],
                                                   ["routes.csv"])
                read = open(engine.format_filename("routes.csv"), "rb")
                write = open(engine.format_filename("routes_new.csv"), "wb")
                print "Cleaning routes data..."
                write.write(read.readline())
                for line in read:
                    values = line.split(',')
                    v = Decimal(values[5])
                    if  v > 0:
                        values[5] = str(v * Decimal("-1"))
                    write.write(','.join(str(value) for value in values))
                write.close()
                read.close()
                
            engine.auto_create_table("routes", filename="routes_new.csv",
                                     cleanup=Cleanup())
                
            engine.insert_data_from_file(engine.format_filename("routes_new.csv"))

            
            # Weather table                
            if not os.path.isfile(engine.format_filename("weather_new.csv")):
                engine.download_files_from_archive(self.urls["weather"], 
                                                   ["weather.csv"])            
                read = open(engine.format_filename("weather.csv"), "rb")
                write = open(engine.format_filename("weather_new.csv"), "wb")
                print "Cleaning weather data..."            
                for line in read:
                    values = line.split(',')
                    newvalues = []
                    for value in values:
                        
                        if ':' in value:
                            newvalues.append(value.replace(':', ''))
                        elif value == "N":
                            newvalues.append(None)
                        else:
                            newvalues.append(value)
                    write.write(','.join(str(value) for value in newvalues))
                write.close()
                read.close()
            
            engine.auto_create_table("weather", filename="weather_new.csv",
                                     pk="RouteDataId", cleanup=Cleanup())            
            engine.insert_data_from_file(engine.format_filename("weather_new.csv"))
            
            
            # Species table
            table = Table()
            table.tablename = "species"
            table.pk = False
            table.header_rows = 11
            
            table.columns=[("countrynum"            ,   ("int",)        ),
                           ("regioncode"            ,   ("int",)        ),
                           ("regionname"            ,   ("char",30)     )]
            table.fixedwidth = [11, 11, 30]
            
            engine.table = table
            engine.create_table()
                                    
            engine.insert_data_from_url(self.urls["species"])
            
            
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
            engine.create_table()
                                    
            engine.insert_data_from_url(self.urls["region_codes"])
                        
            
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
                        
                    print "Downloading and decompressing data from " + state + "..."
                    engine.insert_data_from_archive(self.urls["counts"] + "C" + shortstate + ".exe", 
                                                    ["C" + shortstate + ".csv"])
                            
                except:
                    print "There was an error in " + state + "."
            
            print 'Done!'
        except zipfile.BadZipfile:            
            print "There was an unexpected error in the Breeding Bird Survey archives."
            raise    
        
        return engine
