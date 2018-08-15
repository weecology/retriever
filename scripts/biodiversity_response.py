# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.2",
                           description="",
                           title="The effects of biodiversity on ecosystem community, and population variables reported 1974-2004",
                           citation="Bernhard Schmid, Andrea B. Pfisterer, and Patricia Balvanera. 2009. Effects of biodiversity on ecosystem community, and population variables reported 1974-2004. Ecology 90:853",
                           name="biodiversity-response",
                           keywords=[u'Taxon > plants'],
                           retriever_minimum_version="2.0.dev",
                           tables={},
                           urls={u'population_response': u'https://ndownloader.figshare.com/files/5603108'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3530822",
                           retriever=True)