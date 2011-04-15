from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={},
                           name="Vegetation plots - del Moral, 2010",
                           tags=['Plants'],
                           urls={'species_plot_year': 'http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_PLOT_YEAR.csv', 'species': 'http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_DESCRIPTORS.csv', 'structure_plot_year': 'http://esapubs.org/archive/ecol/E091/152/MSH_STRUCTURE_PLOT_YEAR.csv', 'plots': 'http://esapubs.org/archive/ecol/E091/152/MSH_PLOT_DESCRIPTORS.csv'},
                           shortname="DelMoral2010",
                           description="Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. Helens, Washington. Ecology 91:2185.")