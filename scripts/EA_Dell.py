#retriever
"""EcoData Retriever script DELL dataset"""
import unicodedata
import os
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Thermal dependence of biological traits 2013"
        self.shortname = "DELL"
        self.ref = "http://esapubs.org/archive/ecol/E094/108/"
        self.urls = {'TempTrait': 'http://esapubs.org/archive/ecol/E094/108/TempTrait_001.txt'}
        self.citation = "Anthony I. Dell, Samraat Pawar, and Van M. Savage. 2013. The thermal dependence of biological traits. Ecology 94:1205. http://dx.doi.org/10.1890/12-2060.1"
        self.tags = ['Taxon > Plants','Taxon > animals', 'Data Type > Compilation']
        self.description = "The data shows how diverse biological rates and times respond to temperature"
        self.tables = {'TempTrait': Table('TempTrait',cleanup=Cleanup(correct_invalid_value, nulls=['NA'])), }

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        self.engine.download_file(self.urls["TempTrait"], "original_TempTrait_001.txt")
        data_path = self.engine.format_filename("TempTrait_001.txt")
        old_data = open(self.engine.find_file("original_TempTrait_001.txt")).read().decode('UTF-16')
        clean_data = unicodedata.normalize('NFKD', old_data).encode('ASCII', 'ignore')
        new_data = open(data_path, 'wb')
        new_data.write(clean_data)
        new_data.close()
        self.engine.auto_create_table(self.tables["TempTrait"],
                                      filename="TempTrait_001.txt")
        self.engine.insert_data_from_file(data_path)

SCRIPT = main()
 