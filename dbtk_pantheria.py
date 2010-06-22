"""Database Toolkit for Pantheria dataset

Usage: python dbtk_pantheria.py [-u username] [--user=username] 
                                [-p password] [--password=password]
                                [-h {hostname} (default=localhost)] [--host=hostname] 
                                [-o {port} (default=3306)] [--port=port]

"""

import dbtk_tools

# Variables to get text file/create database
db = dbtk_tools.db_info()
table = dbtk_tools.table_info()
db.dbname = "Pantheria"
table.tablename = "pantheria"
table.pk = "species_id"
table.sourceurl = "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"

# Database column names and their data types.
# Data type is a tuple, with the first value specifying the type:
#     pk     - primary key
#     int    - integer
#     double - double precision
#     char   - string
#     but    - binary
# The second part of the type specifies the length and is optional
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

db.engine = dbtk_tools.choose_engine()
db.cursor = dbtk_tools.get_cursor(db)
dbtk_tools.create_table(db, table)