#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description='The data is part of a monitoring project on vascular plant composition at the Tallgrass Prairie Preserve in Osage County, Oklahoma, USA.',
                           tags=['Taxon > Plants', 'Spatial Scale > Local', 'Data Type > Time Series', 'Data Type > Observational'],
                           citation='Daniel J. McGlinn, Peter G. Earls, and Michael W. Palmer. 2010. A 12-year study on the scaling of vascular plant composition in an Oklahoma tallgrass prairie. Ecology 91:1872.',
                           urls={'environment': 'http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv', 'climate': 'http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv', 'richness': 'http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv', 'cover': 'http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv', 'species': 'http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv', 'pres': 'http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv'},
                           shortname='McGlinn2010',
                           ref='http://esapubs.org/archive/ecol/E091/124/',
                           name='Vascular plant composition - McGlinn, et al., 2010')