#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'env': Table('env', replace_columns=[['check', 'checkrec']]),'trees': Table('trees', cleanup=Cleanup(correct_invalid_value, nulls=['.', '']),replace_columns=[['check', 'checkrec']])},
                           description="A data set collected in 1989 of vascular plant occurrences in overlapping grids of nested plots in the Oosting Natural Area of the Duke Forest, Orange County, North Carolina, USA.",
                           tags=['Taxon > Plants', 'Spatial Scale > Local', 'Data Type > Time Series', 'Data Type > Observational'],
                           citation="Michael W. Palmer, Robert K. Peet, Rebecca A. Reed, Weimin Xi, and Peter S. White. 2007. A multiscale study of vascular plants in a North Carolina Piedmont forest. Ecology 88:2674.",
                           urls={'species': 'http://esapubs.org/archive/ecol/E088/162/species_codes.txt', 'pres': 'http://esapubs.org/archive/ecol/E088/162/Oosting_pres2.txt', 'trees': 'http://esapubs.org/archive/ecol/E088/162/Oosting_Trees_1998.txt', 'env': 'http://esapubs.org/archive/ecol/E088/162/Oosting_env.txt'},
                           shortname="Palmer2007",
                           ref="http://esapubs.org/archive/ecol/E088/162/",
                           name="North Carolina forest plants (Ecological Archives 2007)")