#retriever
"""EcoData Retriever script DELL dataset"""
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Thermal dependence of biological traits, 2013",
        self.shortname = "DELL"
        self.ref = "http://esapubs.org/archive/ecol/E094/108/"
        self.urls = {'TempTrait': 'http://esapubs.org/archive/ecol/E094/108/TempTrait_001.txt'}
        self.citation = "Anthony I. Dell, Samraat Pawar, and Van M. Savage. 2013. The thermal dependence of biological traits. Ecology 94:1205. http://dx.doi.org/10.1890/12-2060.1"
        self.tags = ['Taxon > Plants','Taxon > animals', 'Data Type > Compilation']
        self.description = "The data shows how diverse biological rates and times respond to temperature"

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        for key in self.urls:
            self.engine.download_file(self.urls[key], self.urls[key].rpartition('/')[-1])
            new_file_path = self.engine.format_filename("new" + key)
            old_data = open(self.engine.find_file(self.urls[key].rpartition('/')[-1]), "rb")
            new_data = open(new_file_path, 'wb')
            data = old_data.read()
            # replace the null bytes in the file
            new_data.write(data.replace('\x00', ''))
            old_data.close()
            new_data.close()
            self.engine.auto_create_table(Table(key,
                                                cleanup=Cleanup(correct_invalid_value,
                                                                nulls=['NA'])), filename=str("new" + key))
            self.engine.insert_data_from_file(new_file_path)


SCRIPT = main()