# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.1",
                           name="macroalgal_communities",
                           title="species data on densities and percent cover in the 60 experimental plots from 1996 to 2002",
                           citation="Peter S. Petraitis and Nicholas Vidargas. 2006. Marine intertidal organisms found in experimental clearings on sheltered shores in the Gulf of Maine, USA. Ecology 87:796.",
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'Mammal_abundance': u'https://ndownloader.figshare.com/files/5596982'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3526004",
                           description="Experimental clearings in macroalgal stands were established in 1996 to determine if mussel beds and macroalgal stands on protected intertidal shores of New England represent alternative community states")