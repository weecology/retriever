# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'data': Table('data', header_rows=0,columns=[(u'Sex', (u'char',)), (u'Length', (u'double',)), (u'Diameter', (u'double',)), (u'Height', (u'double',)), (u'Whole_Weight', (u'double',)), (u'Shucked_weight', (u'double',)), (u'Viscera_weight', (u'double',)), (u'Shell_weight', (u'double',)), (u'Rings', (u'int',))])},
                           version="1.2.2",
                           title="Abalone Age and Size Data",
                           citation="Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.",
                           name="abalone-age",
                           retriever_minimum_version="2.0.dev",
                           urls={u'data': u'http://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'},
                           keywords=[],
                           retriever=True,
                           ref="http://archive.ics.uci.edu/ml/datasets/Abalone",
                           description="Database to aid in the prediction of the age of an Abalone given physical measurements")