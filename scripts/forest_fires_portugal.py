# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'data': Table('data', header_rows=1,columns=[(u'X', (u'int',)), (u'Y', (u'int',)), (u'month', (u'char',)), (u'day', (u'char',)), (u'FFMC', (u'double',)), (u'DC', (u'double',)), (u'ISI', (u'double',)), (u'temp', (u'double',)), (u'RH', (u'double',)), (u'wind', (u'double',)), (u'rain', (u'double',)), (u'area', (u'double',))])},
                           version="1.1.4",
                           title="Forest fire data for Montesinho natural park in Portugal",
                           citation="P. Cortez and A. Morais. A Data Mining Approach to Predict Forest Fires using Meteorological Data. In J. Neves, M. F. Santos and J. Machado Eds., New Trends in Artificial Intelligence, Proceedings of the 13th EPIA 2007 - Portuguese Conference on Artificial Intelligence, December, Guimaraes, Portugal, pp. 512-523, 2007. APPIA, ISBN-13 978-989-95618-0-9.",
                           name="forest-fires-portugal",
                           retriever_minimum_version="2.0.dev",
                           urls={u'data': u'http://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv'},
                           keywords=[],
                           retriever=True,
                           ref="http://archive.ics.uci.edu/ml/datasets/Forest+Fires",
                           description="A database for regression analysis with the aim of predicting burned areas of forestry using meteorological and other data.")