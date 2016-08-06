#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'main': Table('main', ct_names=['female_maturity_d', 'litter_or_clutch_size_n', 'litters_or_clutches_per_y', 'adult_body_mass_g', 'maximum_longevity_y', 'gestation_d', 'weaning_d', 'birth_or_hatching_weight_g', 'weaning_weight_g', 'egg_mass_g', 'incubation_d', 'fledging_age_d', 'longevity_y', 'male_maturity_d', 'inter_litter_or_interbirth_interval_y', 'female_body_mass_g', 'male_body_mass_g', 'no_sex_body_mass_g', 'egg_width_mm', 'egg_length_mm', 'fledging_mass_g', 'adult_svl_cm', 'male_svl_cm', 'female_svl_cm', 'birth_or_hatching_svl_cm', 'female_svl_at_maturity_cm', 'female_body_mass_at_maturity_g', 'no_sex_svl_cm', 'no_sex_maturity_d'],delimiter=',',cleanup=Cleanup(correct_invalid_value, nulls=[-999]),columns=[('record_id', ('pk-auto',)), ('class', ('char', '20')), ('order', ('char', '20')), ('family', ('char', '20')), ('genus', ('char', '20')), ('species', ('char', '20')), ('subspecies', ('char', '20')), ('common_name', ('char', '40')), ('trait_value', ('ct-double',))],ct_column='trait')},
                           description='Compilation of life history traits for birds, mammals, and reptiles.',
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation='Myhrvold, N.P., Baldridge, E., Chan, B., Sivam, D., Freeman, D.L. and Ernest, S.M., 2015. An amniote life-history database to perform comparative analyses with birds, mammals, and reptiles:Ecological Archives E096-269. Ecology, 96(11), pp.3109-000.',
                           urls={'main': 'http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv'},
                           shortname='AmnioteDB',
                           ref='http://esapubs.org/archive/ecol/E096/269',
                           name='Amniote life History database')