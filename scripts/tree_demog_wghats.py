# -*- coding: UTF-8 -*-
#retriever

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Tree demography in Western Ghats, India - Pelissier et al. 2011"
        self.name = "tree-demog-wghats"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.2.0'
        self.ref = "https://figshare.com/collections/Tree_demography_in_an_undisturbed_" \
                   "Dipterocarp_permanent_sample_plot_at_Uppangala_Western_Ghats_of_India/3304026"
        self.urls = {"data": "https://ndownloader.figshare.com/files/5619033"}
        self.citation = "Raphael Pelissier, Jean-Pierre Pascal, N. Ayyappan, B. R. Ramesh, " \
                        "S. Aravajy, and S. R. Ramalingam. 2011. Twenty years tree demography " \
                        "in an undisturbed Dipterocarp permanent sample plot at Uppangala, " \
                        "Western Ghats of India. Ecology 92:1376."
        self.description = "A data set on demography of trees monitored over 20 years in " \
                           "Uppangala permanent sample plot (UPSP)."
        self.keywords = ["plants", "time-series", "observational"]

        if parse_version(VERSION) < parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['NA'])
        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value, missingValues=['NA'])

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        engine.download_files_from_archive(self.urls["data"], ["UPSP_Demo_data.txt", "UPSP_Species_list2.txt"],
                                           filetype="zip")

        # Create table sp_list(Species)
        engine.auto_create_table(Table('sp_list', cleanup=Cleanup(self.cleanup_func_table),
                                 filename="UPSP_Species_list2.txt")
        engine.insert_data_from_file(engine.format_filename("UPSP_Species_list2.txt"))

        # Create table ind_loc_girth
        engine.auto_create_table(Table('ind_loc_girth', cleanup=Cleanup(self.cleanup_func_table),
                                 filename="UPSP_Demo_data.txt")
        engine.insert_data_from_file(engine.format_filename("UPSP_Demo_data.txt"))


SCRIPT = main()
