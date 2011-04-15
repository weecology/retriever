from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={},
                           name="Avian Body Size (Ecological Archives 2007)",
                           tags=['Animals', 'Birds'],
                           urls={'species': 'http://esapubs.org/archive/ecol/E088/096/avian_ssd_jan07.txt'},
                           shortname="AvianBodySize",
                           description="Terje Lislevand, Jordi Figuerola, and Tamas Szekely. 2007. Avian body sizes in relation to fecundity, mating system, display behavior, and resource sharing. Ecology 88:1605.")