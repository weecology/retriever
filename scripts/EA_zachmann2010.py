from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table

VERSION = '0.5'

replace = [
           ("jan", "january"),
           ("feb", "february"),
           ("mar", "march"),
           ("apr", "april"),
           ("jun", "june"),
           ("jul", "july"),
           ("aug", "august"),
           ("sep", "september"),
           ("oct", "october"),
           ("nov", "november"),
           ("dec", "december")
           ]

SCRIPT = BasicTextTemplate(
                           name="Sagebrush steppe quadrats (Ecological Archives 2010)",
                           description="Luke Zachmann, Corey Moffet, and Peter Adler. 2010. Mapped quadrats in sagebrush steppe: long-term data for analyzing demographic rates and plant-plant interactions. Ecology 91:3427.",
                           shortname="Zachmann2010",
                           tags=["Plants"],
                           ref="http://esapubs.org/archive/ecol/E091/243/",
                           urls = {
                                   "density": "http://esapubs.org/archive/ecol/E091/243/allrecords_density.csv",
                                   "cover": "http://esapubs.org/archive/ecol/E091/243/allrecords_cover.csv",
                                   "quad_info": "http://esapubs.org/archive/ecol/E091/243/quad_info.csv",
                                   "grazing": "http://esapubs.org/archive/ecol/E091/243/grazing_info.csv",
                                   "quad_inventory": "http://esapubs.org/archive/ecol/E091/243/quad_inventory.csv",
                                   "species": "http://esapubs.org/archive/ecol/E091/243/species_list.csv",
                                   "taxonomy": "http://esapubs.org/archive/ecol/E091/243/taxonomic_grouping.csv",
                                   "monthly_mean_temp" : "http://esapubs.org/archive/ecol/E091/243/monthly_mean_temp.csv",
                                   "monthly_ppt": "http://esapubs.org/archive/ecol/E091/243/total_monthly_ppt.csv",
                                   "monthly_sno": "http://esapubs.org/archive/ecol/E091/243/total_monthly_sno.csv",
                                   "counts" : "http://esapubs.org/archive/ecol/E091/243/annuals_counts_v3.csv"
                                   },
                           tables = {
                                      "monthly_mean_temp": Table("monthly_mean_temp", replace_columns=replace),
                                      "monthly_ppt": Table("monthly_ppt", replace_columns=replace),
                                      "monthly_sno": Table("monthly_sno", replace_columns=replace),
                                     }
                           )
