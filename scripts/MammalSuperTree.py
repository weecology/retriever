# retriever
from pkg_resources import parse_version

SCRIPT_VER = "1.2.3"
try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION

if parse_version(VERSION) <= parse_version("2.0.0"):
    from retriever.lib.templates import DownloadOnlyTemplate

    class main(DownloadOnlyTemplate):
        def __init__(self, **kwargs):
            DownloadOnlyTemplate.__init__(self, **kwargs)
            self.name = "Mammal Super Tree"
            self.shortname = "mammal-super-tree"
            self.ref = "http://doi.org/10.1111/j.1461-0248.2009.01307.x"
            self.citation = "Fritz, S. A., Bininda-Emonds, O. R. P. and Purvis, A. (2009), Geographical variation in predictors of mammalian extinction risk: big is bad, but only in the tropics. Ecology Letters, 12: 538-549. doi:10.1111/j.1461-0248.2009.01307.x"
            self.description = "Mammal Super Tree from Fritz, S.A., O.R.P Bininda-Emonds, and A. Purvis. 2009. Geographical variation in predictors of mammalian extinction risk: big is bad, but only in the tropics. Ecology Letters 12:538-549"
            self.retriever_minimum_version = "2.0.dev"
            self.version = "1.2.3"
            self.urls = {
                "mammal_super_tree_fritz2009.tre": "http://onlinelibrary.wiley.com/store/10.1111/j.1461-0248.2009.01307.x/asset/supinfo/ELE_1307_sm_SA1.tre?v=1&s=366b28651a9b5d1a3148ef9a8620f8aa31a7df44"
            }


else:
    from retriever.lib.templates import Script
    from retriever.lib.models import Table

    class main(Script):
        def __init__(self, **kwargs):
            Script.__init__(self, **kwargs)
            self.title = "Mammal Super Tree"
            self.name = "mammal-super-tree"
            self.ref = "http://doi.org/10.1111/j.1461-0248.2009.01307.x"
            self.citation = "Fritz, S. A., Bininda-Emonds, O. R. P. and Purvis, A. (2009), Geographical variation in predictors of mammalian extinction risk: big is bad, but only in the tropics. Ecology Letters, 12: 538-549. doi:10.1111/j.1461-0248.2009.01307.x"
            self.description = "Mammal Super Tree from Fritz, S.A., O.R.P Bininda-Emonds, and A. Purvis. 2009. Geographical variation in predictors of mammalian extinction risk: big is bad, but only in the tropics. Ecology Letters 12:538-549"
            self.retriever_minimum_version = "2.0.dev"
            self.version = "1.2.3"
            self.urls = {
                "mammal_super_tree_fritz2009.tre": "http://onlinelibrary.wiley.com/store/10.1111/j.1461-0248.2009.01307.x/asset/supinfo/ELE_1307_sm_SA1.tre?v=1&s=366b28651a9b5d1a3148ef9a8620f8aa31a7df44"
            }
            self.downlaod_only = True
            self.tables = {"trees": Table("trees")}

        def download(self, engine=None, debug=False):
            if engine.name != "Download Only":
                raise Exception(
                    "The mammal-super-tree dataset contains only non-tabular data files, and can only be used with the 'download only' engine."
                )
            Script.download(self, engine, debug)


SCRIPT = main()
