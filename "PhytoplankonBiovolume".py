#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'bvd_raw': Table('bvd_raw', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'taxa_table': Table('taxa_table', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'bvd_species_ag': Table('bvd_species_ag', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'bvd_genus_raw': Table('bvd_genus_raw', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'bvd_genus_ag': Table('bvd_genus_ag', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'bvd_species_raw': Table('bvd_species_raw', cleanup=Cleanup(correct_invalid_value, nulls=['NA']))},
                           description="Sampling phytoplankton communities basing on cell size.",
                           tags=['Taxon > Phytoplankton', 'Data Type > Compilation'],
                           citation="Colin T. Kremer, Jacob P. Gillette, Lars G. Rudstam, Pal Brettum, and Robert Ptacnik. 2014. A compendium of cell and natural unit biovolumes for >1200 freshwater phytoplankton species. Ecology 95:2984.",
                           urls={'bvd_raw': 'http://esapubs.org/archive/ecol/E095/257/bvd_raw_052814.csv', 'taxa_table': 'http://esapubs.org/archive/ecol/E095/257/taxa_table_030614.csv', 'bvd_species_ag': 'http://esapubs.org/archive/ecol/E095/257/bvd_species_ag_030614.csv', 'bvd_genus_raw': 'http://esapubs.org/archive/ecol/E095/257/bvd_genus_raw_030614.csv', 'bvd_genus_ag': 'http://esapubs.org/archive/ecol/E095/257/bvd_genus_ag_030614.csv', 'bvd_species_raw': 'http://esapubs.org/archive/ecol/E095/257/bvd_species_raw_030614.csv'},
                           shortname="PhytoplankonBiovolume",
                           ref="http://www.esapubs.org/archive/ecol/E095/257/",
                           name="Biovolumes for freshwater phytoplankton - Colin et al. 2014")