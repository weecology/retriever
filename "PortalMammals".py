#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'main': Table('main', delimiter=',',cleanup=Cleanup(correct_invalid_value, nulls=['', None]),columns=[('recordid', ('pk-int',)), ('mo', ('int',)), ('dy', ('int',)), ('yr', ('int',)), ('period', ('int',)), ('plot', ('int',)), ('note1', ('char', '9')), ('stake', ('int',)), ('species', ('char', '9')), ('sex', ('char', '9')), ('age', ('char', '9')), ('reprod', ('char', '9')), ('testes', ('char', '9')), ('vagina', ('char', '9')), ('pregnant', ('char', '9')), ('nipples', ('char', '9')), ('lactation', ('char', '9')), ('hfl', ('int',)), ('wgt', ('int',)), ('tag', ('char', '9')), ('note2', ('char', '9')), ('ltag', ('char', '9')), ('note3', ('char', '9')), ('prevrt', ('char', '9')), ('prevlet', ('char', '9')), ('nestdir', ('char', '9')), ('neststk', ('char', '9')), ('note4', ('char', '9')), ('note5', ('char', '9'))],contains_pk=True)},
                           description="The data set represents a Desert ecosystems using the composition and abundances of ants, plants, and rodents has occurred continuously on 24 plots.",
                           tags=['Taxon > Mammals', 'Biome > Desert', 'Data Type > Time Series', 'Data Type > Experimental'],
                           scan_lines=40000,
                           citation="S. K. Morgan Ernest, Thomas J. Valone, and James H. Brown. 2009. Long-term monitoring and experimental manipulation of a Chihuahuan Desert ecosystem near Portal, Arizona, USA. Ecology 90:1708.",
                           urls={'plots': 'https://ndownloader.figshare.com/files/3299474', 'main': 'http://esapubs.org/archive/ecol/E090/118/Portal_rodents_19772002.csv', 'species': 'https://ndownloader.figshare.com/files/3299483'},
                           shortname="PortalMammals",
                           ref="http://esapubs.org/archive/ecol/E090/118/",
                           name="Portal Project Mammals (Ecological Archives 2009)")