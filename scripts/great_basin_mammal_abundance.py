# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.1",
                           name="great-basin-mammal-abundance",
                           title="Mammal abundance indices in the northern portion of the Great Basin",
                           citation="Rebecca A. Bartel, Frederick F. Knowlton, and Charles Stoddart. 2005. Mammal abundance indices in the northern portion of the Great Basin, 1962-1993. Ecology 86:3130.",
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'Mammal_abundance': u'https://ndownloader.figshare.com/files/5596343'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3525485",
                           description="Indices of abundance of selected mammals obtained for two study areas within the Great Basin.")