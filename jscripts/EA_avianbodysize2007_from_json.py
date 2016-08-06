#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'species': Table('species', cleanup=Cleanup(correct_invalid_value, nulls=[-999]))},
                           description='A comprehensive compilation of data set on avian body sizes that would be useful for future comparative studies of avian biology.',
                           tags=['Taxon > Birds', 'Data Type > Compilation'],
                           citation='Terje Lislevand, Jordi Figuerola, and Tamas Szekely. 2007. Avian body sizes in relation to fecundity, mating system, display behavior, and resource sharing. Ecology 88:1605.',
                           urls={'species': 'http://esapubs.org/archive/ecol/E088/096/avian_ssd_jan07.txt'},
                           shortname='AvianBodySize',
                           ref='http://esapubs.org/archive/ecol/E088/096/',
                           name='Avian Body Size Ecological Archives 2007')