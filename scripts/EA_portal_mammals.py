"""Retriever script for the Portal Project mammals

Dataset published by Ernest et al. 2009 in Ecological Archives.

"""

#TO DO - confirm column reversal with authors and correct

from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

SCRIPT = BasicTextTemplate(
                           name="Portal Project Mammals (Ecological Archives 2009)",
                           description="S. K. Morgan Ernest, Thomas J. Valone, and James H. Brown. 2009. Long-term monitoring and experimental manipulation of a Chihuahuan Desert ecosystem near Portal, Arizona, USA. Ecology 90:1708.",
                           shortname="PortalMammals",
                           tags=["Animals", "Mammals"],
                           ref="http://esapubs.org/archive/ecol/E090/118/",
                           tables = {
                                     "plots": Table("plots", 
                                                    delimiter=',', 
                                                    contains_pk=True,
                                                    header_rows=0,
                                                    columns=[("PlotID"            , ("pk-auto",) ),
                                                             ("PlotTypeAlphaCode" , ("char", 2)  ),
                                                             ("PlotTypeNumCode"   , ("int",)     ),
                                                             ("PlotTypeDescript"  , ("char", 30) )]
                                                    ),
                                     "main": Table("main", 
                                                   cleanup=Cleanup(correct_invalid_value,
                                                                   nulls=[])
                                                   ),
                                     },
                           urls = {
                                   "main": "http://esapubs.org/archive/ecol/E090/118/Portal_rodents_19772002.csv",
                                   "species": "http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt",
                                   "plots": "http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt"
                                   }
                           )
