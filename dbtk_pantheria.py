"""Database Toolkit for Pantheria dataset

See dbtk_tools.py for usage

"""

import datacleanup
from dbtk_tools import *
import dbtk_ui

class DbTk_Pantheria(DbTk):
    name = "Pantheria"
    url = ""
    required_opts = []
    def download(self, engine=None):            
        # Variables to get text file/create database        
        engine = self.checkengine(engine)
        
        db = Database()
        db.dbname = "Pantheria"
        engine.db = db
        engine.get_cursor()
        engine.create_db()
        
        table = Table()
        table.tablename = "pantheria"
        table.pk = "species_id"        
        table.cleanup = datacleanup.correct_invalid_value
        table.nullindicators = ["-999", "-999.00", -999]
        
        table.columns=[("species_id"            ,   ("pk",)         ),
                       ("sporder"               ,   ("char", 20)    ),
                       ("family"                ,   ("char", 20)    ),
                       ("genus"                 ,   ("char", 20)    ),
                       ("species"               ,   ("char", 20)    ),
                       ("binomial"              ,   ("char", 50)    ),
                       ("binomial 2"            ,   ("combine",)    ),
                       ("activity_cycle"        ,   ("double",)     ),
                       ("body_mass"             ,   ("double",)     ),
                       ("forearm_length"        ,   ("double",)     ),
                       ("head_body_length"      ,   ("double",)     ),
                       ("age_eye_opening"       ,   ("double",)     ),
                       ("age_first_birth"       ,   ("double",)     ),
                       ("met_rate_mL02hr"       ,   ("double",)     ),
                       ("met_rate_mass_g"       ,   ("double",)     ),
                       ("diet_breadth"          ,   ("double",)     ),
                       ("dispersal_age"         ,   ("double",)     ),
                       ("gestation_len"         ,   ("double",)     ),
                       ("habitat_breadth"       ,   ("double",)     ),
                       ("home_range"            ,   ("double",)     ),
                       ("home_range_indiv"      ,   ("double",)     ),
                       ("interbirth_interval"   ,   ("double",)     ),
                       ("litter_size"           ,   ("double",)     ),
                       ("litters_per_year"      ,   ("double",)     ),
                       ("max_longevity"         ,   ("double",)     ),
                       ("neonate_body_mass"     ,   ("double",)     ),
                       ("neonate_head_body_len" ,   ("double",)     ),
                       ("pop_density"           ,   ("double",)     ),
                       ("pop_grp_size"          ,   ("double",)     ),
                       ("sexual_maturity_age"   ,   ("double",)     ),
                       ("social_group_size"     ,   ("double",)     ),
                       ("teat_number"           ,   ("double",)     ),
                       ("terrestriality"        ,   ("double",)     ),
                       ("trophic_level"         ,   ("double",)     ),
                       ("weaning_age"           ,   ("double",)     ),
                       ("weaning_body_mass"     ,   ("double",)     ),
                       ("weaning_head_body_len" ,   ("double",)     ),
                       ("refs"                  ,   ("char", 500)   ),
                       ("adult_body_mass_ext"   ,   ("double",)     ),
                       ("litters_per_year_ext"  ,   ("double",)     ),
                       ("neonate_body_mass_ext" ,   ("double",)     ),
                       ("weaning_body_mass_ext" ,   ("double",)     ),
                       ("GR_area"               ,   ("double",)     ),
                       ("GR_max_lat"            ,   ("double",)     ),
                       ("GR_min_lat"            ,   ("double",)     ),
                       ("GR_mid_range_lat"      ,   ("double",)     ),
                       ("GR_max_long"           ,   ("double",)     ),
                       ("GR_min_long"           ,   ("double",)     ),
                       ("GR_mid_range_long"     ,   ("double",)     ),
                       ("hu_pop_den_min"        ,   ("double",)     ),
                       ("hu_pop_den_mean"       ,   ("double",)     ),
                       ("hu_pop_den_5p"         ,   ("double",)     ),
                       ("hu_pop_den_change"     ,   ("double",)     ),
                       ("precip_mean"           ,   ("double",)     ),
                       ("temp_mean"             ,   ("double",)     ),
                       ("AET_mean"              ,   ("double",)     ),
                       ("PET_mean"              ,   ("double",)     )]
        engine.table = table
        engine.table.source = engine.open_url("http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt")
        
        engine.create_table()
        engine.add_to_table()
        
        
if __name__ == "__main__":
    me = DbTk_Pantheria()
    if len(sys.argv) == 1:                
        dbtk_ui.launch_wizard([me])
    else:
        me.download()