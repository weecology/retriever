# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.2.1",
                           title="Mammal Life History Database - Ernest, et al., 2003",
                           citation="S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
                           name="mammal-life-hist",
                           retriever_minimum_version="2.0.dev",
                           urls={u'species': u'https://ndownloader.figshare.com/files/5593334'},
                           keywords=[u'mammals', u'literature-compilation', u'life-history'],
                           retriever=True,
                           ref="https://figshare.com/collections/LIFE_HISTORY_CHARACTERISTICS_OF_PLACENTAL_NONVOLANT_MAMMALS/3297992",
                           description="The purpose of this data set was to compile general life history characteristics for a variety of mammalian species to perform comparative life history analyses among different taxa and different body size groups.")