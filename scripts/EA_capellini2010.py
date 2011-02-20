"""Capellini et al. 2010, Ecological Archives, Retriever Script"""

from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

replace = [
           ("Subclass", "subclass"),
           ("Order", "order"),
           ("Species", "species"),
           ("BMR (mlO2/hour)", "BMR_ml_O2_hr"),
           ("Body mass for BMR (gr)", "body_mass_bmr_g"),
           ("Reference for BMR", "reference_bmr"),
           ("FMR (kJ/day)", "FMR_kJ_day"),
           ("Body mass for FMR (gr)", "body_mass_fmr_g"),
           ("Reference for FMR", "reference_fmr")
           ]

SCRIPT = BasicTextTemplate(
    name = "Phylogeny and metabolic rates in mammals (Ecological Archives 2010)",
    description = "Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783–2793.",
    shortname = "MammalMR2010",
    ref = "http://www.esapubs.org/archive/ecol/E091/198/",
    urls = {"MammalMR2010": "http://www.esapubs.org/archive/ecol/E091/198/data.txt"},
    tables = {"MammalMR2010": Table("MammalMR2010", 
                                    cleanup = Cleanup(correct_invalid_value, nulls=[-9999]),
                                    replace_columns = replace
                                    )
              }
)