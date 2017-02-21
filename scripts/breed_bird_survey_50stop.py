#retriever
"""Retriever script for Breeding Bird Survey 50 stop data

"""
from __future__ import print_function
from builtins import chr
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import range

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
        self.name = "USGS North American Breeding Bird Survey 50 stop"
        self.shortname = "breed-bird-survey-50stop"
        self.description = "A Cooperative effort between the U.S. Geological Survey's Patuxent Wildlife Research Center and Environment Canada's Canadian Wildlife Service to monitor the status and trends of North American bird populations."
        self.citation = "Pardieck, K.L., D.J. Ziolkowski Jr., M.-A.R. Hudson. 2015. North American Breeding Bird Survey Dataset 1966 - 2014, version 2014.0. U.S. Geological Survey, Patuxent Wildlife Research Center."
        self.ref = "http://www.pwrc.usgs.gov/BBS/"
        self.tags = ["birds", "continental-scale"]
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.1'
        self.urls = {
                     "counts": "ftp://ftpext.usgs.gov/pub/er/md/laurel/BBS/DataFiles/50-StopData/1997ToPresent_SurveyWide/",
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

            table.columns=[("species_id", ("pk-int",) ),
                           ("AOU", ("int",) ),
                           ("english_common_name", ("char",50) ),
                           ("french_common_name", ("char",50) ),
                           ("spanish_common_name", ("char",50) ),
                           ("sporder", ("char",30) ),
                           ("family", ("char",30) ),
                           ("genus", ("char",30) ),
                           ("species", ("char",50) ),
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
                engine.download_files_from_archive(self.urls["weather"], ["weather.csv"])
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
            table = Table("counts", pk=False, delimiter=',')
            table.columns=[("RouteDataID"           ,   ("int",)        ),
                           ("countrynum"            ,   ("int",)        ),
                           ("statenum"              ,   ("int",)        ),
                           ("Route"                 ,   ("int",)        ),
                           ("RPID"                  ,   ("int",)        ),
                           ("year"                  ,   ("int",)        ),
                           ("AOU"                   ,   ("int",)        ),
                           ("Stop1"                 ,   ("int",)        ),
                           ("Stop2"                 ,   ("int",)        ),
                           ("Stop3"                 ,   ("int",)        ),
                           ("Stop4"                 ,   ("int",)        ),
                           ("Stop5"                 ,   ("int",)        ),
                           ("Stop6"                 ,   ("int",)        ),
                           ("Stop7"                 ,   ("int",)        ),
                           ("Stop8"                 ,   ("int",)        ),
                           ("Stop9"                 ,   ("int",)        ),
                           ("Stop10"                ,   ("int",)        ),
                           ("Stop11"                ,   ("int",)        ),
                           ("Stop12"                ,   ("int",)        ),
                           ("Stop13"                ,   ("int",)        ),
                           ("Stop14"                ,   ("int",)        ),
                           ("Stop15"                ,   ("int",)        ),
                           ("Stop16"                ,   ("int",)        ),
                           ("Stop17"                ,   ("int",)        ),
                           ("Stop18"                ,   ("int",)        ),
                           ("Stop19"                ,   ("int",)        ),
                           ("Stop20"                ,   ("int",)        ),
                           ("Stop21"                ,   ("int",)        ),
                           ("Stop22"                ,   ("int",)        ),
                           ("Stop23"                ,   ("int",)        ),
                           ("Stop24"                ,   ("int",)        ),
                           ("Stop25"                ,   ("int",)        ),
                           ("Stop26"                ,   ("int",)        ),
                           ("Stop27"                ,   ("int",)        ),
                           ("Stop28"                ,   ("int",)        ),
                           ("Stop29"                ,   ("int",)        ),
                           ("Stop30"                ,   ("int",)        ),
                           ("Stop31"                ,   ("int",)        ),
                           ("Stop32"                ,   ("int",)        ),
                           ("Stop33"                ,   ("int",)        ),
                           ("Stop34"                ,   ("int",)        ),
                           ("Stop35"                ,   ("int",)        ),
                           ("Stop36"                ,   ("int",)        ),
                           ("Stop37"                ,   ("int",)        ),
                           ("Stop38"                ,   ("int",)        ),
                           ("Stop39"                ,   ("int",)        ),
                           ("Stop40"                ,   ("int",)        ),
                           ("Stop41"                ,   ("int",)        ),
                           ("Stop42"                ,   ("int",)        ),
                           ("Stop43"                ,   ("int",)        ),
                           ("Stop44"                ,   ("int",)        ),
                           ("Stop45"                ,   ("int",)        ),
                           ("Stop46"                ,   ("int",)        ),
                           ("Stop47"                ,   ("int",)        ),
                           ("Stop48"                ,   ("int",)        ),
                           ("Stop49"                ,   ("int",)        ),
                           ("Stop50"                ,   ("int",)        )]

            part = ""
            engine.table = table
            engine.create_table()

            for part in range(1,11):
                part = str(part)
                try:
                    print("Inserting data from part " + part + "...")
                    try:
                        engine.table.cleanup = Cleanup()
                        engine.insert_data_from_archive(self.urls["counts"] +
                                                        "Fifty" + part + ".zip",
                                                        ["fifty" + part + ".csv"])
                    except:
                        print("Failed bulk insert on " + part + ", inserting manually.")
                        engine.connection.rollback()
                        engine.table.cleanup = Cleanup(correct_invalid_value,
                                                       nulls=['*'])
                        engine.insert_data_from_archive(self.urls["counts"] +
                                                        "Fifty" + part + ".zip",
                                                        ["fifty" + part + ".csv"])

                except:
                    print("There was an error in part " + part + ".")
                    raise

        except zipfile.BadZipfile:
            print("There was an unexpected error in the Breeding Bird Survey archives.")
            raise

        return engine


SCRIPT = main()
