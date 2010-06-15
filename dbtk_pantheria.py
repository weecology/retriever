# Database Toolkit for Ernest 2003 Ecological Archives
# Mammalian Life History Database

# Usage: python /file/path/to/dbtk_ernest2003.py

import dbtk_from_txt

# Create the Database
dbname = "Pantheria"
tablename = "pantheria"
pk = "species_id"
url = "http://esapubs.org/archive/ecol/E090/184/PanTHERIA_1-0_WR05_Aug2008.txt"
delimiter = None

dbcolumns=[("species_id"        ,    "INT(5) NOT NULL AUTO_INCREMENT"),
           ("sporder"           ,    "CHAR(20)"),
           ("family"            ,    "CHAR(20)"),
           ("genus"             ,    "CHAR(20)"),
           ("species"           ,    "CHAR(20)"),
           ("binomial"          ,    "CHAR(50)"),
           ("binomial 2"        ,    "combine"),
           ("activity_cycle"    ,    "INT(5)"),
           ("body_mass"         ,    "DECIMAL(10,2)"),
           ("forearm_length"    ,    "DECIMAL(10,2)"),
           ("head_body_length"  ,    "DECIMAL(10,2)"),
           ("age_eye_opening"   ,    "DECIMAL(10,2)"),
           ("age_first_birth"   ,    "DECIMAL(10,2)"),
           ("met_rate_mL02hr"   ,    "DECIMAL(10,2)"),
           ("met_rate_mass_g"   ,    "DECIMAL(10,2)"),
           ("diet_breadth"      ,    "INT(5)"),
           ("dispersal_age"     ,    "DECIMAL(10,2)"),
           ("gestation_len"     ,    "DECIMAL(10,2)"),
           ("habitat_breadth"   ,    "INT(5)"),
           ("home_range"        ,    "DECIMAL(20,10)"),
           ("home_range_indiv"  ,    "DECIMAL(20,10)"),
           ("interbirth_interval",   "DECIMAL(10,2)"),
           ("litter_size"       ,    "DECIMAL(10,2)"),
           ("litters_per_year"  ,    "DECIMAL(10,2)"),
           ("max_longevity"     ,    "DECIMAL(10,2)"),
           ("neonate_body_mass" ,    "DECIMAL(10,2)"),
           ("neonate_head_body_len", "DECIMAL(10,2)"),
           ("pop_density"       ,    "DECIMAL(10,2)"),
           ("pop_grp_size"      ,    "DECIMAL(10,2)"),
           ("sexual_maturity_age",   "DECIMAL(10,2)"),
           ("social_group_size" ,    "DECIMAL(10,2)"),
           ("teat_number"       ,    "INT(5)"),
           ("terrestriality"    ,    "INT(5)"),
           ("trophic_level"     ,    "INT(5)"),
           ("weaning_age"       ,    "DECIMAL(10,2)"),
           ("weaning_body_mass" ,    "DECIMAL(10,2)"),
           ("weaning_head_body_len", "DECIMAL(10,2)"),
           ("ref"               ,    "INT(5)"),
           ("adult_body_mass_ext",   "DECIMAL(10,2)"),
           ("litters_per_year_ext",  "DECIMAL(10,2)"),
           ("neonate_body_mass_ext", "DECIMAL(10,2)"),
           ("weaning_body_mass_ext", "DECIMAL(10,2)"),
           ("GR_area"           ,    "DECIMAL(10,2)"),
           ("GR_max_lat"        ,    "DECIMAL(10,2)"),
           ("GR_min_lat"        ,    "DECIMAL(10,2)"),
           ("GR_mid_range_lat"  ,    "DECIMAL(10,2)"),
           ("GR_max_long"       ,    "DECIMAL(10,2)"),
           ("GR_min_long"       ,    "DECIMAL(10,2)"),
           ("GR_mid_range_long" ,    "DECIMAL(10,2)"),
           ("hu_pop_den_min"    ,    "DECIMAL(10,2)"),
           ("hu_pop_den_mean"   ,    "DECIMAL(10,2)"),
           ("hu_pop_den_5p"     ,    "DECIMAL(10,2)"),
           ("hu_pop_den_change" ,    "DECIMAL(10,2)"),
           ("precip_mean"       ,    "DECIMAL(10,2)"),
           ("temp_mean"         ,    "DECIMAL(10,2)"),
           ("AET_mean"          ,    "DECIMAL(10,2)"),
           ("PET_mean"          ,    "DECIMAL(10,2)")]

dbtk_from_txt.setup(dbname, tablename, pk, url, delimiter, dbcolumns)    