from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={},
                           name="Indian Forest Stand Structure (Ecological Archives 2010",
                           tags=['Plants'],
                           urls={'species': 'http://esapubs.org/archive/ecol/E091/216/Species_list.txt', 'macroplots': 'http://esapubs.org/archive/ecol/E091/216/Macroplot_data.txt', 'microplots': 'http://esapubs.org/archive/ecol/E091/216/Microplot_data.txt', 'sites': 'http://esapubs.org/archive/ecol/E091/216/Site_variables.txt'},
                           shortname="Ramesh2010",
                           description="B. R. Ramesh, M. H. Swaminath, Santoshgouda V. Patil, Dasappa, Raphael Pelissier, P. Dilip Venugopal, S. Aravajy, Claire Elouard, and S. Ramalingam. 2010. Forest stand structure and composition in 96 sites along environmental gradients in the central Western Ghats of India. Ecology 91:3118.")