#retriever

"""Retriever script for direct download of Bioclim data"""

from retriever.lib.templates import Script


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Bioclim 2.5 Minute Climate Data"
        self.shortname = "Bioclim"
        self.ref = "http://worldclim.org/bioclim"
        self.urls = {"climate": "http://biogeo.ucdavis.edu/data/climate/worldclim/1_4/grid/cur/bio_2-5m_bil.zip"}

    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            raise Exception("The Bioclim dataset contains only non-tabular data files, and can only be used with the 'download only' engine.")
        Script.download(self, engine, debug)
        file_names = ["bio%s.bil" % file_num for file_num in range(1, 20)]
        self.engine.download_files_from_archive(self.urls["climate"], file_names)
        self.engine.register_files(file_names)

SCRIPT = main()
