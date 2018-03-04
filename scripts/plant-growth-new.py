from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "plant growth_new"
        self.shortname = "DataS1"
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1569/full"
        self.urls = {"plantgrowth": "http://onlinelibrary.wiley.com/store/10.1002/ecy.1569/asset/supinfo/ecy1569-sup-0001-DataS1.zip?v=1&s=219c74fa85bfe6738e649bedd844f40428351802"}
        self.citation = "Engemann, K., Sandel, B., Boyle, B. L., Enquist, B. J., Jorgensen, P. M., Kattge, J., McGill, B. J., Morueta-Holme, N., Peet, R. K., Spencer, N. J., Violle, C., Wiser, S. K. and Svenning, J. .-C. (2016), A plant growth form dataset for the New World. Ecology. Accepted Author Manuscript. doi:10.1002/ecy.1569"
        self.tags = ['Taxon > Plants', 'Data Type > Observational']
        self.retriever_minimum_version = 2.0
        self.script_version = 1.0
        self.description = "This dataset provides growth form classifications for 67,413 vascular plant species from North, Central, and South America."

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # files are in another DataS1 folder
        # important files considered (GrowthForm_Final.txt, GrowthForm_Initial.txt, Growthform_Scheme.txt)

        file_name = ["DataS1/Growthform_Scheme.txt"]
        engine.download_files_from_archive(self.urls["plantgrowth"], file_name)


        # creating scheme from Growthform_Scheme.txt
        engine.auto_create_table(Table("GrowthFormscheme", cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),
                                 filename="Growthform_Scheme.txt")
        engine.insert_data_from_file(engine.format_filename("Growthform_Scheme.txt"))


SCRIPT = main()