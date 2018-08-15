# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'fronds': Table('fronds', nulls=[u'-99999'])},
                           version="1.0.1",
                           title="The data was used to investigate patterns and causes of variation in NPP by the giant kelp, Macrocystis pyrifera, which is believed to be one of the fastest growing autotrophs on earth.",
                           citation="Andrew Rassweiler, Katie K. Arkema, Daniel C. Reed, Richard C. Zimmerman, and Mark A. Brzezinski. 2008. Net primary production, growth, and standing crop of Macrocystis pyrifera in southern California. Ecology 89:2068.",
                           name="macrocystis-variation",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'fronds': u'https://ndownloader.figshare.com/files/5601737', u'production': u'https://ndownloader.figshare.com/files/5601731', u'density': u'https://ndownloader.figshare.com/files/5601734'},
                           keywords=[u'Taxon > plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3529700",
                           description="")