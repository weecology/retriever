# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.1",
                           title="Fire-related traits for plant species of the Mediterranean Basin. Ecology 90:1420",
                           citation="S. Paula, M. Arianoutsou, D. Kazanis, Ç. Tavsanoglu, F. Lloret, C. Buhk, F. Ojeda, B. Luna, J. M. Moreno, A. Rodrigo, J. M. Espelta, S. Palacio, B. Fernández-Santos,, P. M. Fernandes, and J. G. Pausas. 2009. Fire-related traits for plant species of the Mediterranean Basin. Ecology 90:1420.",
                           name="mediter-basin-plant-traits",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'species': u'https://ndownloader.figshare.com/files/5603675'},
                           keywords=[u'Taxon > Plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3531092",
                           description="This data set compiles the most updated and comprehensive information on fire-related traits for vascular plant species of the Mediterranean Basin")