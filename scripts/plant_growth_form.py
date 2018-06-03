#retriever
from pkg_resources import parse_version

from retriever.lib.models import Table
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
        self.title = "Plant Growth Form"
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1569/full"
        self.urls = {
            "plantgrowth": "https://esajournals.onlinelibrary.wiley.com"
                           "/action/downloadSupplement?doi=10.1002%2Fecy."
                           "1569&attachmentId=184128600"
        }
        self.citation = "Engemann, K., Sandel, B., Boyle, B. L., Enquist, " \
                        "B. J., Jorgensen, P. M., Kattge, J., McGill, " \
                        "B. J., Morueta-Holme, N., Peet, R. K., Spencer, " \
                        "N. J., Violle, C., Wiser, S. K. and Svenning, " \
                        "J. .-C. (2016), " \
                        "A plant growth form dataset for the New World. " \
                        "Ecology. Accepted Author Manuscript. " \
                        "doi:10.1002/ecy.1569"
        self.tags = ['Taxon > Plants', 'Data Type > Observational']
        self.retriever_minimum_version = "2.0.dev"
        self.version = '1.0.0'
        self.description = "Growth form classifications for 67,413 vascular " \
                           "plant species from North, Central, and " \
                           "South America."
        current_version = parse_version(VERSION).__str__()
        if current_version <= parse_version("2.0.dev"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        file_names = ["DataS1/Growthform_Scheme.txt",
                      "DataS1/GrowthForm_Initial.txt",
                      "DataS1/GrowthForm_Final.txt"]
        engine.download_files_from_archive(
            self.urls["plantgrowth"], file_names)

        current_version = parse_version(VERSION).__str__()
        older_versions = current_version < parse_version("2.1.dev").__str__()
        # DataS1/Growthform_Scheme.txt is 16 bit file,
        # Process to DataS1/Growthform_Sch.txt with 8 bit
        old_data = self.engine.find_file("DataS1/Growthform_Scheme.txt")
        old_reader = open_fr(old_data, encoding="UTF-16")
        new_data = self.engine.format_filename("DataS1/Growthform_Sch.txt")
        new_writter = open_fw(new_data)
        for line in old_reader:
            if to_str(line).strip():
                a = ["NA"] * 3
                string_line = to_str(line).strip()
                for (i, item) in enumerate(string_line.split("\t")):
                    a[i] = item
                    new_writter.write('\t'.join(a) + "\n")
        new_writter.close()
        old_reader.close()
        columns = [
            ("record_id", ("pk-auto",)),
            ("growthform_std", ("char",)),
            ("growthform_org", ("char",)),
            ("reference", ("char",))]

        filename = "DataS1/Growthform_Sch.txt"
        if older_versions:
            filename = "Growthform_Sch.txt"
        table_obj = Table('Growthform_Scheme', delimiter="\t", columns=columns)
        self.engine.auto_create_table(table_obj, filename=filename)
        self.engine.insert_data_from_file(engine.format_filename(filename))

        # process DataS1/GrowthForm_Initial.txt
        filename = "DataS1/GrowthForm_Initial.txt"
        if older_versions:
            filename = "GrowthForm_Initial.txt"
        table_obj = Table('GrowthForm_Initial', delimiter="\t")
        self.engine.auto_create_table(table_obj, filename=filename)
        self.engine.insert_data_from_file(engine.format_filename(filename))

        # process DataS1/GrowthForm_Final.txt
        filename = "DataS1/GrowthForm_Final.txt"
        if older_versions:
            filename = "GrowthForm_Final.txt"
        table_obj = Table('GrowthForm_Final', delimiter="\t")
        self.engine.auto_create_table(table_obj, filename=filename)
        self.engine.insert_data_from_file(engine.format_filename(filename))


SCRIPT = main()
