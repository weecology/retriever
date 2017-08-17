#retriever

"""Retriever script for direct download of Bioclim data"""
from builtins import range

from retriever.lib.templates import Script
try:
    from retriever import VERSION
except ImportError:
    from retriever.lib.defaults import VERSION
from pkg_resources import parse_version


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Bioclim 2.5 Minute Climate Data"
        self.name = "bioclim"
        self.ref = "http://worldclim.org/bioclim"
        self.urls = {"climate": "http://biogeo.ucdavis.edu/data/climate/worldclim/1_4/grid/cur/bio_2-5m_bil.zip"}
        self.description = "Bioclimatic variables that are derived from the monthly temperature and rainfall values in order to generate more biologically meaningful variables."
        self.citation = "Hijmans, R.J., S.E. Cameron, J.L. Parra, P.G. Jones and A. Jarvis, 2005. Very high resolution interpolated climate surfaces for global land areas. International Journal of Climatology 25: 1965-1978."
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.2.1'
        self.keywords = ["climate"]
        
        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
        
    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            raise Exception("The Bioclim dataset contains only non-tabular data files, and can only be used with the 'download only' engine.")
        Script.download(self, engine, debug)
        file_names = []
        for file_num in range(1, 20):
            for ext in (['bil', 'hdr']):
                file_names += ["bio{0}.{1}".format(file_num, ext)]
        self.engine.download_files_from_archive(self.urls["climate"], file_names)
        self.engine.register_files(file_names)

SCRIPT = main()

