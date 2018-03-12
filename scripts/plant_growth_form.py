#retriever
from pkg_resources import parse_version

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw, to_str
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "plant-growth-form"
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1569/full"
        self.urls = {
            "plantgrowth": "http://onlinelibrary.wiley.com/store/10.1002/ecy.1569/asset/supinfo/ecy1569-sup-0001-DataS1.zip?v=1&s=219c74fa85bfe6738e649bedd844f40428351802"}
        self.citation = "Engemann, K., Sandel, B., Boyle, B. L., Enquist, B. J., Jorgensen, P. M., Kattge, J., McGill, B. J., Morueta-Holme, N., Peet, R. K., Spencer, N. J., Violle, C., Wiser, S. K. and Svenning, J. .-C. (2016), A plant growth form dataset for the New World. Ecology. Accepted Author Manuscript. doi:10.1002/ecy.1569"
        self.tags = ['Taxon > Plants', 'Data Type > Observational']
        self.retriever_minimum_version = "2.0.dev"
        self.version = '1.0.0'
        self.description = "This dataset provides growth form classifications for 67,413 vascular plant species from North, Central, and South America."

        if parse_version(VERSION) <= parse_version("2.0.dev"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        # Download and unzip all files
        file_names = ["DataS1/Growthform_Scheme.txt", "DataS1/GrowthForm_Initial.txt", "DataS1/GrowthForm_Final.txt"]
        engine.download_files_from_archive(self.urls["plantgrowth"], file_names,
                                           filetype="zip")

        # process DataS1/Growthform_Sch.txt
        data_path = self.engine.format_filename("DataS1/Growthform_Sch.txt")
        old_data = open_fr(self.engine.find_file("DataS1/Growthform_Scheme.txt"), encoding="UTF-16")
        new_data = open_fw(data_path)

        for line in old_data:
            if to_str(line).strip():
                a = ["NA"] * 3
                string_line = to_str(line).strip()
                for (i, item) in enumerate(string_line.split("\t")):
                    a[i] = item
                new_data.write('\t'.join(a) + "\n")
        new_data.close()
        old_data.close()

        columns = [
            ("record_id", ("pk-auto",)),
            ("growthform_std", ("char",)),
            ("growthform_org", ("char",)),
            ("reference", ("char",))]
        if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
            self.engine.auto_create_table(Table('Growthform_Scheme', delimiter="\t", columns=columns),
                                          filename="DataS1/Growthform_Sch.txt")
            self.engine.insert_data_from_file(engine.format_filename("DataS1/Growthform_Sch.txt"))
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['NA'])

        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=['NA'])
            self.engine.auto_create_table(Table('Growthform_Scheme', delimiter="\t", columns=columns),
                                          filename="Growthform_Sch.txt")
            self.engine.insert_data_from_file(engine.format_filename("Growthform_Sch.txt"))

            # process DataS1/GrowthForm_Initial.txt
            if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
                self.engine.auto_create_table(Table('GrowthForm_Initial', delimiter="\t"),
                                              filename="DataS1/GrowthForm_Initial.txt")
                self.engine.insert_data_from_file(engine.format_filename("DataS1/GrowthForm_Initial.txt"))
            else:
                self.engine.auto_create_table(Table('GrowthForm_Initial', delimiter="\t"),
                                              filename="GrowthForm_Initial.txt")
                self.engine.insert_data_from_file(engine.format_filename("GrowthForm_Initial.txt"))

            # process DataS1/GrowthForm_Final.txt
            if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
                self.engine.auto_create_table(Table('GrowthForm_Final', delimiter="\t"),
                                              filename="DataS1/GrowthForm_Final.txt")
                self.engine.insert_data_from_file(engine.format_filename("DataS1/GrowthForm_Final.txt"))
            else:
                self.engine.auto_create_table(Table('GrowthForm_Final', delimiter="\t"),
                                              filename="GrowthForm_Final.txt")
                self.engine.insert_data_from_file(engine.format_filename("GrowthForm_Final.txt"))


SCRIPT = main()
