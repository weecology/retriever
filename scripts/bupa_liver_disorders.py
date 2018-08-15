# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'bupa': Table('bupa', header_rows=0,columns=[(u'mcv', (u'int',)), (u'alkphos', (u'int',)), (u'sgpt', (u'int',)), (u'sqot', (u'int',)), (u'gammagt', (u'int',)), (u'drinks', (u'int',)), (u'selector', (u'int',))])},
                           version="1.0.0",
                           title="BUPA liver disorders",
                           citation="Richard S. Forsyth, 8 Grosvenor Avenue, Mapperley Park , Nottingham NG3 5DX, 0602-621676",
                           name="bupa-liver-disorders",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'bupa': u'https://archive.ics.uci.edu/ml/machine-learning-databases/liver-disorders/bupa.data'},
                           keywords=[u'bupa', u'liver', u'disorder', u'alcohol', u'consumption'],
                           retriever=True,
                           ref="https://archive.ics.uci.edu/ml/datasets/Liver+Disorders",
                           description="The first 5 variables are all blood tests which are thought to be sensitive to liver disorders that might arise from excessive alcohol consumption. Each line in the dataset constitutes the record of a single male individual. The 7th field (selector) has been widely misinterpreted in the past as a dependent variable representing presence or absence of a liver disorder. This is incorrect. The 7th field was created by BUPA researchers as a train/test selector. It is not suitable as a dependent variable for classification. The dataset does not contain any variable representing presence or absence of a liver disorder.")