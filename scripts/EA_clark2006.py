#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value

class main(Script):
    def __init__(self):
        Script.__init__(self,
                        tables={'trees': Table('trees', cleanup=Cleanup(correct_invalid_value, nulls=[-999]))},
                        name="Tree growth, mortality, physical condition - Clark, 2006",
                        tags=['Taxon > Plants'],
                        urls={'trees': 'http://esapubs.org/archive/ecol/E087/132/LS_trees_1983_2000.txt'},
                        shortname="Clark2006",
                        description = "The data set helps to examine the post-establishment ecology of 10 species of tropical wet forest trees selected to span a range of predicted life history patterns at the La Selva Biological Station in Costa Rica.",
                        ref = "http://esapubs.org/archive/ecol/E087/132/",
                        citation="David B. Clark and Deborah A. Clark. 2006. Tree growth, mortality, physical condition, and microsite in an old-growth lowland tropical rain forest. Ecology 87:2132.")
    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.download_file(self.urls["trees"], "LS_trees_1983_2000_original.txt")
        data_path = self.engine.format_filename("LS_trees_1983_2000.txt")
        old_data = open(self.engine.find_file("LS_trees_1983_2000_original.txt"), 'rb')
        new_data = open(data_path, 'wb')

        last_line = None
        for line in old_data:
            if last_line: new_data.write(last_line)
            last_line = line

        new_data.close()
        old_data.close()

        self.engine.auto_create_table(self.tables["trees"],
                                      filename="LS_trees_1983_2000.txt")
        self.engine.insert_data_from_file(data_path)

SCRIPT = main()
