# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'species': Table('species', columns=[(u'Year', (u'int',)), (u'Nest', (u'int',)), (u'Nest_date', (u'char',)), (u'SW_Vegetation', (u'double',)), (u'Clutch_Size', (u'int',)), (u'Nest_Predation', (u'int',)), (u'Nest_Survival', (u'int',)), (u'Live_Hatchlings', (u'int',))])},
                           version="1.0.2",
                           title="Nesting ecology and offspring recruitment in a long-lived turtle",
                           citation="Lisa E. Schwanz, Rachel M. Bowden, Ricky-John Spencer, and Fredric J. Janzen. 2009. Nesting ecology and offspring recruitment in a long-lived turtle. Ecology 90:1709. [https://doi.org/10.6084/m9.figshare.3531323.v1]",
                           name="turtle-offspring-nesting",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'species': u'https://ndownloader.figshare.com/files/5604044'},
                           keywords=[u'Taxon > Animals', u'demography', u'early life stages', u'fluctuating environments', u'maternal effects', u'nesting behavior', u'predation', u'temperature dependent sex determination', u'turtles'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3531323",
                           description="Valuable empirical resource for exploring important facets of nesting ecology and hatchling recruitment in a wild population of a long-lived species.")