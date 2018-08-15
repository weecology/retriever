# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.1",
                           title="Nematode traits and environmental constraints in 200 soil systems",
                           citation="Christian Mulder and J. Arie Vonk. 2011. Nematode traits and environmental constraints in 200 soil systems:scaling within the 60–6000 µm body size range. Ecology 92:2004.",
                           name="nematode-traits",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'Trait': u'https://ndownloader.figshare.com/files/5620305', u'Dutchagroecosystems': u'https://ndownloader.figshare.com/files/5620302'},
                           keywords=[u'Taxon > Plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3552057",
                           description="This data set includes information on taxonomy, life stage, sex, feeding habit, trophic level, geographic location, sampling period, ecosystem type, soil type, and soil chemistry")