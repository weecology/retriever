# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.1",
                           title="Barnacle, fucoid, and mussel recruitment in the Gulf of Maine, USA, from 1997 to 2007",
                           citation="Peter S. Petraitis, Harrison Liu, and Erika C. Rhile. 2009. Barnacle, fucoid, and mussel recruitment in the Gulf of Maine, USA, from 1997 to 2007. Ecology 90:571.",
                           name="marine-recruitment-data",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'plot_data': u'https://ndownloader.figshare.com/files/5602883'},
                           keywords=[u'Taxon > plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3530633",
                           description="This data set provides access to recruitment data collected in the experimental plots from 1997 to 2007")