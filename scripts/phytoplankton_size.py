# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'bvd_raw': Table('bvd_raw', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'taxa_table': Table('taxa_table', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'bvd_species_ag': Table('bvd_species_ag', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'bvd_genus_raw': Table('bvd_genus_raw', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'bvd_genus_ag': Table('bvd_genus_ag', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'bvd_species_raw': Table('bvd_species_raw', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']))},
                           version="1.2.1",
                           title="Biovolumes for freshwater phytoplankton - Colin et al. 2014",
                           citation="Colin T. Kremer, Jacob P. Gillette, Lars G. Rudstam, Pal Brettum, and Robert Ptacnik. 2014. A compendium of cell and natural unit biovolumes for >1200 freshwater phytoplankton species. Ecology 95:2984.",
                           name="phytoplankton-size",
                           retriever_minimum_version="2.0.dev",
                           urls={u'bvd_raw': u'https://ndownloader.figshare.com/files/5632146', u'taxa_table': u'https://ndownloader.figshare.com/files/5632155', u'bvd_species_ag': u'https://ndownloader.figshare.com/files/5632149', u'bvd_genus_raw': u'https://ndownloader.figshare.com/files/5632143', u'bvd_genus_ag': u'https://ndownloader.figshare.com/files/5632140', u'bvd_species_raw': u'https://ndownloader.figshare.com/files/5632152'},
                           keywords=[u'phytoplankton', u'literature-compilation', u'size'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3560628",
                           description="Sampling phytoplankton communities basing on cell size.")