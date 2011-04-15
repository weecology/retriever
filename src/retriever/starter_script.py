"""Starter EcoData Retriever Script"""

from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'

name = "ENTER AN ~5-10 WORD NAME FOR THE DATASET IN PLACE OF THIS TEXT"
description = "ENTER A BRIEF DESCRIPTION OF THIS DATASET IN PLACE OF THIS TEXT"
shortname = "ENTER SHORT NAME OF ~10 CHARACTERS FOR THE DATASET IN PLACE OF THIS TEXT"

#Enter a list of urls, one for each table to be included in the database. If
#there is more than one table then separate them using commas
urls = {"ENTER_TABLE_NAME_HERE":"http://URL_HERE",
        "ANOTHER_TABLE_NAME_HERE":"http://ANOTHER_URL_HERE"}

SCRIPT = BasicTextTemplate(name=name, description=description,
                           shortname=shortname, urls=urls)