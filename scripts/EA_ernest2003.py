from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={},
                           name="Mammal Life History Database - Ernest, et al., 2003",
                           tags=['Animals', 'Mammals'],
                           urls={'species': 'http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt'},
                           shortname="MammalLH",
                           description="S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.")