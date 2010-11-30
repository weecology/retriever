from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

replace_month_names = [("jan", "january"),
                       ("feb", "february"),
                       ("mar", "march"),
                       ("apr", "april"),
                       ("jun", "june"),
                       ("jul", "july"),
                       ("aug", "august"),
                       ("sep", "september"),
                       ("oct", "october"),
                       ("nov", "november"),
                       ("dec", "december")]

SCRIPT = BasicTextTemplate(
                           name="Kansas plant quadrats (Ecological Archives 2007)",
                           description="Peter B. Adler, William R. Tyburczy, and William K. Lauenroth. 2007. Long-term mapped quadrats from Kansas prairie: demographic information for herbaceaous plants. Ecology 88:2673.",
                           shortname="Adler2007",
                           ref="http://esapubs.org/archive/ecol/E088/161/",
                           urls = {
                                   "main": "http://esapubs.org/archive/ecol/E088/161/allrecords.csv",
                                   "quadrat_info": "http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv",
                                   "quadrat_inventory": "http://esapubs.org/archive/ecol/E088/161/quadrat_inventory.csv",
                                   "species": "http://esapubs.org/archive/ecol/E088/161/species_list.csv",
                                   "monthly_temp": "http://esapubs.org/archive/ecol/E088/161/monthly_temp.csv",
                                   "monthly_ppt": "http://esapubs.org/archive/ecol/E088/161/monthly_ppt.csv",
                                  },
                           tables = {
                                     "monthly_temp": Table("monthly_temp",
                                                           cleanup=Cleanup(correct_invalid_value,
                                                                           nulls=["NA"]),
                                                           replace_columns=replace_month_names),
                                     "monthly_ppt": Table("monthly_ppt",
                                                          replace_columns=replace_month_names,
                                                          cleanup=Cleanup(correct_invalid_value,
                                                                          nulls=["NA"]),
                                                          ),
                                     "quadrat_inventory": Table("quadrat_inventory",
                                                                cleanup=Cleanup(correct_invalid_value,
                                                                                nulls=["NA"]),
                                                                )
                                    }
                           )
