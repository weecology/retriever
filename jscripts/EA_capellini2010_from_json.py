#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'MammalMR2010': Table('MammalMR2010', cleanup=Cleanup(correct_invalid_value, nulls=[-9999]))},
                           description='Data on basal metabolic rate (BMR) with experimental animal body mass, field metabolic rate (FMR) with wild animal body mass, and sources of the data. Ecological Archives E091-198-S1.',
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation='Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783-2793.',
                           urls={'MammalMR2010': 'http://www.esapubs.org/archive/ecol/E091/198/data.txt'},
                           shortname='MammalMR2010',
                           ref='http://www.esapubs.org/archive/ecol/E091/198/',
                           name='Phylogeny and metabolic rates in mammals (Ecological Archives 2010)')