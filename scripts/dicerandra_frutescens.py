# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.2",
                           description="Study of the demography of Dicerandra frutescens, an endemic and endangered mint restricted to Florida scrub",
                           title="Demography of the endemic mint Dicerandra frutescens in Florida scrub",
                           citation="Eric S. Menges. 2008. Demography of the endemic mint Dicerandra frutescens in Florida scrub. Ecology 89:1474.",
                           name="dicerandra-frutescens",
                           keywords=[u'Taxon > plants'],
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'populations': u'https://ndownloader.figshare.com/files/5601455'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3529460",
                           retriever=True)