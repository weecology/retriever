"""Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. 
Helens, Washington. Ecology 91:2185.

"""

from retriever.lib.templates import BasicTextTemplate

VERSION = '0.5'

SCRIPT = BasicTextTemplate(
                           name="Vegetation plots - del Moral, 2010",
                           description="Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. Helens, Washington. Ecology 91:2185.",
                           shortname="DelMoral2010",
                           ref="http://esapubs.org/archive/ecol/E091/152/",
                           urls={"species_plot_year": "http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_PLOT_YEAR.csv",
                                 "structure_plot_year": "http://esapubs.org/archive/ecol/E091/152/MSH_STRUCTURE_PLOT_YEAR.csv",
                                 "species": "http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_DESCRIPTORS.csv",                              
                                 "plots": "http://esapubs.org/archive/ecol/E091/152/MSH_PLOT_DESCRIPTORS.csv"}
                           )
