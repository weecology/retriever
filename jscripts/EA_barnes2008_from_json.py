#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'main': Table('main', cleanup=Cleanup(correct_invalid_value, nulls=['n/a', '0.0000E+00']))},
                           description='The data set contians relationships between predator and prey size which are needed to describe interactions of species and size classes in food webs.',
                           tags=['Taxon > Fish', 'Data Type > Compilation'],
                           citation='C. Barnes, D. M. Bethea, R. D. Brodeur, J. Spitz, V. Ridoux, C. Pusineri, B. C. Chase, M. E. Hunsicker, F. Juanes, A. Kellermann, J. Lancaster, F. Menard, F.-X. Bard, P. Munk, J. K. Pinnegar, F. S. Scharf, R. A. Rountree, K. I. Stergiou, C. Sassa, A. Sabates, and S. Jennings. 2008. Predator and prey body sizes in marine food webs. Ecology 89:881.',
                           urls={'main': 'http://www.esapubs.org/Archive/ecol/E089/051/Predator_and_prey_body_sizes_in_marine_food_webs_vsn3.txt'},
                           shortname='MarineSize',
                           ref='http://www.esapubs.org/Archive/ecol/E089/051/',
                           name='Marine Predator and Prey Body Sizes (Ecological Archives 2008)')