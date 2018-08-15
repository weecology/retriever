# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.3",
                           name="community-abundance-misc",
                           title="Miscellaneous Abundance Database (figshare 2012)",
                           citation="Baldridge, Elita, A Data-intensive Assessment of the Species Abundance Distribution(2013). All Graduate Theses and Dissertations. Paper 4276.",
                           retriever_minimum_version="2.0.dev",
                           tables={},
                           urls={u'citations': u'http://files.figshare.com/2023506/Citations_table_abundances.csv', u'main': u'http://files.figshare.com/2023547/Species_abundances.csv', u'sites': u'http://files.figshare.com/2023504/Sites_table_abundances.csv'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           retriever=True,
                           description="Community abundance data for fish, reptiles, amphibians, beetles, spiders, and birds, compiled from the literature by Elita Baldridge.")