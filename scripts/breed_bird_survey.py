#retriever
"""Retriever script for Breeding Bird Survey

"""
from __future__ import print_function
from builtins import chr
from builtins import str
from future import standard_library
standard_library.install_aliases()

import os
import urllib.request, urllib.parse, urllib.error
import zipfile
from decimal import Decimal
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, no_cleanup, correct_invalid_value
from retriever import HOME_DIR, open_fr, open_fw


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "USGS North American Breeding Bird Survey"
        self.shortname = "breed-bird-survey"
        self.description = "A Cooperative effort between the U.S. Geological Survey's Patuxent Wildlife Research Center and Environment Canada's Canadian Wildlife Service to monitor the status and trends of North American bird populations."
        self.citation = "Pardieck, K.L., D.J. Ziolkowski Jr., M.-A.R. Hudson. 2015. North American Breeding Bird Survey Dataset 1966 - 2014, version 2014.0. U.S. Geological Survey, Patuxent Wildlife Research Center"
        self.ref = "http://www.pwrc.usgs.gov/BBS/"
        self.tags = ["birds", "continental-scale"]
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.1'
        self.urls = {
                     "counts": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/States/",
                     "routes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/Routes.zip",
                     "weather": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/Weather.zip",
                     "region_codes": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/RegionCodes.txt",
                     "species": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/SpeciesList.txt"
                     }

    def download(self, engine=None, debug=False):
        try:
            Script.download(self, engine, debug)

            engine = self.engine

            # Species table
            table = Table("species", cleanup=Cleanup(), contains_pk=True,
                          header_rows=9)

            table.columns=[("species_id",               ("pk-int",)         ),
                           ("AOU",                      ("int",)            ),
                           ("english_common_name",      ("char",50)         ),
                           ("french_common_name",       ("char",50)         ),
                           ("spanish_common_name",      ("char",50)         ),
                           ("sporder",                  ("char",30)         ),
                           ("family",                   ("char",30)         ),
                           ("genus",                    ("char",30)         ),
                           ("species",                  ("char",50)         ),
                           ]
            table.fixed_width = [7,6,51,51,51,51,51,51,50]

            engine.table = table
            engine.create_table()
            engine.insert_data_from_url(self.urls["species"])

            # Routes table
            engine.download_files_from_archive(self.urls["routes"], ["routes.csv"])
            engine.auto_create_table(Table("routes", cleanup=Cleanup()),
                                     filename="routes.csv")
            engine.insert_data_from_file(engine.format_filename("routes.csv"))

            # Weather table
            if not os.path.isfile(engine.format_filename("weather_new.csv")):
                engine.download_files_from_archive(self.urls["weather"],
                                                   ["weather.csv"])
                read = open_fr(engine.format_filename("weather.csv"))
                write = open_fw(engine.format_filename("weather_new.csv"))
                print("Cleaning weather data...")
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

            engine.auto_create_table(Table("weather", pk="RouteDataId",
                                           cleanup=Cleanup(correct_invalid_value, nulls=['NULL'])),
                                     filename="weather_new.csv")
            engine.insert_data_from_file(engine.format_filename("weather_new.csv"))

            # Region_codes table
            table = Table("region_codes", pk=False, header_rows=11,
                          fixed_width=[11, 11, 30])

            def regioncodes_cleanup(value, engine):
                replace = {chr(225):"a", chr(233):"e", chr(237):"i", chr(243):"o"}
                newvalue = str(value)
                for key in list(replace.keys()):
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

                    print("Inserting data from " + state + "...")
                    try:
                        engine.table.cleanup = Cleanup()
                        engine.insert_data_from_archive(self.urls["counts"] + shortstate + ".zip",
                                                        [shortstate + ".csv"])
                    except:
                        print("Failed bulk insert on " + state + ", inserting manually.")
                        engine.connection.rollback()
                        engine.table.cleanup = Cleanup(correct_invalid_value,
                                                       nulls=['*'])
                        engine.insert_data_from_archive(self.urls["counts"] + shortstate + ".zip",
                                                        [shortstate + ".csv"])

                except:
                    print("There was an error in " + state + ".")
                    raise

        except zipfile.BadZipfile:
            print("There was an unexpected error in the Breeding Bird Survey archives.")
            raise

        return engine


SCRIPT = main()
