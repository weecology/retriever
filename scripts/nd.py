# -*- coding: utf-8  -*-
#retriever
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "nd"
        self.ref = "http://index.gain.org/"
        self.urls = {"nd":"https://gain-new.crc.nd.edu/assets/gain/files/resources-2017-03-10-14h04.zip"}
        self.citation = "na"
        self.retriever_minimum_version = 2.0
        self.script_version = 1.0
        self.description = "The ND-GAIN Country Index summarizes a country's vulnerability to climate change and other global challenges in combination with its readiness to improve resilience. It aims to help governments, businesses and communities better prioritize investments for a more efficient response to the immediate global challenges ahead."

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # files are in resources folder which in turn is in gain folder
        # important files considered (gain.csv,gain_delta.csv)

        file_names = ["resources/gain/gain.csv", "resources/gain/gain_delta.csv"]

        engine.download_files_from_archive(self.urls["nd"], file_names)

        # creating scheme from gain.csv
        engine.auto_create_table(Table("gain", cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),
                                 filename="gain.csv")
        
        engine.insert_data_from_file(engine.format_filename("gain.csv"))

        # creating scheme from gain_delta.csv
        engine.auto_create_table(Table("gain_delta", cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),
                                 filename="gain_delta.csv")
        engine.insert_data_from_file(engine.format_filename("gain_delta.csv"))


SCRIPT = main()
