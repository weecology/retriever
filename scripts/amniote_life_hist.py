# -*- coding: UTF-8 -*-
#retriever

from pkg_resources import parse_version

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script
from retriever.lib.defaults import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Amniote life History database"
        self.name = "amniote-life-hist"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '2.0.0'
        self.ref = "https://figshare.com/collections/An_amniote_life-history_database_to_perform_comparative_" \
                   "analyses_with_birds_mammals_and_reptiles/3308127"
        self.urls = {"data": "https://ndownloader.figshare.com/files/8067269"}
        self.citation = "Myhrvold, N.P., Baldridge, E., Chan, B., Sivam, D., Freeman, D.L. and Ernest, S.M., 2015. " \
                        "An amniote life-history database to perform comparative analyses with birds, mammals, " \
                        "and reptiles:Ecological Archives E096-269. Ecology, 96(11), pp.3109-000."
        self.description = "Compilation of life history traits for birds, mammals, and reptiles."
        self.keywords = ["mammals", "literature-compilation"]
        self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=['-999'])

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['-999'])

    def download(self, engine=None):
        Script.download(self, engine)
        engine = self.engine
        engine.download_files_from_archive(self.urls["data"], ["Data_Files/Amniote_Database_Aug_2015.csv",
                                                               "Data_Files/Amniote_Database_References_Aug_2015.csv",
                                                               "Data_Files/Amniote_Range_Count_Aug_2015.csv"],
                                           filetype="zip")

        ct_column = 'trait'  # all tables use the same ct_column name

        # Create tables from Amniote_Database_Aug.csv and Amniote_Database_References_Aug_2015.csv
        # Both reference and main have the same headers

        ct_names = ['female_maturity_d', 'litter_or_clutch_size_n', 'litters_or_clutches_per_y', 'adult_body_mass_g',
                    'maximum_longevity_y', 'gestation_d', 'weaning_d', 'birth_or_hatching_weight_g', 'weaning_weight_g',
                    'egg_mass_g', 'incubation_d', 'fledging_age_d', 'longevity_y', 'male_maturity_d',
                    'inter_litter_or_interbirth_interval_y', 'female_body_mass_g', 'male_body_mass_g',
                    'no_sex_body_mass_g', 'egg_width_mm', 'egg_length_mm', 'fledging_mass_g', 'adult_svl_cm',
                    'male_svl_cm', 'female_svl_cm', 'birth_or_hatching_svl_cm', 'female_svl_at_maturity_cm',
                    'female_body_mass_at_maturity_g', 'no_sex_svl_cm', 'no_sex_maturity_d']

        # Create table main from Amniote_Database_Aug_2015.csv

        columns = [
            ('record_id', ('pk-auto',)), ('class', ('char', '20')), ('order', ('char', '20')),
            ('family', ('char', '20')), ('genus', ('char', '20')), ('species', ('char', '50')),
            ('subspecies', ('char', '20')), ('common_name', ('char', '400')), ('trait_value', ('ct-double',))]
        table_main = Table('main', delimiter=',', cleanup=self.cleanup_func_table)
        table_main.ct_column = ct_column
        table_main.ct_names = ct_names
        table_main.columns = columns
        engine.auto_create_table(table_main,
                                 filename="Amniote_Database_Aug_2015.csv")
        engine.insert_data_from_file(engine.format_filename("Amniote_Database_Aug_2015.csv"))

        # Create table reference from Amniote_Database_References_Aug_2015.csv
        reference_columns = [
            ('record_id', ('pk-auto',)), ('class', ('char', '20')), ('order', ('char', '20')),
            ('family', ('char', '20')), ('genus', ('char', '20')), ('species', ('char', '50')),
            ('subspecies', ('char', '20')), ('common_name', ('char', '400')), ('reference', ('ct-char',))]

        table_references = Table('references', delimiter=',', cleanup=self.cleanup_func_table)
        table_references.ct_column = ct_column
        table_references.ct_names = ct_names
        table_references.columns = reference_columns
        engine.auto_create_table(table_references,
                                 filename="Amniote_Database_References_Aug_2015.csv")
        engine.insert_data_from_file(engine.format_filename("Amniote_Database_References_Aug_2015.csv"))

        # Create table Range
        # This table has different values for headers from the above tables.
        range_ct_names = ["min_female_maturity", "max_female_maturity", "count_female_maturity", "min_litter_clutch_size",
                    "max_litter_clutch_size", "count_litter_clutch_size", "min_litters_clutches",
                    "max_litters_clutches", "count_litters_clutches", "min_adult_body_mass", "max_adult_body_mass",
                    "count_adult_body_mass", "min_maximum_longevity", "max_maximum_longevity",
                    "count_maximum_longevity", "min_gestation", "max_gestation", "count_gestation", "min_weaning",
                    "max_weaning", "count_weaning", "min_birth_hatching_weight", "max_birth_hatching_weight",
                    "count_birth_hatching_weight", "min_weaning_weight", "max_weaning_weight", "count_weaning_weight",
                    "min_egg_mass", "max_egg_mass", "count_egg_mass", "min_incubation", "max_incubation",
                    "count_incubation", "min_fledging_age", "max_fledging_age", "count_fledging_age",
                    "min_male_maturity", "max_male_maturity", "count_male_maturity",
                    "min_inter_litter_interbirth_interval", "max_inter_litter_interbirth_interval",
                    "count_inter_litter_interbirth_interval", "min_female_body_mass", "max_female_body_mass",
                    "count_female_body_mass", "min_male_body_mass", "max_male_body_mass", "count_male_body_mass",
                    "min_no_sex_body_mass", "max_no_sex_body_mass", "count_no_sex_body_mass", "min_egg_width",
                    "max_egg_width", "count_egg_width", "min_egg_length", "max_egg_length", "count_egg_length",
                    "min_fledging_mass", "max_fledging_mass", "count_fledging_mass", "min_adult_svl", "max_adult_svl",
                    "count_adult_svl", "min_male_svl", "max_male_svl", "count_male_svl", "min_female_svl",
                    "max_female_svl", "count_female_svl", "min_hatching_svl", "max_hatching_svl", "count_hatching_svl",
                    "min_female_svl_at_maturity", "max_female_svl_at_maturity", "count_female_svl_at_maturity",
                    "min_female_body_mass_at_maturity", "max_female_body_mass_at_maturity",
                    "count_female_body_mass_at_maturity", "min_no_sex_svl", "max_no_sex_svl", "count_no_sex_svl",
                    "min_no_sex_maturity", "max_no_sex_maturity", "count_no_sex_maturity"]
        range_columns = [
            ('record_id', ('pk-auto',)), ('classx', ('char', '20')), ('orderx', ('char', '20')),
            ('familyx', ('char', '20')), ('genus', ('char', '20')), ('species', ('char', '50')),
            ('subspecies', ('char', '20')), ('common_name', ('char', '400')), ('trait_value', ('ct-double',))]

        table_range = Table('range', delimiter=',', cleanup=self.cleanup_func_table)
        table_range.ct_column = ct_column
        table_range.ct_names = range_ct_names
        table_range.columns = range_columns
        engine.auto_create_table(table_range,
                                 filename="Amniote_Range_Count_Aug_2015.csv")
        engine.insert_data_from_file(engine.format_filename("Amniote_Range_Count_Aug_2015.csv"))


SCRIPT = main()
