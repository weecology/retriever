#retriever
"""Data Retriever script LEDA dataset"""
from builtins import str
from pkg_resources import parse_version

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import HOME_DIR, open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "A database on the life history traits of the Northwest European flora"
        self.name = "plant-life-hist-eu"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.4.3'
        self.ref = "http://www.uni-oldenburg.de/en/biology/landeco/research/projects/leda/"
        self.urls = {
            "Age_of_first_flowering": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/age_of_first_flowering.txt",
            "Branching": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/branching.txt",
            "Bud_bank_seasonality": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/buds_seasonality.txt",
            "Bud_vertical_distribution": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/buds_vertical_dist.txt",
            "Buoyancy": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/buoyancy.txt",
            "Canopy_height": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/canopy_height.txt",
            "Clonal_growth_organs": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/CGO.txt",
            "Dispersal_type": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/dispersal_type.txt",
            "Leaf_distribution_along_the_stem": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/leaf_distribution.txt",
            "Leaf_dry_matter_content": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/LDMC_und_Geo.txt",
            "Leaf_mass": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/leaf_mass.txt",
            "Leaf_size": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/leaf_size.txt",
            "Morphology_of_dispersal_unit": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/morphology_dispersal_unit.txt",
            "Plant_growth_form": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/plant_growth_form.txt",
            "Plant_life_span": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/plant_life_span.txt",
            "Releasing_height": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/releasing_height.txt",
            "Seed_bank": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/seed_bank.txt",
            "Seed_longevity": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/seed_longevity.txt",
            "Seed_mass": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/seed_mass.txt",
            "Seed_number": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/seed_number.txt",
            "Seed_shape": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/seed_shape.txt",
            "Shoot_growth_form": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/shoot_growth_form.txt",
            "Specific_leaf_area": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/SLA_und_geo_neu.txt",
            "Seed_number_per_shoot": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/SNP.txt",
            "Woodiness": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/ssd.txt",
            "Terminal_velocity": "http://www.uni-oldenburg.de/fileadmin/user_upload/biologie/ag/landeco/download/LEDA/Data_files/TV.txt",
        }
        self.citation = "KLEYER, M., BEKKER, R.M., KNEVEL, I.C., BAKKER, J.P, THOMPSON, K., SONNENSCHEIN, M., POSCHLOD, P., VAN GROENENDAEL, J.M., KLIMES, L., KLIMESOVA, J., KLOTZ, S., RUSCH, G.M., HERMY, M., ADRIAENS, D., BOEDELTJE, G., BOSSUYT, B., DANNEMANN, A., ENDELS, P., GoeTZENBERGER, L., HODGSON, J.G., JACKEL, A-K., KueHN, I., KUNZMANN, D., OZINGA, W.A., RoeMERMANN, C., STADLER, M., SCHLEGELMILCH, J., STEENDAM, H.J., TACKENBERG, O., WILMANN, B., CORNELISSEN, J.H.C., ERIKSSON, O., GARNIER, E., PECO, B. (2008): The LEDA Traitbase: A database of life-history traits of Northwest European flora. Journal of Ecology 96: 1266-1274"
        self.keywords = ['plants', 'observational']
        self.description = "The LEDA Traitbase provides information on plant traits that describe three key features of plant dynamics: persistence, regeneration and dispersal. "

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['NA'])
        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=['NA'])

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        for key in self.urls:
            self.engine.download_file(self.urls[key], self.urls[key].rpartition('/')[-1])
            new_file_path = self.engine.format_filename("new" + key)
            old_data = open_fr(self.engine.find_file(self.urls[key].rpartition('/')[-1]))
            new_data = open_fw(new_file_path)
            with old_data as file_block:

                # after the metadata lines, set data to True
                data = False
                for lines in file_block.readlines():
                    # meta data contins line with no ";" and may have "(;;;;)+" or empty lines
                    if not data and (";" not in lines or ";;;;" in lines):
                        pass
                    else:
                        data = True
                        new_data.write(lines)
            file_block.close()
            new_data.close()
            self.engine.auto_create_table(Table(key,
                                                cleanup=self.cleanup_func_table), filename=str("new" + key))
            self.engine.insert_data_from_file(new_file_path)


SCRIPT = main()
