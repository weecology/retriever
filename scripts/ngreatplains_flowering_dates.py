# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.2",
                           title="First-flowering dates of plants in the Northern Great Plains",
                           citation="Steven E. Travers and Kelsey L. Dunnell. 2009. First-flowering dates of plants in the Northern Great Plains. Ecology 90:2332.",
                           name="ngreatplains-flowering-dates",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'observations': u'https://ndownloader.figshare.com/files/5604587'},
                           keywords=[u'Taxon > Plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3531716",
                           description="Observations data of first-flowering time of native and nonnative plant species in North Dakota and Minnesota over the course of 51 years in the last century")