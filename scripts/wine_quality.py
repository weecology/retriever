# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'white': Table('white', header_rows=1,columns=[(u'fixed_acidity', (u'double',)), (u'volatile_acidity', (u'double',)), (u'citric_acid', (u'double',)), (u'residual_sugar', (u'double',)), (u'chlorides', (u'double',)), (u'free_sulfur_dioxide', (u'int',)), (u'total_sulfur_dioxide', (u'int',)), (u'density', (u'double',)), (u'pH', (u'double',)), (u'sulphates', (u'double',)), (u'alcohol', (u'double',)), (u'quality', (u'int',))]),'red': Table('red', header_rows=1,columns=[(u'fixed_acidity', (u'double',)), (u'volatile_acidity', (u'double',)), (u'citric_acid', (u'double',)), (u'residual_sugar', (u'double',)), (u'chlorides', (u'double',)), (u'free_sulfur_dioxide', (u'int',)), (u'total_sulfur_dioxide', (u'int',)), (u'density', (u'double',)), (u'pH', (u'double',)), (u'sulphates', (u'double',)), (u'alcohol', (u'double',)), (u'quality', (u'int',))])},
                           version="1.1.2",
                           title="Wine Quality",
                           citation="P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.",
                           name="wine-quality",
                           retriever_minimum_version="2.0.dev",
                           urls={u'white': u'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv', u'red': u'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'},
                           keywords=[u'wine', u'alcohol'],
                           retriever=True,
                           ref="Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.http://archive.ics.uci.edu/ml/datasets/Wine+Quality",
                           description="Two datasets are included, related to red and white vinho verde wine samples, from the north of Portugal. The goal is to model wine quality based on physicochemical tests")