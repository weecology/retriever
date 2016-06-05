#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description='spatially explicit measurements of population level leaf herbivory on 1145 species of vascular plants from 189 studies from across the globe.',
                           tags=['Taxon > Plants'],
                           citation='Martin M. Turcotte, Christina J. M. Thomsen, Geoffrey T. Broadhead, Paul V. A. Fine, Ryan M. Godfrey, Greg P. A. Lamarre, Sebastian T. Meyer, Lora A. Richards, and Marc T. J. Johnson. 2014. Percentage leaf herbivory across vascular plant species. Ecology 95:788. http://dx.doi.org/10.1890/13-1741.1.',
                           urls={'Leaf_herbivory': 'http://www.esapubs.org/archive/ecol/E095/065/Leaf_herbivory.csv'},
                           shortname='leaf_herbivory',
                           name='Leaf herbivory dataset')