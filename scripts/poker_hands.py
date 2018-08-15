# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'training': Table('training', header_rows=0,columns=[(u'S1', (u'int',)), (u'C1', (u'int',)), (u'S2', (u'int',)), (u'C2', (u'int',)), (u'S3', (u'int',)), (u'C3', (u'int',)), (u'S4', (u'int',)), (u'C4', (u'int',)), (u'S5', (u'int',)), (u'C5', (u'int',)), (u'Class', (u'int',))]),'testing': Table('testing', header_rows=0,columns=[(u'S1', (u'int',)), (u'C1', (u'int',)), (u'S2', (u'int',)), (u'C2', (u'int',)), (u'S3', (u'int',)), (u'C3', (u'int',)), (u'S4', (u'int',)), (u'C4', (u'int',)), (u'S5', (u'int',)), (u'C5', (u'int',)), (u'Class', (u'int',))])},
                           version="1.2.2",
                           title="Poker Hand dataset",
                           citation="Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.",
                           name="poker-hands",
                           retriever_minimum_version="2.0.dev",
                           urls={u'training': u'http://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-training-true.data', u'testing': u'http://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-testing.data'},
                           keywords=[u'games', u'poker'],
                           retriever=True,
                           ref="http://archive.ics.uci.edu/ml/datasets/Poker+Hand",
                           description="A dataset used to predict poker hands")