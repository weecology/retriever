# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'Iris': Table('Iris', delimiter=',',header_rows=0,columns=[(u'sepal_length', (u'double',)), (u'sepal_width', (u'double',)), (u'petal_length', (u'double',)), (u'petal_width', (u'double',)), (u'class', (u'char', u'20'))])},
                           version="1.2.1",
                           title="Iris Plants Database",
                           citation="R. A. Fisher. 1936. The Use of Multiple Measurements in Taxonomic Problems. and Asuncion, A. & Newman, D.J. (2007). UCI Machine Learning Repository [http://www.ics.uci.edu/~mlearn/MLRepository.html]. Irvine, CA: University of California, School of Information and Computer Science.",
                           name="iris",
                           retriever_minimum_version="2.0.dev",
                           urls={u'Iris': u'http://mlr.cs.umass.edu/ml/machine-learning-databases/iris/bezdekIris.data'},
                           keywords=[u'plants', u'literature-compilation', u'categorical'],
                           retriever=True,
                           ref="http://mlr.cs.umass.edu/ml/datasets/Iris",
                           description="Famous dataset from R. A. Fisher. This dataset has been corrected. Information Source: Asuncion, A. & Newman, D.J. (2007). UCI Machine Learning Repository [http://www.ics.uci.edu/~mlearn/MLRepository.html]. Irvine, CA: University of California, School of Information and Computer Science.")