"""Database Toolkit for Pantheria dataset

"""

from dbtk_ui import *

class EAPantheria(DbTk):
    name = "Pantheria"
    shortname = "Pantheria"
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
        table.cleanup = Cleanup(correct_invalid_value, {"nulls":("-999", "-999.00", -999)} )
        
        decimalformat = ("decimal","30,20")
        table.columns=[("species_id"            ,   ("pk-auto",)    ),
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
                       ("home_range"            ,   decimalformat   ),
                       ("home_range_indiv"      ,   decimalformat   ),
                       ("interbirth_interval"   ,   ("double",)     ),
                       ("litter_size"           ,   ("double",)     ),
                       ("litters_per_year"      ,   ("double",)     ),
                       ("max_longevity"         ,   ("double",)     ),
                       ("neonate_body_mass"     ,   decimalformat   ),
                       ("neonate_head_body_len" ,   decimalformat   ),
                       ("pop_density"           ,   decimalformat   ),
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
                       ("GR_area"               ,   decimalformat   ),
                       ("GR_max_lat"            ,   decimalformat   ),
                       ("GR_min_lat"            ,   decimalformat   ),
                       ("GR_mid_range_lat"      ,   decimalformat   ),
                       ("GR_max_long"           ,   decimalformat   ),
                       ("GR_min_long"           ,   decimalformat   ),
                       ("GR_mid_range_long"     ,   decimalformat   ),
                       ("hu_pop_den_min"        ,   decimalformat   ),
                       ("hu_pop_den_mean"       ,   decimalformat   ),
                       ("hu_pop_den_5p"         ,   decimalformat   ),
                       ("hu_pop_den_change"     ,   decimalformat   ),
                       ("precip_mean"           ,   ("double",)     ),
                       ("temp_mean"             ,   ("double",)     ),
                       ("AET_mean"              ,   ("double",)     ),
                       ("PET_mean"              ,   ("double",)     )]
        engine.table = table
        engine.create_table()
        
        engine.insert_data_from_url("http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt")
        
        return engine        
        
        
if __name__ == "__main__":
    me = EAPantheria()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:        
        final_cleanup(me.download())