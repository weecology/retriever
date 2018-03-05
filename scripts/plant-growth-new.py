#retriever
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from pkg_resources import parse_version
try:
    from retriever.lib.defaults import VERSION
    try:
      from retriever.lib.tools import open_fr, open_fw
    except ImportError:
      from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import open_fr, open_fw, VERSION

class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "plant_growth_new"
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1569/full"
        self.urls = {"plantgrowth": "http://onlinelibrary.wiley.com/store/10.1002/ecy.1569/asset/supinfo/ecy1569-sup-0001-DataS1.zip?v=1&s=219c74fa85bfe6738e649bedd844f40428351802"}
        self.citation = "Engemann, K., Sandel, B., Boyle, B. L., Enquist, B. J., Jorgensen, P. M., Kattge, J., McGill, B. J., Morueta-Holme, N., Peet, R. K., Spencer, N. J., Violle, C., Wiser, S. K. and Svenning, J. .-C. (2016), A plant growth form dataset for the New World. Ecology. Accepted Author Manuscript. doi:10.1002/ecy.1569"
        self.tags = ['Taxon > Plants', 'Data Type > Observational']
        self.retriever_minimum_version = 2.0
        self.script_version = 1.0
        self.description = "This dataset provides growth form classifications for 67,413 vascular plant species from North, Central, and South America."
        
        

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.download_file(self.urls["plantgrowth"], "Growthform_Scheme.txt")
        data_path = self.engine.format_filename("Growthform_Scheme.txt")
        old_data = open_fr(self.engine.find_file("Growthform_Scheme.txt"))
        new_data = open_fw(data_path)
        # original file's header contains an end of line charactor in the middle hence creating two lines
        # Read in the two lines and create the full header
        line1 = old_data.readline().strip()
        line2 = old_data.readline()
        newline = line1 + "\t" + line2
        new_data.write(newline)
        for line in old_data:
            new_data.write(line)
        new_data.close()
        old_data.close()

        self.engine.auto_create_table(self.tables["plantgrowth"],
                                      filename="Growthform_Scheme.txt")
        self.engine.insert_data_from_file(data_path)

SCRIPT = main()
