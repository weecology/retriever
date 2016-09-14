#retriever
"""Data Retriever script for the eBird Observation Dataset"""

from retriever.lib.templates import Script
from retriever.lib.models import Table


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "eBird Observation Dataset"
        self.shortname = "eBirdOD"
        self.ref = "http://ebird.org/content/ebird/news/gbif/"
        self.urls = {"main": "https://dataone.ornith.cornell.edu/metacat/d1/mn/v1/object/CLOEODDATA.05192014.1"}
        self.retriever_minimum_version = '2.0.0-dev'
        self.script_version = '1.0'
        self.description = "A collection of observations from birders through portals managed and maintained by local partner conservation organizations"

    def download(self, engine=None, debug=False):
        data_file_name = "eBird_Observation_Dataset_2013.csv"
        Script.download(self, engine, debug)
        self.engine.download_files_from_archive(self.urls["main"],
                                                [data_file_name],
                                                filetype='gz')
        table = (Table("main", delimiter=","))
        table.columns=[("BASISOFRECORD",("char", )),
                       ("INSTITUTIONCODE",("char", )),
                       ("COLLECTIONCODE",("char", )),
                       ("CATALOGNUMBER",("char", )),
                       ("OCCURRENCEID",("char", )),
                       ("RECORDEDBY",("char", )),
                       ("YEAR",("int", )),
                       ("MONTH",("int", )),
                       ("DAY",("int", )),
                       ("COUNTRY",("char", )),
                       ("STATEPROVINCE",("char", )),
                       ("COUNTY",("char", )),
                       ("DECIMALLATITUDE",("double", )),
                       ("DECIMALLONGITUDE",("double", )),
                       ("LOCALITY",("char", )),
                       ("KINGDOM",("char", )),
                       ("PHYLUM",("char", )),
                       ("CLASS",("char", )),
                       ("SPORDER",("char", )),
                       ("FAMILY",("char", )),
                       ("GENUS",("char", )),
                       ("SPECIFICEPITHET",("char", )),
                       ("SCIENTIFICNAME",("char", )),
                       ("VERNACULARNAME",("char", )),
                       ("INDIVIDUALCOUNT",("int", ))]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(data_file_name))
        return engine

SCRIPT = main()
