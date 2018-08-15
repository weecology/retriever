# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.2.1",
                           title="Vascular plant composition - McGlinn, et al., 2010",
                           citation="Daniel J. McGlinn, Peter G. Earls, and Michael W. Palmer. 2010. A 12-year study on the scaling of vascular plant composition in an Oklahoma tallgrass prairie. Ecology 91:1872.",
                           name="plant-comp-ok",
                           retriever_minimum_version="2.0.dev",
                           urls={u'climate': u'https://ndownloader.figshare.com/files/5613450', u'richness': u'https://ndownloader.figshare.com/files/5613441', u'cover': u'https://ndownloader.figshare.com/files/5613438', u'environment': u'https://ndownloader.figshare.com/files/5613447', u'species': u'https://ndownloader.figshare.com/files/5613444', u'pres': u'https://ndownloader.figshare.com/files/5613435'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3547209",
                           description="The data is part of a monitoring project on vascular plant composition at the Tallgrass Prairie Preserve in Osage County, Oklahoma, USA.")