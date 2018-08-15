# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.1",
                           name="mapped-plant-quads-mt",
                           title="Mapped plant quadrat time-series from Montana (Anderson et al. 2011)",
                           citation="Jed Anderson, Lance Vermeire, and Peter B. Adler. 2011. Fourteen years of mapped, permanent quadrats in a northern mixed prairie, USA. Ecology 92:1703.",
                           retriever_minimum_version="2.0.dev",
                           tables={},
                           urls={u'allrecords_cover': u'https://ndownloader.figshare.com/files/5619447', u'allrecords_density': u'https://ndownloader.figshare.com/files/5619444', u'species_list': u'https://ndownloader.figshare.com/files/5619456'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3551799",
                           description="Long term plant quadrats of northern mixed prairie in Montana.")