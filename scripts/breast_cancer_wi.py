# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'wpbc': Table('wpbc', delimiter=',',header_rows=0,columns=[(u'ID', (u'int',)), (u'Outcome', (u'char',)), (u'Time', (u'int',)), (u'radius', (u'double',)), (u'texture', (u'double',)), (u'perimeter', (u'double',)), (u'area', (u'double',)), (u'smoothness', (u'double',)), (u'compactness', (u'double',)), (u'concavity', (u'double',)), (u'concave_points', (u'double',)), (u'symmetry', (u'double',)), (u'fractal_dimension', (u'double',))]),'wdbc': Table('wdbc', delimiter=',',header_rows=0,columns=[(u'ID', (u'int',)), (u'Diagnosis', (u'char',)), (u'radius', (u'double',)), (u'texture', (u'double',)), (u'perimeter', (u'double',)), (u'area', (u'double',)), (u'smoothness', (u'double',)), (u'compactness', (u'double',)), (u'concavity', (u'double',)), (u'concave_points', (u'double',)), (u'symmetry', (u'double',)), (u'fractal_dimension', (u'double',))]),'breastCancerWisconsin': Table('breastCancerWisconsin', delimiter=',',cleanup=Cleanup(correct_invalid_value, missing_values=[u'?']),header_rows=0,columns=[(u'Sample_Code_Number', (u'int',)), (u'Clump_Thickness', (u'int',)), (u'Uniformity_of_Cell_Size', (u'int',)), (u'Uniformity_of_Cell_Shape', (u'int',)), (u'Marginal_Adhesion', (u'int',)), (u'Single_Epithelial_Cell_Size', (u'int',)), (u'Bare_Nuclei', (u'int',)), (u'Bland_Chromatin', (u'int',)), (u'Normal_Nucleoli', (u'int',)), (u'Mitoses', (u'int',)), (u'Class', (u'int',))])},
                           version="1.2.2",
                           title="Wisconsin Breast Cancer Database",
                           citation="Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.",
                           name="breast-cancer-wi",
                           retriever_minimum_version="2.0.dev",
                           urls={u'wpbc': u'http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wpbc.data', u'wdbc': u'http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data', u'breastCancerWisconsin': u'http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data'},
                           keywords=[u'cancer', u'health', u'disease', u'medicine'],
                           retriever=True,
                           ref="http://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29",
                           description="Database containing information on Wisconsin Breast Cancer Diagnostics")