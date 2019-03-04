# -*- coding: UTF-8 -*-
# retriever

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
        self.title = "Marine Predator and Prey Body Sizes - Barnes et al. 2008"
        self.name = "predator-prey-size-marine"
        self.retriever_minimum_version = "2.0.dev"
        self.version = "2.0.2"
        self.ref = "https://figshare.com/collections/PREDATOR_AND_PREY_BODY_SIZES_IN_MARINE_FOOD_WEBS/3300257"
        self.urls = {"data": "https://ndownloader.figshare.com/files/5601029"}
        self.citation = (
            "C. Barnes, D. M. Bethea, R. D. Brodeur, J. Spitz, V. Ridoux, C. Pusineri, B. C. Chase, "
            "M. E. Hunsicker, F. Juanes, A. Kellermann, J. Lancaster, F. Menard, F.-X. Bard, P. Munk, "
            "J. K. Pinnegar, F. S. Scharf, R. A. Rountree, K. I. Stergiou, C. Sassa, A. Sabates, and S. "
            "Jennings. 2008. Predator and prey body sizes in marine food webs. Ecology 89:881."
        )
        self.description = (
            "The data set contains relationships between predator and prey size which are needed to "
            "describe interactions of species and size classes in food webs."
        )
        self.keywords = ["fish", "literature-compilation", "size"]
        self.cleanup_func_table = Cleanup(
            correct_invalid_value, missing_values=["n/a", "0.0000E+00"]
        )

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(
                correct_invalid_value, nulls=["n/a", "0.0000E+00"]
            )

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        filename = "Predator_and_prey_body_sizes_in_marine_food_webs_vsn4.txt"
        engine.download_files_from_archive(
            self.urls["data"], [filename], filetype="zip"
        )

        # Create table Species

        engine.auto_create_table(
            Table("main", cleanup=self.cleanup_func_table), filename=filename
        )
        engine.insert_data_from_file(engine.format_filename(filename))


SCRIPT = main()
