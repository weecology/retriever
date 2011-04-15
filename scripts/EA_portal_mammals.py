from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'plots': Table('plots', delimiter=',',columns=[('PlotID', ('pk-auto',)), ('PlotTypeAlphaCode', ('char', '2')), ('PlotTypeNumCode', ('int',)), ('PlotTypeDescript', ('char', '3'))],header_rows=0,contains_pk=True),'main': Table('main', cleanup=Cleanup(correct_invalid_value, nulls=[None]))},
                           name="Portal Project Mammals (Ecological Archives 2009)",
                           tags=['Animals', 'Mammals'],
                           ref="http://esapubs.org/archive/ecol/E090/118/",
                           urls={'plots': 'http://wiki.ecologicaldata.org/sites/default/files/portal_plots.txt', 'main': 'http://esapubs.org/archive/ecol/E090/118/Portal_rodents_19772002.csv', 'species': 'http://wiki.ecologicaldata.org/sites/default/files/portal_species.txt'},
                           shortname="PortalMammals",
                           description="S. K. Morgan Ernest, Thomas J. Valone, and James H. Brown. 2009. Long-term monitoring and experimental manipulation of a Chihuahuan Desert ecosystem near Portal, Arizona, USA. Ecology 90:1708.")