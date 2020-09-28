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
import zipfile
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from pkg_resources import parse_version

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import HOME_DIR, open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "USGS North American Breeding Bird Survey 50 stop"
        self.name = "breed-bird-survey-50stop"
        self.description = "A Cooperative effort between the U.S. Geological Survey's Patuxent Wildlife Research Center and Environment Canada's Canadian Wildlife Service to monitor the status and trends of North American bird populations."
        self.citation = "Pardieck, K.L., D.J. Ziolkowski Jr., M.-A.R. Hudson. 2015. North American Breeding Bird Survey Dataset 1966 - 2014, version 2014.0. U.S. Geological Survey, Patuxent Wildlife Research Center."
        self.ref = "http://www.pwrc.usgs.gov/BBS/"
        self.keywords = ["birds", "continental-scale"]
        self.retriever_minimum_version = '2.0.dev'
        self.version = '3.0.0'
        base_url = "https://www.sciencebase.gov/catalog/file/get/5ea04e9a82cefae35a129d65?f=__disk__"
        self.urls = {
            "counts": base_url + "40%2Fe4%2F92%2F40e4925dde30ffd926b1b4d540b485d8a9a320ba",
            "routes": base_url + "5d%2Fca%2F74%2F5dca74b1e3e1c21f18443e8f27c38bf0e2b2a234&allowOpen=true",
            "weather": base_url + "87%2Fb5%2F1d%2F87b51d999ae1ad18838aa60851e9bcff4498ac8d",
            "migrants": base_url + "bf%2Fe5%2Ff6%2Fbfe5f6834f85cc1e31edf67b5eb825b9abff5806",
            "Vehicledata": base_url + "a9%2F97%2F2b%2Fa9972b26aaeb48bf9425ed21681312b4cc063a7c",
            "species": base_url + "6f%2F16%2F1f%2F6f161fc7c7db1dcaf1259deb02d824700f280460&allowOpen=true",
        }
        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(
                correct_invalid_value, nulls=['NULL'])
            self.cleanup_func_clean = Cleanup(
                correct_invalid_value, nulls=['*'])
        else:
            self.encoding = "latin-1"
            self.cleanup_func_table = Cleanup(
                correct_invalid_value, missing_values=['NULL'])
            self.cleanup_func_clean = Cleanup(
                correct_invalid_value, missing_values=['*'])

    def download(self, engine=None, debug=False):
        try:
            Script.download(self, engine, debug)

            engine = self.engine

            # Species table
            table = Table("species", cleanup=Cleanup(), contains_pk=True, header_rows=11)
            table.columns = [
                ("species_id", ("pk-int",)),
                ("AOU", ("int",)),
                ("english_common_name", ("char", 50)),
                ("french_common_name", ("char", 50)),
                ("spanish_common_name", ("char", 50)),
                ("sporder", ("char", 30)),
                ("family", ("char", 30)),
                ("genus", ("char", 30)),
                ("species", ("char", 50)),
            ]
            table.fixed_width = [7, 6, 51, 51, 51, 51, 51, 51, 50]
            engine.table = table
            engine.create_table()
            engine.insert_data_from_url(self.urls["species"])

            # Routes table
            engine.download_files_from_archive(self.urls["routes"], ["routes.csv"],
                                               archive_name="routes.zip")
            engine.auto_create_table(Table("routes", cleanup=Cleanup()),
                                     filename="routes.csv")
            engine.insert_data_from_file(engine.format_filename("routes.csv"))

            # Weather table
            engine.download_files_from_archive(self.urls["weather"], ["weather.csv"],
                                               archive_name="weather.zip")
            engine.auto_create_table(Table("weather",
                                           pk="RouteDataId",
                                           cleanup=self.cleanup_func_table),
                                     filename="weather.csv")
            engine.insert_data_from_file(engine.format_filename("weather.csv"))

            # Migrations data
            engine.download_files_from_archive(self.urls["migrants"],
                                               archive_name="MigrantNonBreeder.zip")
            engine.extract_zip(
                engine.format_filename("MigrantNonBreeder/Migrants.zip"),
                engine.format_filename("Migrant"),
            )
            engine.extract_zip(
                engine.format_filename("MigrantNonBreeder/MigrantSummary.zip"),
                engine.format_filename("MigrantSummary"),
            )

            table = Table("migrants", cleanup=Cleanup())
            table.columns = [
                ('routedataid', ('int',)), ('countrynum', ('int',)),
                ('statenum', ('int',)), ('route', ('int',)), ('rpid', ('int',)),
                ('year', ('int',)), ('aou', ('int',)), ('stop1', ('int',)),
                ('stop2', ('int',)), ('stop3', ('int',)), ('stop4', ('int',)),
                ('stop5', ('int',)), ('stop6', ('int',)), ('stop7', ('int',)),
                ('stop8', ('int',)), ('stop9', ('int',)), ('stop10', ('int',)),
                ('stop11', ('int',)), ('stop12', ('int',)), ('stop13', ('int',)),
                ('stop14', ('int',)), ('stop15', ('int',)), ('stop16', ('int',)),
                ('stop17', ('int',)), ('stop18', ('int',)), ('stop19', ('int',)),
                ('stop20', ('int',)), ('stop21', ('int',)), ('stop22', ('int',)),
                ('stop23', ('int',)), ('stop24', ('int',)), ('stop25', ('int',)),
                ('stop26', ('int',)), ('stop27', ('int',)), ('stop28', ('int',)),
                ('stop29', ('int',)), ('stop30', ('int',)), ('stop31', ('int',)),
                ('stop32', ('int',)), ('stop33', ('int',)), ('stop34', ('int',)),
                ('stop35', ('int',)), ('stop36', ('int',)), ('stop37', ('int',)),
                ('stop38', ('int',)), ('stop39', ('int',)), ('stop40', ('int',)),
                ('stop41', ('int',)), ('stop42', ('int',)), ('stop43', ('int',)),
                ('stop44', ('int',)), ('stop45', ('int',)), ('stop46', ('int',)),
                ('stop47', ('int',)), ('stop48', ('int',)), ('stop49', ('int',)),
                ('stop50', ('int',))
            ]
            engine.table = table
            engine.create_table()
            engine.insert_data_from_file(engine.format_filename("Migrant/Migrants.csv"))

            table = Table("migrantsummary", cleanup=Cleanup())
            table.columns = [('routedataid', ('int',)), ('countrynum', ('int',)),
                             ('statenum', ('int',)), ('route', ('int',)),
                             ('rpid', ('int',)), ('year', ('int',)), ('aou', ('int',)),
                             ('count10', ('int',)), ('count20', ('int',)),
                             ('count30', ('int',)), ('count40', ('int',)),
                             ('count50', ('int',)), ('stoptotal', ('int',)),
                             ('speciestotal', ('int',))]
            engine.table = table
            engine.create_table()
            engine.insert_data_from_file(
                engine.format_filename("MigrantSummary/MigrantSummary.csv"))

            table = Table("vehicledata", cleanup=Cleanup())
            table.columns = [
                ('routedataid', ('int',)), ('countrynum', ('int',)),
                ('statenum', ('int',)), ('route', ('int',)), ('rpid', ('int',)),
                ('year', ('int',)), ('recordedcar', ('char',)), ('car1', ('int',)),
                ('car2', ('int',)), ('car3', ('int',)), ('car4', ('int',)),
                ('car5', ('int',)), ('car6', ('int',)), ('car7', ('int',)),
                ('car8', ('int',)), ('car9', ('int',)), ('car10', ('int',)),
                ('car11', ('int',)), ('car12', ('int',)), ('car13', ('int',)),
                ('car14', ('int',)), ('car15', ('int',)), ('car16', ('int',)),
                ('car17', ('int',)), ('car18', ('int',)), ('car19', ('int',)),
                ('car20', ('int',)), ('car21', ('int',)), ('car22', ('int',)),
                ('car23', ('int',)), ('car24', ('int',)), ('car25', ('int',)),
                ('car26', ('int',)), ('car27', ('int',)), ('car28', ('int',)),
                ('car29', ('int',)), ('car30', ('int',)), ('car31', ('int',)),
                ('car32', ('int',)), ('car33', ('int',)), ('car34', ('int',)),
                ('car35', ('int',)), ('car36', ('int',)), ('car37', ('int',)),
                ('car38', ('int',)), ('car39', ('int',)), ('car40', ('int',)),
                ('car41', ('int',)), ('car42', ('int',)), ('car43', ('int',)),
                ('car44', ('int',)), ('car45', ('int',)), ('car46', ('int',)),
                ('car47', ('int',)), ('car48', ('int',)), ('car49', ('int',)),
                ('car50', ('int',)), ('noise1', ('int',)), ('noise2', ('int',)),
                ('noise3', ('int',)), ('noise4', ('int',)), ('noise5', ('int',)),
                ('noise6', ('int',)), ('noise7', ('int',)), ('noise8', ('int',)),
                ('noise9', ('int',)), ('noise10', ('int',)), ('noise11', ('int',)),
                ('noise12', ('int',)), ('noise13', ('int',)), ('noise14', ('int',)),
                ('noise15', ('int',)), ('noise16', ('int',)), ('noise17', ('int',)),
                ('noise18', ('int',)), ('noise19', ('int',)), ('noise20', ('int',)),
                ('noise21', ('int',)), ('noise22', ('int',)), ('noise23', ('int',)),
                ('noise24', ('int',)), ('noise25', ('int',)), ('noise26', ('int',)),
                ('noise27', ('int',)), ('noise28', ('int',)), ('noise29', ('int',)),
                ('noise30', ('int',)), ('noise31', ('int',)), ('noise32', ('int',)),
                ('noise33', ('int',)), ('noise34', ('int',)), ('noise35', ('int',)),
                ('noise36', ('int',)), ('noise37', ('int',)), ('noise38', ('int',)),
                ('noise39', ('int',)), ('noise40', ('int',)), ('noise41', ('int',)),
                ('noise42', ('int',)), ('noise43', ('int',)), ('noise44', ('int',)),
                ('noise45', ('int',)), ('noise46', ('int',)), ('noise47', ('int',)),
                ('noise48', ('int',)), ('noise49', ('int',)), ('noise50', ('int',))
            ]
            engine.table = table
            engine.create_table()
            engine.download_files_from_archive(self.urls["Vehicledata"],
                                               archive_name="VehicleData.zip")
            engine.extract_zip(
                engine.format_filename("VehicleData/VehicleData.zip"),
                engine.format_filename("VehicleData"),
            )
            engine.insert_data_from_file(
                engine.format_filename("VehicleData/VehicleData.csv"))


            # Counts table
            table = Table("counts", pk=False, delimiter=',')
            engine.download_files_from_archive(self.urls["counts"],
                                               archive_name="50-StopData.zip")
            table.columns = [("RouteDataID", ("int",)),
                             ("countrynum", ("int",)),
                             ("statenum", ("int",)),
                             ("Route", ("int",)),
                             ("RPID", ("int",)),
                             ("year", ("int",)),
                             ("AOU", ("int",)),
                             ("Stop1", ("int",)),
                             ("Stop2", ("int",)),
                             ("Stop3", ("int",)),
                             ("Stop4", ("int",)),
                             ("Stop5", ("int",)),
                             ("Stop6", ("int",)),
                             ("Stop7", ("int",)),
                             ("Stop8", ("int",)),
                             ("Stop9", ("int",)),
                             ("Stop10", ("int",)),
                             ("Stop11", ("int",)),
                             ("Stop12", ("int",)),
                             ("Stop13", ("int",)),
                             ("Stop14", ("int",)),
                             ("Stop15", ("int",)),
                             ("Stop16", ("int",)),
                             ("Stop17", ("int",)),
                             ("Stop18", ("int",)),
                             ("Stop19", ("int",)),
                             ("Stop20", ("int",)),
                             ("Stop21", ("int",)),
                             ("Stop22", ("int",)),
                             ("Stop23", ("int",)),
                             ("Stop24", ("int",)),
                             ("Stop25", ("int",)),
                             ("Stop26", ("int",)),
                             ("Stop27", ("int",)),
                             ("Stop28", ("int",)),
                             ("Stop29", ("int",)),
                             ("Stop30", ("int",)),
                             ("Stop31", ("int",)),
                             ("Stop32", ("int",)),
                             ("Stop33", ("int",)),
                             ("Stop34", ("int",)),
                             ("Stop35", ("int",)),
                             ("Stop36", ("int",)),
                             ("Stop37", ("int",)),
                             ("Stop38", ("int",)),
                             ("Stop39", ("int",)),
                             ("Stop40", ("int",)),
                             ("Stop41", ("int",)),
                             ("Stop42", ("int",)),
                             ("Stop43", ("int",)),
                             ("Stop44", ("int",)),
                             ("Stop45", ("int",)),
                             ("Stop46", ("int",)),
                             ("Stop47", ("int",)),
                             ("Stop48", ("int",)),
                             ("Stop49", ("int",)),
                             ("Stop50", ("int",))]

            part = ""
            engine.table = table
            engine.create_table()

            for part in range(1, 11):
                part = str(part)
                try:
                    print("Inserting data from part " + part + "...")
                    try:
                        "1997ToPresent_SurveyWide"
                        engine.table.cleanup = Cleanup()
                        engine.extract_zip(
                            engine.format_filename("50-StopData/1997ToPresent_SurveyWide/Fifty" + part + ".zip"),
                            engine.format_filename("fifty" + part + ".csv"),
                        )
                    except:
                        print("fifty{}: Failed bulk insert on, inserting manually.".format(part))
                        engine.connection.rollback()
                        engine.table.cleanup = self.cleanup_func_clean
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
