#retriever

"""Retriever script for direct download of data data"""
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script
from retriever import VERSION
from pkg_resources import parse_version


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "PREDICTS Database"
        self.name = "predicts"
        self.ref = "http://data.nhm.ac.uk/dataset/902f084d-ce3f-429f-a6a5-23162c73fdf7"
        self.urls = {"PREDICTS": "http://data.nhm.ac.uk/dataset/the-2016-release-of-the-predicts-database/resource/78dac1a9-6aa0-4dcb-9750-50df04f8ca6e/download"}
        self.citation = "Lawrence N Hudson; Tim Newbold; Sara Contu; Samantha L L Hill et al. (2016). Dataset: The 2016 release of the PREDICTS database. http://dx.doi.org/10.5519/0066354"
        self.keywords = ['biodiversity', 'anthropogenic pressures']
        self.retriever_minimum_version = "2.0.dev"
        self.version = "1.0.0"
        self.description = "A dataset of 3,250,404 measurements, collated from 26,114 sampling locations in 94 countries and representing 47,044 species."

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        filename = "predicts_data.csv"
        tablename = "predicts_main"

        table = Table(str(tablename) , delimiter=',' )
        table.columns = [   ("Source_ID", ("pk-auto")),
                            ("Reference", ("char")),
                            ("Study_number", ("int")),
                            ("Study_name", ("char")),
                            ("SS", ("char")),
                            ("Diversity_metric", ("char")),
                            ("Diversity_metric_unit", ("char")),
                            ("Diversity_metric_type", ("char")),
                            ("Diversity_metric_is_effort_sensitive", ("Logical")),
                            ("Diversity_metric_is_suitable_for_Chao", ("Logical")),
                            ("Sampling_method", ("char")),
                            ("Sampling_effort_unit", ("char")),
                            ("Study_common_taxon", ("char")),
                            ("Rank_of_study_common_taxon", ("char")),
                            ("Site_number", ("int")),
                            ("Site_name", ("char")),
                            ("Block", ("int")),
                            ("SSS", ("char")),
                            ("SSB", ("char")),
                            ("SSBS", ("char")),
                            ("Sample_start_earliest", ("char")),
                            ("Sample_end_latest", ("char")),
                            ("Sample_midpoint", ("char")),
                            ("Sample_date_resolution", ("char")),
                            ("Max_linear_extent_metres", ("float")),
                            ("Habitat_patch_area_square_metres", ("float")),
                            ("Sampling_effort", ("float")),
                            ("Rescaled_sampling_effort", ("float")),
                            ("Habitat_as_described", ("char")),
                            ("Predominant_land_use", ("char")),
                            ("Source_for_predominant_land_use", ("char")),
                            ("Use_intensity", ("char")),
                            ("Km_to_nearest_edge_of_habitat", ("float")),
                            ("Years_since_fragmentation_or_conversion", ("float")),
                            ("Transect_details", ("char")),
                            ("Coordinates_method", ("char")),
                            ("Longitude", ("float")),
                            ("Latitude", ("float")),
                            ("Country_distance_metres", ("int")),
                            ("Country", ("char")),
                            ("UN_subregion", ("char")),
                            ("UN_region", ("char")),
                            ("Ecoregion_distance_metres", ("float")),
                            ("Ecoregion", ("char")),
                            ("Biome", ("char")),
                            ("Realm", ("char")),
                            ("Hotspot", ("char")),
                            ("Wilderness_area", ("char")),
                            ("N_samples", ("int")),
                            ("Taxon_number", ("int")),
                            ("Taxon_name_entered", ("char")),
                            ("Indication", ("char")),
                            ("Parsed_name", ("char")),
                            ("Taxon", ("char")),
                            ("COL_ID", ("int")),
                            ("Name_status", ("char")),
                            ("Rank", ("char")),
                            ("Kingdom", ("char")),
                            ("Phylum", ("char")),
                            ("Class", ("char")),
                            ("Order", ("char")),
                            ("Family", ("char")),
                            ("Genus", ("char")),
                            ("Species", ("char")),
                            ("Best_guess_binomial", ("char")),
                            ("Higher_taxa", ("char")),
                            ("Higher_taxon", ("char")),
                            ("Measurement", ("float")),
                            ("Effort_corrected_measurement", ("float"))]

        engine.table = table
        if not os.path.isfile(engine.format_filename(filename)):
            engine.download_files_from_archive(self.urls["PREDICTS"], [filename], filetype="zip", archivename="predicts_data")
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(str(filename)))

SCRIPT = main()
