#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description="PanTHERIA is a data set of multispecies trait data from diverse literature sources and also includes spatial databases of mammalian geographic ranges and global climatic and anthropogenic variables.",
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation="Kate E. Jones, Jon Bielby, Marcel Cardillo, Susanne A. Fritz, Justin O'Dell, C. David L. Orme, Kamran Safi, Wes Sechrest, Elizabeth H. Boakes, Chris Carbone, Christina Connolly, Michael J. Cutts, Janine K. Foster, Richard Grenyer, Michael Habib, Christopher A. Plaster, Samantha A. Price, Elizabeth A. Rigby, Janna Rist, Amber Teacher, Olaf R. P. Bininda-Emonds, John L. Gittleman, Georgina M. Mace, and Andy Purvis. 2009. PanTHERIA:a species-level database of life history, ecology, and geography of extant and recently extinct mammals. Ecology 90:2648.",
                           urls={'species': 'http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt'},
                           shortname="Pantheria",
                           ref="http://esapubs.org/archive/ecol/E090/184/",
                           name="Pantheria (Ecological Archives 2009 - WR05)")