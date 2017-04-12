#retriever

"""Retriever script for direct download of data data"""
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script
from retriever import VERSION
from pkg_resources import parse_version


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "BAAD: a Biomass And Allometry Database for woody plants"
        self.name = "biomass-allometry-db"
        self.ref = "https://doi.org/10.6084/m9.figshare.c.3307692.v1"
        self.urls = {"BAAD": "https://ndownloader.figshare.com/files/5634309"}
        self.citation = "Falster, D.S., Duursma, R.A., Ishihara, M.I., Barneche, D.R., FitzJohn, R.G., Varhammar, A., Aiba, M., Ando, M., Anten, N., Aspinwall, M.J. and Baltzer, J.L., 2015. BAAD: a Biomass And Allometry Database for woody plants."
        self.keywords = ['plants', 'observational']
        self.retriever_minimum_version = "2.0.dev"
        self.version = "1.3.0"
        self.description = "The data set is a Biomass and allometry database (BAAD) for woody plants containing 259634 measurements collected in 176 different studies from 21084 individuals across 678 species."
        
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

        # files are nested in another baad_data folder
        # important files considered (baad_data.csv,baad_methods.csv)
        # relevant files can be added in the same manner

        file_names = ["baad_data/baad_data.csv", "baad_data/baad_methods.csv"]
        engine.download_files_from_archive(self.urls["BAAD"], file_names)

        # creating data from baad_data.csv
        engine.auto_create_table(Table("data", cleanup=self.cleanup_func_table),
                                 filename="baad_data.csv")
        engine.insert_data_from_file(engine.format_filename("baad_data.csv"))

        # creating methods from baad_methods.csv
        engine.auto_create_table(Table("methods", cleanup=self.cleanup_func_table),
                                 filename="baad_methods.csv")
        engine.insert_data_from_file(engine.format_filename("baad_methods.csv"))

SCRIPT = main()
