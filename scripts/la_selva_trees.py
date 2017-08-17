#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value
try:
    from retriever import VERSION
except ImportError:
    from retriever.lib.defaults import VERSION
from pkg_resources import parse_version


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=[-999])
        self.title="Tree growth, mortality, physical condition - Clark, 2006"
        self.keywords=['plants', 'time-series']
        self.urls={'trees': 'https://ndownloader.figshare.com/files/5597693'}
        self.name="la-selva-trees"
        self.description="The data set helps to examine the post-establishment ecology of 10 species of tropical wet forest trees selected to span a range of predicted life history patterns at the La Selva Biological Station in Costa Rica."
        self.ref="https://doi.org/10.6084/m9.figshare.c.3299324.v1"
        self.retriever_minimum_version= "2.0.dev"
        self.version='1.4.1'
        self.citation="David B. Clark and Deborah A. Clark. 2006. Tree growth, mortality, physical condition, and microsite in an old-growth lowland tropical rain forest. Ecology 87:2132."

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=[-999])
        self.tables={'trees': Table('trees', cleanup=self.cleanup_func_table)}

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        self.engine.download_file(self.urls["trees"], "LS_trees_1983_2000.txt")
        data_path = self.engine.format_filename("LS_trees_1983_2000.txt")
        self.engine.auto_create_table(self.tables["trees"], filename="LS_trees_1983_2000.txt")
        self.engine.insert_data_from_file(data_path)

SCRIPT = main()
