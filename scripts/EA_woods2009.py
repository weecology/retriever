from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table

VERSION = '0.5'

replace = [(str(year), 'yr_' + str(year)) for year in [1935, 1948, 1974, 1978, 1979, 1989, 1992, 1993, 1994, 1997, 1999, 2001, 2002, 2004, 2007]]

SCRIPT = BasicTextTemplate(
                           name="Michigan canopy dynamics (Ecological Archives 2009)",
                           description="Kerry D. Woods. 2009. Multi-decade, spatially explicit population studies of canopy dynamics in Michigan old-growth forests. Ecology 90:3587.",
                           shortname="Woods2009",
                           ref="http://www.esapubs.org/archive/ecol/E090/251/",
                           urls = {
                                   "all_plots_1935_1948": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/all_plots_1935_1948.txt",
                                   "all_plots_1974_1980": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/all_plots_1974-1980.txt",
                                   "upland_plots_1989_2007": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/upland_plots_89-07.txt",
                                   "swamp": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/swamp_all_modern.txt",
                                   "species_codes": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/species_codes.txt",
                                   "sampling_history": "http://www.esapubs.org/archive/ecol/E090/251/datafiles/sampling_history.txt"
                                   },
                           tables = {
                                     "sampling_history": Table("sampling_history",
                                                               replace_columns = replace)
                                     }
                           )
