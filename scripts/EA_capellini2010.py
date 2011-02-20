"""Capellini et al. 2010, Ecological Archives, Retriever Script"""

from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

SCRIPT = BasicTextTemplate(
    name = "Phylogeny and metabolic rates in mammals (Ecological Archives 2010)",
    description = "Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783-2793.",
    shortname = "MammalMR2010",
    ref = "http://www.esapubs.org/archive/ecol/E091/198/",
    urls = {"MammalMR2010": "http://www.esapubs.org/archive/ecol/E091/198/data.txt"},
    tables = {"MammalMR2010": Table("MammalMR2010", 
                                    cleanup = Cleanup(correct_invalid_value, nulls=[-9999]),
                                    )
              }
)