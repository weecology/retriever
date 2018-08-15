# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'WineComposition': Table('WineComposition', delimiter=',',header_rows=0,columns=[(u'Alcohol', (u'int',)), (u'Malic_Acid', (u'double',)), (u'Ash', (u'double',)), (u'Alcalinity_of_Ash', (u'double',)), (u'Magnesium', (u'double',)), (u'Total_phenols', (u'double',)), (u'Flavanoids', (u'double',)), (u'Nonflavanoid_phenols', (u'double',)), (u'Proanthocyanins', (u'double',)), (u'Color_Intensity', (u'double',)), (u'Hue', (u'double',)), (u'OD280/OD315_of_Diluted_Wines', (u'double',)), (u'Proline', (u'int',))])},
                           description="A chemical analysis of wines grown in the same region in Italy but derived from three different cultivators.",
                           title="Wine Composition",
                           citation="Forina, M. et al, PARVUS - An Extendible Package for Data",
                           name="wine-composition",
                           version="1.1.1",
                           urls={u'WineComposition': u'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'},
                           keywords=[u'wine', u'alcohol'],
                           ref="Exploration, Classification and Correlation. Institute of Pharmaceutical",
                           retriever=True)