from dbtk.lib.templates import BasicTextTemplate

VERSION = '0.4.1'

SCRIPT = BasicTextTemplate(
                           name="Vascular plant composition - McGlinn, et al., 2010",
                           description="S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
                           shortname="McGlinn2010",
                           ref="http://esapubs.org/archive/ecol/E091/124/",
                           urls={"pres": "http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv",
                                 "cover": "http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv",
                                 "richness": "http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv",
                                 "species": "http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv",
                                 "environment": "http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv",
                                 "climate": "http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv"}
                           )
