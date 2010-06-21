"""Database Toolkit for Pantheria dataset

Usage: python dbtk_pantheria.py [-u username] [--user=username] 
                                [-p password] [--password=password]
                                [-h {hostname} (default=localhost)] [--host=hostname] 
                                [-o {port} (default=3306)] [--port=port]

"""

import dbtk_tools

# Variables to get text file/create database
dbinfo = dbtk_tools.db_info()
dbinfo.dbname = "Pantheria"
dbinfo.tablename = "pantheria"
dbinfo.pk = "species_id"
dbinfo.url = "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"

# Database column names and their data types. Use data type "skip" to skip the value,
# and "combine" to merge a string value into the previous column
dbinfo.dbcolumns=[("species_id"            ,   "INT(5) NOT NULL AUTO_INCREMENT"),
                  ("sporder"               ,   "VARCHAR(20)"),
                  ("family"                ,   "VARCHAR(20)"),
                  ("genus"                 ,   "VARCHAR(20)"),
                  ("species"               ,   "VARCHAR(20)"),
                  ("binomial"              ,   "VARCHAR(50)"),
                  ("binomial 2"            ,   "combine"),
                  ("activity_cycle"        ,   "INT(5)"),
                  ("body_mass"             ,   "DOUBLE"),
                  ("forearm_length"        ,   "DOUBLE"),
                  ("head_body_length"      ,   "DOUBLE"),
                  ("age_eye_opening"       ,   "DOUBLE"),
                  ("age_first_birth"       ,   "DOUBLE"),
                  ("met_rate_mL02hr"       ,   "DOUBLE"),
                  ("met_rate_mass_g"       ,   "DOUBLE"),
                  ("diet_breadth"          ,   "INT(5)"),
                  ("dispersal_age"         ,   "DOUBLE"),
                  ("gestation_len"         ,   "DOUBLE"),
                  ("habitat_breadth"       ,   "INT(5)"),
                  ("home_range"            ,   "DOUBLE"),
                  ("home_range_indiv"      ,   "DOUBLE"),
                  ("interbirth_interval"   ,   "DOUBLE"),
                  ("litter_size"           ,   "DOUBLE"),
                  ("litters_per_year"      ,   "DOUBLE"),
                  ("max_longevity"         ,   "DOUBLE"),
                  ("neonate_body_mass"     ,   "DOUBLE"),
                  ("neonate_head_body_len" ,   "DOUBLE"),
                  ("pop_density"           ,   "DOUBLE"),
                  ("pop_grp_size"          ,   "DOUBLE"),
                  ("sexual_maturity_age"   ,   "DOUBLE"),
                  ("social_group_size"     ,   "DOUBLE"),
                  ("teat_number"           ,   "INT(5)"),
                  ("terrestriality"        ,   "INT(5)"),
                  ("trophic_level"         ,   "INT(5)"),
                  ("weaning_age"           ,   "DOUBLE"),
                  ("weaning_body_mass"     ,   "DOUBLE"),
                  ("weaning_head_body_len" ,   "DOUBLE"),
                  ("refs"                  ,   "VARCHAR(500)"),
                  ("adult_body_mass_ext"   ,   "DOUBLE"),
                  ("litters_per_year_ext"  ,   "DOUBLE"),
                  ("neonate_body_mass_ext" ,   "DOUBLE"),
                  ("weaning_body_mass_ext" ,   "DOUBLE"),
                  ("GR_area"               ,   "DOUBLE"),
                  ("GR_max_lat"            ,   "DOUBLE"),
                  ("GR_min_lat"            ,   "DOUBLE"),
                  ("GR_mid_range_lat"      ,   "DOUBLE"),
                  ("GR_max_long"           ,   "DOUBLE"),
                  ("GR_min_long"           ,   "DOUBLE"),
                  ("GR_mid_range_long"     ,   "DOUBLE"),
                  ("hu_pop_den_min"        ,   "DOUBLE"),
                  ("hu_pop_den_mean"       ,   "DOUBLE"),
                  ("hu_pop_den_5p"         ,   "DOUBLE"),
                  ("hu_pop_den_change"     ,   "DOUBLE"),
                  ("precip_mean"           ,   "DOUBLE"),
                  ("temp_mean"             ,   "DOUBLE"),
                  ("AET_mean"              ,   "DOUBLE"),
                  ("PET_mean"              ,   "DOUBLE")]

dbinfo.cursor = dbtk_tools.get_cursor_mysql()
dbtk_tools.setup(dbinfo)    