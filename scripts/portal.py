# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.1",
                           description="The data set represents a Desert ecosystems using the composition and abundances of ants, plants, and rodents has occurred continuously on 24 plots. Currently includes only mammal data.",
                           title="Portal Project Data (Ernest et al. 2009)",
                           scan_lines=40000,
                           citation="S. K. Morgan Ernest, Thomas J. Valone, and James H. Brown. 2009. Long-term monitoring and experimental manipulation of a Chihuahuan Desert ecosystem near Portal, Arizona, USA. Ecology 90:1708.",
                           name="portal",
                           retriever_minimum_version="2.0.dev",
                           tables={'main': Table('main', delimiter=',',cleanup=Cleanup(correct_invalid_value, missing_values=[u'', None]),columns=[(u'recordid', (u'pk-int',)), (u'mo', (u'int',)), (u'dy', (u'int',)), (u'yr', (u'int',)), (u'period', (u'int',)), (u'plot', (u'int',)), (u'note1', (u'char', u'9')), (u'stake', (u'int',)), (u'species', (u'char', u'9')), (u'sex', (u'char', u'9')), (u'age', (u'char', u'9')), (u'reprod', (u'char', u'9')), (u'testes', (u'char', u'9')), (u'vagina', (u'char', u'9')), (u'pregnant', (u'char', u'9')), (u'nipples', (u'char', u'9')), (u'lactation', (u'char', u'9')), (u'hfl', (u'int',)), (u'wgt', (u'int',)), (u'tag', (u'char', u'9')), (u'note2', (u'char', u'9')), (u'ltag', (u'char', u'9')), (u'note3', (u'char', u'9')), (u'prevrt', (u'char', u'9')), (u'prevlet', (u'char', u'9')), (u'nestdir', (u'char', u'9')), (u'neststk', (u'char', u'9')), (u'note4', (u'char', u'9')), (u'note5', (u'char', u'9'))],contains_pk=True)},
                           urls={u'plots': u'https://ndownloader.figshare.com/files/3299474', u'main': u'https://ndownloader.figshare.com/files/5603981', u'species': u'https://ndownloader.figshare.com/files/3299483'},
                           keywords=[u'mammals', u'desert', u'time-series', u'experimental', u'observational'],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3531317",
                           retriever=True)