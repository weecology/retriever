# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.1",
                           name="fish-parasite-hosts",
                           title="Fish parasite host ecological characteristics (Strona, et al., 2013)",
                           citation="Giovanni Strona, Maria Lourdes D. Palomares, Nicolas Bailly, Paolo Galli, and Kevin D. Lafferty. 2013. Host range, host ecology, and distribution of more than 11800 fish parasite species. Ecology 94:544.",
                           retriever_minimum_version="2.0.dev",
                           tables={'host_characteristics': Table('host_characteristics', replace_columns=[[u'P_T', u'parasite_taxonomic_group'], [u'P_F', u'parasite_family'], [u'P_SP', u'parasite_species'], [u'H_C', u'host_class'], [u'H_O', u'host_order'], [u'H_F', u'host_family'], [u'H_SP', u'host_species'], [u'GEO', u'biogeographical_region'], [u'MaxL', u'maximum_host_bodylength'], [u'K', u'host_growth_rate'], [u'Y', u'host_life_span'], [u'Ym', u'host_age_first_maturity'], [u'T', u'host_trophic_level'], [u'F', u'freshwater'], [u'B', u'brackish'], [u'M', u'marine'], [u'AOO', u'area_of_occupancy'], [u'LAT', u'latitudinal_range'], [u'LON', u'longitudinal range']],cleanup=Cleanup(correct_invalid_value, missing_values=[u'na']))},
                           urls={u'host_characteristics': u'https://ndownloader.figshare.com/files/5624799'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3555378",
                           description="The data set includes 38008 fish parasite records (for Acanthocephala, Cestoda, Monogenea, Nematoda, Trematoda) compiled from scientific literature.")