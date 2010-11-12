"""Daniel J. McGlinn, Peter G. Earls, and Michael W. Palmer. 2010. A 12-year 
study on the scaling of vascular plant composition in an Oklahoma tallgrass 
prairie. Ecology 91:1872.

"""

from dbtk.lib.templates import BasicTextTemplate
from dbtk.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.4'

SCRIPT = BasicTextTemplate(
                           name="Vascular plant composition - McGlinn, et al., 2010",
                           shortname="McGlinn2010",
                           ref="http://esapubs.org/archive/ecol/E091/124/",
                           urls={"pres": "http://esapubs.org/archive/ecol/E091/124/TGPP_pres.csv",
                                 "cover": "http://esapubs.org/archive/ecol/E091/124/TGPP_cover.csv",
                                 "richness": "http://esapubs.org/archive/ecol/E091/124/TGPP_rich.csv",
                                 "species": "http://esapubs.org/archive/ecol/E091/124/TGPP_specodes.csv",
                                 "environment": "http://esapubs.org/archive/ecol/E091/124/TGPP_env.csv",
                                 "climate": "http://esapubs.org/archive/ecol/E091/124/TGPP_clim.csv"}
                           )
