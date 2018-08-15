# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'gdp': Table('gdp', columns=[(u'Country Name', (u'char',)), (u'Country Code', (u'char',)), (u'Year', (u'double',)), (u'Value', (u'double',))],do_not_bulk_insert=False)},
                           version="1.0.2",
                           title="GDP Data",
                           citation="NA",
                           name="gdp",
                           retriever_minimum_version="2.0.dev",
                           urls={u'gdp': u'https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv'},
                           keywords=[u'GDP', u'World', u'Gross Domestic Product', u'Time Series'],
                           retriever=True,
                           ref="https://github.com/datasets/gdp/blob/master",
                           description="Country, regional and world GDP in current US Dollars ($). Regional means collections of countries e.g. Europe & Central Asia. Data is sourced from the World Bank and turned into a standard normalized CSV.")