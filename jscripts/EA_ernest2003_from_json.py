#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description='The purpose of this data set was to compile general life history characteristics for a variety of mammalian species to perform comparative life history analyses among different taxa and different body size groups.',
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation='S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.',
                           urls={'species': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt'},
                           shortname='MammalLH',
                           ref='http://esapubs.org/archive/ecol/E084/093/',
                           name='Mammal Life History Database - Ernest, et al., 2003')