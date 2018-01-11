# -*- coding: utf-8  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'gdp': Table('gdp', columns=[(u'Country Name', (u'char',)), (u'Country Code', (u'char',)), (u'Year 1961', (u'double',)), (u'Year 1962', (u'double',)), (u'Year 1963', (u'double',)), (u'Year 1964', (u'double',)), (u'Year 1965', (u'double',)), (u'Year 1966', (u'double',)), (u'Year 1967', (u'double',)), (u'Year 1968', (u'double',)), (u'Year 1969', (u'double',)), (u'Year 1970', (u'double',)), (u'Year 1971', (u'double',)), (u'Year 1972', (u'double',)), (u'Year 1973', (u'double',)), (u'Year 1974', (u'double',)), (u'Year 1975', (u'double',)), (u'Year 1976', (u'double',)), (u'Year 1977', (u'double',)), (u'Year 1978', (u'double',)), (u'Year 1979', (u'double',)), (u'Year 1980', (u'double',)), (u'Year 1981', (u'double',)), (u'Year 1982', (u'double',)), (u'Year 1983', (u'double',)), (u'Year 1984', (u'double',)), (u'Year 1985', (u'double',)), (u'Year 1986', (u'double',)), (u'Year 1987', (u'double',)), (u'Year 1988', (u'double',)), (u'Year 1989', (u'double',)), (u'Year 1990', (u'double',)), (u'Year 1991', (u'double',)), (u'Year 1991', (u'double',)), (u'Year 1992', (u'double',)), (u'Year 1993', (u'double',)), (u'Year 1994', (u'double',)), (u'Year 1995', (u'double',)), (u'Year 1996', (u'double',)), (u'Year 1997', (u'double',)), (u'Year 1998', (u'double',)), (u'Year 1999', (u'double',)), (u'Year 2000', (u'double',)), (u'Year 2001', (u'double',)), (u'Year 2002', (u'double',)), (u'Year 2003', (u'double',)), (u'Year 2004', (u'double',)), (u'Year 2004', (u'double',)), (u'Year 2005', (u'double',)), (u'Year 2006', (u'double',)), (u'Year 2007', (u'double',)), (u'Year 2008', (u'double',)), (u'Year 2009', (u'double',)), (u'Year 2010', (u'double',)), (u'Year 2011', (u'double',)), (u'Year 2012', (u'double',)), (u'Year 2013', (u'double',)), (u'Year 2014', (u'double',)), (u'Year 2015', (u'double',)), (u'Year 2016', (u'double',)), (u'Year 2017', (u'double',))],do_not_bulk_insert=False)},
                           version="1.0.0",
                           encoding="UTF-8",
                           citation="NA",
                           name="gdp",
                           retriever_minimum_version="2.0.dev",
                           urls={u'gdp': u'http://api.worldbank.org/indicator/NY.GDP.MKTP.CD?format=csv'},
                           keywords=[u'GDP', u'World', u'Gross Domestic Product', u'Time Series'],
                           title="GDP Data",
                           retriever=True,
                           ref="https://github.com/datasets/gdp/blob/master",
                           description="Country, regional and world GDP in current US Dollars ($). Regional means collections of countries e.g. Europe & Central Asia. Data is sourced from the World Bank and turned into a standard normalized CSV.")
