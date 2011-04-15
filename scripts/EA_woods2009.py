from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'sampling_history': Table('sampling_history', replace_columns=[('1935', 'yr_1935'), ('1948', 'yr_1948'), ('1974', 'yr_1974'), ('1978', 'yr_1978'), ('1979', 'yr_1979'), ('1989', 'yr_1989'), ('1992', 'yr_1992'), ('1993', 'yr_1993'), ('1994', 'yr_1994'), ('1997', 'yr_1997'), ('1999', 'yr_1999'), ('2001', 'yr_2001'), ('2002', 'yr_2002'), ('2004', 'yr_2004'), ('2007', 'yr_2007')])},
                           name="Michigan canopy dynamics (Ecological Archives 2009)",
                           tags=['Plants'],
                           ref="http://www.esapubs.org/archive/ecol/E090/251/",
                           urls={'all_plots_1935_1948': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/all_plots_1935_1948.txt', 'all_plots_1974_1980': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/all_plots_1974-1980.txt', 'swamp': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/swamp_all_modern.txt', 'sampling_history': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/sampling_history.txt', 'species_codes': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/species_codes.txt', 'upland_plots_1989_2007': 'http://www.esapubs.org/archive/ecol/E090/251/datafiles/upland_plots_89-07.txt'},
                           shortname="Woods2009",
                           description="Kerry D. Woods. 2009. Multi-decade, spatially explicit population studies of canopy dynamics in Michigan old-growth forests. Ecology 90:3587.")