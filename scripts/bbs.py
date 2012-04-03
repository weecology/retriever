#retriever
"""Retriever script for Breeding Bird Survey
 
"""

import os
import urllib
import zipfile
from decimal import Decimal
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, no_cleanup, correct_invalid_value

VERSION = '0.5'

class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "USGS North American Breeding Bird Survey"
        self.shortname = "BBS"
        self.ref = "http://www.pwrc.usgs.gov/BBS/"
        self.tags = ["Taxon > Birds", "Spatial Scale > Continental"]
        self.urls = {
                     "counts": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/States/",
                     "routes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/Routes.exe",
                     "weather": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/Weather.exe",
                     "region_codes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/RegionCodes.txt",
                     "species": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/SpeciesList.txt"
                     }
                     
    def download(self, engine=None, debug=False):
        try:
            Script.download(self, engine, debug)
            
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
                
            engine.auto_create_table(Table("routes", cleanup=Cleanup()), 
                                     filename="routes_new.csv")
                
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
            
            engine.auto_create_table(Table("weather", pk="RouteDataId", cleanup=Cleanup()), 
                                     filename="weather_new.csv")
            engine.insert_data_from_file(engine.format_filename("weather_new.csv"))
            
            
            # Species table
            table = Table("species", pk=False, delimiter=',')
            
            table.columns=[("species_id"            ,   ("pk-auto",)        ),
                           ("AOU"                   ,   ("int",)            ),
                           ("genus"                 ,   ("char",30)         ),
                           ("species"               ,   ("char",50)         ),
                           ("subspecies"            ,   ("char",30)         ),
                           ("id_to_species"         ,   ("bool",)           )]
            
            engine.table = table
            engine.create_table()
            
            engine.download_file(self.urls["species"], "SpeciesList.txt")
            species_list = open(engine.format_filename("SpeciesList.txt"), "rb")
            for n in range(8):
                species_list.readline()
            
            rows = []
            for line in species_list:
                if line and len(line) > 273:
                    latin_name = line[273:].split()
                    if len(latin_name) < 2:
                        # If there's no species given, add "None" value
                        latin_name.append("None")
                    subspecies = ' '.join(latin_name[2:]) if len(latin_name) > 2 else "None"                    
                    id_to_species = "1" if latin_name[1] != "None" else "0"
                    if latin_name[1] == "sp.":
                        latin_name[1] = "None"
                        id_to_species = "0"
                    if ("x" in latin_name or "/" in latin_name or "or" in latin_name):
                        # Hybrid species or only identified to a group of species
                        latin_name[1] = ' '.join(latin_name[1:])
                        subspecies = "None"
                        id_to_species = "0"
                    
                    rows.append(','.join([
                                          line.split()[1], 
                                          latin_name[0],
                                          latin_name[1],
                                          subspecies,
                                          id_to_species
                                          ]))
                    
            engine.table.source = rows
            engine.add_to_table()
            
            species_list.close()
            
            
            # Region_codes table
            table = Table("region_codes", pk=False, header_rows=11,
                          fixed_width=[11, 11, 30])
            def regioncodes_cleanup(value, engine):
                replace = {chr(225):"a", chr(233):"e", chr(237):"i", chr(243):"o"}
                newvalue = str(value)
                for key in replace.keys():
                    if key in newvalue:
                        newvalue = newvalue.replace(key, replace[key])
                return newvalue
            table.cleanup = Cleanup(regioncodes_cleanup)
            
            table.columns=[("countrynum"            ,   ("int",)        ),
                           ("regioncode"            ,   ("int",)        ),
                           ("regionname"            ,   ("char",30)     )]
            
            engine.table = table
            engine.create_table()
                                    
            engine.insert_data_from_url(self.urls["region_codes"])
                        
            
            # Counts table
            table = Table("counts", delimiter=',')
            
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
                    
                    print "Inserting data from " + state + "..."
                    try:
                        engine.table.cleanup = Cleanup()
                        engine.insert_data_from_archive(self.urls["counts"] + shortstate + ".exe", 
                                                        [shortstate + ".csv"])
                    except:               
                        print "Failed bulk insert on " + state + ", inserting manually."
                        engine.connection.rollback()
                        engine.table.cleanup = Cleanup(correct_invalid_value,
                                                       nulls=['*'])
                        engine.insert_data_from_archive(self.urls["counts"] + shortstate + ".exe", 
                                                        [shortstate + ".csv"])
                            
                except:
                    print "There was an error in " + state + "."
                    raise
            
        except zipfile.BadZipfile:            
            print "There was an unexpected error in the Breeding Bird Survey archives."
            raise    
        
        return engine
        
        
SCRIPT = main()
