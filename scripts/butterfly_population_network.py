# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.2",
                           description="Stephen F. Matter, Nusha Keyghobadhi, and Jens Roland. 2014. Ten years of abundance data within a spatial population network of the alpine butterfly, Parnassius smintheus. Ecology 95:2985.",
                           title="Spatial Population Data Alpine Butterfly - Matter et al 2014",
                           citation="Matter, Stephen F., Nusha Keyghobadhi, and Jens Roland. 2014. Ten years of abundance data within a spatial population network of the alpine butterfly, Parnassius smintheus. Ecology 95:2985. Ecological Archives E095-258.",
                           name="butterfly-population-network",
                           keywords=[u'butterflies', u'observational'],
                           retriever_minimum_version="2.0.dev",
                           tables={'Dispersal': Table('Dispersal', cleanup=Cleanup(correct_invalid_value, missing_values=[u'n/a'])),'Landscape': Table('Landscape', cleanup=Cleanup(correct_invalid_value, missing_values=[u'n/a'])),'PopulationAbunTransect': Table('PopulationAbunTransect', cleanup=Cleanup(correct_invalid_value, missing_values=[u'n/a'])),'PopulationAbunMark_Recap': Table('PopulationAbunMark_Recap', cleanup=Cleanup(correct_invalid_value, missing_values=[u'n/a']))},
                           urls={u'Dispersal': u'https://ndownloader.figshare.com/files/5632170', u'Landscape': u'https://ndownloader.figshare.com/files/5632173', u'PopulationAbunTransect': u'https://ndownloader.figshare.com/files/5632167', u'PopulationAbunMark_Recap': u'https://ndownloader.figshare.com/files/5632164'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/collections/Ten_years_of_abundance_data_within_a_spatial_population_network_of_the_alpine_butterfly_i_Parnassius_smintheus_i_/3307179",
                           retriever=True)