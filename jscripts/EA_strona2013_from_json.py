#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'host_characteristics': Table('host_characteristics', cleanup=Cleanup(correct_invalid_value, nulls=['na']),replace_columns=[['P_T', 'parasite_taxonomic_group'], ['P_F', 'parasite_family'], ['P_SP', 'parasite_species'], ['H_C', 'host_class'], ['H_O', 'host_order'], ['H_F', 'host_family'], ['H_SP', 'host_species'], ['GEO', 'biogeographical_region'], ['MaxL', 'maximum_host_bodylength'], ['K', 'host_growth_rate'], ['Y', 'host_life_span'], ['Ym', 'host_age_first_maturity'], ['T', 'host_trophic_level'], ['F', 'freshwater'], ['B', 'brackish'], ['M', 'marine'], ['AOO', 'area_of_occupancy'], ['LAT', 'latitudinal_range'], ['LON', 'longitudinal range']])},
                           description='The data set includes 38008 fish parasite records (for Acanthocephala, Cestoda, Monogenea, Nematoda, Trematoda) compiled from scientific literature.',
                           citation='Giovanni Strona, Maria Lourdes D. Palomares, Nicolas Bailly, Paolo Galli, and Kevin D. Lafferty. 2013. Host range, host ecology, and distribution of more than 11800 fish parasite species. Ecology 94:544.',
                           urls={'host_characteristics': 'http://esapubs.org/archive/ecol/E094/045/FPEDB.csv'},
                           shortname='FishParasiteHosts',
                           name='Fish parasite host ecological characteristics - Strona, et al., 2013')