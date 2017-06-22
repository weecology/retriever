# -*- coding: latin-1 -*-
#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.defaults import VERSION
from pkg_resources import parse_version

class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title="Food web including metazoan parasites for a brackish shallow water ecosystem in Germany and Denmark"
        self.citation="C. Dieter Zander, Neri Josten, Kim C. Detloff, Robert Poulin, John P. McLaughlin, and David W. Thieltges. 2011. Food web including metazoan parasites for a brackish shallow water ecosystem in Germany and Denmark. Ecology 92:2007."
        self.name="flensburg-food-web"
        self.shortname="flensburg-food-web"
        self.ref="https://figshare.com/articles/Full_Archive/3552066"
        self.description="This data is of a food web for the Flensburg Fjord, a brackish shallow water inlet on the Baltic Sea, between Germany and Denmark."
        self.keywords = []
        self.retriever_minimum_version='2.0.dev'
        self.version='1.0.1'
        self.urls={"zip": "https://ndownloader.figshare.com/files/5620326"}
        self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=[''])

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['', 'unknown'])

    def download(self, engine=None):
        Script.download(self, engine)
        engine = self.engine
        file_names = [ ('Flensburg_Data_Links.csv','links'),
                        ('Flensburg_Data_Nodes.csv','nodes')
                     ]

        engine.download_files_from_archive(self.urls["zip"], [i[0] for i in file_names], filetype="zip", archivename="ECOL_92_174")
        
        for(filename,tablename) in file_names:
            data_path = self.engine.format_filename(filename)
            self.engine.auto_create_table(Table(str(tablename), cleanup=self.cleanup_func_table),filename=filename)
            self.engine.insert_data_from_file(data_path)

SCRIPT = main()
