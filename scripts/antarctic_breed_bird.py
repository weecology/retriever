# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.2",
                           description="The data set represents the accumulation of 19 years of seabird population abundance data which was collected by the Antarctic Site Inventory, an opportunistic vessel-based monitoring program surveying the Antarctic Peninsula and associated sub-Antarctic Islands.",
                           title="Antarctic Site Inventory breeding bird survey data, 1994-2013",
                           citation="Heather J. Lynch, Ron Naveen, and Paula Casanovas. 2013. Antarctic Site Inventory breeding bird survey data, 1994-2013. Ecology 94:2653.",
                           name="antarctic-breed-bird",
                           keywords=[u'birds'],
                           retriever_minimum_version="2.0.dev",
                           tables={},
                           urls={u'species': u'https://ndownloader.figshare.com/files/5628465'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/collections/Antarctic_Site_Inventory_breeding_bird_survey_data_1994_2013/3306315",
                           retriever=True)