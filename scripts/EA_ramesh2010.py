from retriever.lib.templates import BasicTextTemplate

VERSION = '0.5'

SCRIPT = BasicTextTemplate(
                           name="Indian Forest Stand Structure (Ecological Archives 2010)",
                           description="B. R. Ramesh, M. H. Swaminath, Santoshgouda V. Patil, Dasappa, Raphael Pelissier, P. Dilip Venugopal, S. Aravajy, Claire Elouard, and S. Ramalingam. 2010. Forest stand structure and composition in 96 sites along environmental gradients in the central Western Ghats of India. Ecology 91:3118.",
                           shortname="Ramesh2010",
                           ref="http://esapubs.org/archive/ecol/E091/216/",
                           urls = {
                                   "macroplots": "http://esapubs.org/archive/ecol/E091/216/Macroplot_data.txt",
                                   "microplots": "http://esapubs.org/archive/ecol/E091/216/Microplot_data.txt",
                                   "sites": "http://esapubs.org/archive/ecol/E091/216/Site_variables.txt",
                                   "species": "http://esapubs.org/archive/ecol/E091/216/Species_list.txt"
                                   }
                           )
