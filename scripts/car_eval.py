# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'data': Table('data', delimiter=',',header_rows=0,columns=[(u'buying', (u'char',)), (u'maint', (u'char',)), (u'doors', (u'char',)), (u'persons', (u'char',)), (u'lug_boot', (u'char',)), (u'safety', (u'char',))])},
                           version="1.1.2",
                           title="Car Evaluation",
                           citation="Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.",
                           name="car-eval",
                           retriever_minimum_version="2.0.dev",
                           urls={u'data': u'http://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data'},
                           keywords=[u'categorical', u'multivariate'],
                           retriever=True,
                           ref="http://archive.ics.uci.edu/ml/datasets/Car+Evaluation",
                           description="A database useful for testing constructive induction and structure discovery methods.")