# -*- coding: UTF-8 -*-
#retriever

from pkg_resources import parse_version

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Pantheria (Jones et al. 2009)"
        self.name = "pantheria"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.3'
        self.ref = "https://figshare.com/collections/PanTHERIA_a_species-level_database_of_life_history_ecology_" \
                   "and_geography_of_extant_and_recently_extinct_mammals/3301274"
        self.urls = {"data": "https://ndownloader.figshare.com/files/5604752"}
        self.citation = "Kate E. Jones, Jon Bielby, Marcel Cardillo, Susanne A. Fritz, Justin O'Dell, C. David L. " \
                        "Orme, Kamran Safi, Wes Sechrest, Elizabeth H. Boakes, Chris Carbone, Christina Connolly, " \
                        "Michael J. Cutts, Janine K. Foster, Richard Grenyer, Michael Habib, Christopher A. " \
                        "Plaster, Samantha A. Price, Elizabeth A. Rigby, Janna Rist, Amber Teacher, Olaf R. P. " \
                        "Bininda-Emonds, John L. Gittleman, Georgina M. Mace, and Andy Purvis. 2009. PanTHERIA:a " \
                        "species-level database of life history, ecology, and geography of extant and recently " \
                        "extinct mammals. Ecology 90:2648."
        self.description = "PanTHERIA is a data set of multispecies trait data from diverse literature sources " \
                           "and also includes spatial databases of mammalian geographic ranges and global climatic " \
                           "and anthropogenic variables."
        self.keywords = ["mammals", "literature-compilation", "life-history"]

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value,
                                              nulls=['NA', '-999.00'])
        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value,
                                              missing_values=['NA', '-999.00'])

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        file_name = "PanTHERIA_1-0_WR05_Aug2008.txt"
        engine.download_files_from_archive(self.urls["data"], [file_name], "zip")
        # Create table Species
        engine.auto_create_table(Table('species',
                                       cleanup=self.cleanup_func_table),
                                 filename=file_name)
        engine.insert_data_from_file(engine.format_filename(file_name))


SCRIPT = main()
