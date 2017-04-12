# -*- coding: UTF-8 -*-
#retriever

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Pantheria (Jones et al. 2009)"
        self.shortname = "pantheria"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.2.0'
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
        self.tags = ["mammals", "literature-compilation", "life-history"]

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        engine.download_files_from_archive(self.urls["data"], ["PanTHERIA_1-0_WR05_Aug2008.txt"],
                                           filetype="zip")

        # Create table Species
        engine.auto_create_table(Table('species', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),
                                 filename="PanTHERIA_1-0_WR05_Aug2008.txt")
        engine.insert_data_from_file(engine.format_filename("PanTHERIA_1-0_WR05_Aug2008.txt"))

SCRIPT = main()
