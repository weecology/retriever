# Database Toolkit for Pantheria dataset

# Usage: python /file/path/to/dbtk_pantheria.py

import dbtk_from_txt

# Variables to get text file/create database
dbname = "Pantheria"
tablename = "pantheria"
pk = "species_id"
url = "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"
delimiter = None

# Database column names and their data types. Use data type "skip" to skip the value, and
# "combine" to merge a string value into the previous column
dbcolumns=[("species_id"            ,   "INT(5) NOT NULL AUTO_INCREMENT"),
           ("sporder"               ,   "VARCHAR(20)"),
           ("family"                ,   "VARCHAR(20)"),
           ("genus"                 ,   "VARCHAR(20)"),
           ("species"               ,   "VARCHAR(20)"),
           ("binomial"              ,   "VARCHAR(50)"),
           ("binomial 2"            ,   "combine"),
           ("activity_cycle"        ,   "INT(5)"),
           ("body_mass"             ,   "DECIMAL(20,2)"),
           ("forearm_length"        ,   "DECIMAL(20,2)"),
           ("head_body_length"      ,   "DECIMAL(20,2)"),
           ("age_eye_opening"       ,   "DECIMAL(20,2)"),
           ("age_first_birth"       ,   "DECIMAL(20,2)"),
           ("met_rate_mL02hr"       ,   "DECIMAL(20,2)"),
           ("met_rate_mass_g"       ,   "DECIMAL(20,2)"),
           ("diet_breadth"          ,   "INT(5)"),
           ("dispersal_age"         ,   "DECIMAL(20,2)"),
           ("gestation_len"         ,   "DECIMAL(20,2)"),
           ("habitat_breadth"       ,   "INT(5)"),
           ("home_range"            ,   "DECIMAL(20,10)"),
           ("home_range_indiv"      ,   "DECIMAL(20,10)"),
           ("interbirth_interval"   ,   "DECIMAL(20,2)"),
           ("litter_size"           ,   "DECIMAL(20,2)"),
           ("litters_per_year"      ,   "DECIMAL(20,2)"),
           ("max_longevity"         ,   "DECIMAL(20,2)"),
           ("neonate_body_mass"     ,   "DECIMAL(20,2)"),
           ("neonate_head_body_len" ,   "DECIMAL(20,2)"),
           ("pop_density"           ,   "DECIMAL(20,2)"),
           ("pop_grp_size"          ,   "DECIMAL(20,2)"),
           ("sexual_maturity_age"   ,   "DECIMAL(20,2)"),
           ("social_group_size"     ,   "DECIMAL(20,2)"),
           ("teat_number"           ,   "INT(5)"),
           ("terrestriality"        ,   "INT(5)"),
           ("trophic_level"         ,   "INT(5)"),
           ("weaning_age"           ,   "DECIMAL(20,2)"),
           ("weaning_body_mass"     ,   "DECIMAL(20,2)"),
           ("weaning_head_body_len" ,   "DECIMAL(20,2)"),
           ("refs"                  ,   "VARCHAR(500)"),
           ("adult_body_mass_ext"   ,   "DECIMAL(20,2)"),
           ("litters_per_year_ext"  ,   "DECIMAL(20,2)"),
           ("neonate_body_mass_ext" ,   "DECIMAL(20,2)"),
           ("weaning_body_mass_ext" ,   "DECIMAL(20,2)"),
           ("GR_area"               ,   "DECIMAL(20,2)"),
           ("GR_max_lat"            ,   "DECIMAL(20,2)"),
           ("GR_min_lat"            ,   "DECIMAL(20,2)"),
           ("GR_mid_range_lat"      ,   "DECIMAL(20,2)"),
           ("GR_max_long"           ,   "DECIMAL(20,2)"),
           ("GR_min_long"           ,   "DECIMAL(20,2)"),
           ("GR_mid_range_long"     ,   "DECIMAL(20,2)"),
           ("hu_pop_den_min"        ,   "DECIMAL(20,2)"),
           ("hu_pop_den_mean"       ,   "DECIMAL(20,2)"),
           ("hu_pop_den_5p"         ,   "DECIMAL(20,2)"),
           ("hu_pop_den_change"     ,   "DECIMAL(20,2)"),
           ("precip_mean"           ,   "DECIMAL(20,2)"),
           ("temp_mean"             ,   "DECIMAL(20,2)"),
           ("AET_mean"              ,   "DECIMAL(20,2)"),
           ("PET_mean"              ,   "DECIMAL(20,2)")]

dbtk_from_txt.setup(dbname, tablename, pk, url, delimiter, dbcolumns)    