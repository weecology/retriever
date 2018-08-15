# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.1",
                           title="Effects of biodiversity on the functioning of ecosystems:A summary of 164 experimental manipulations of species richness",
                           citation="Bradley J. Cardinale, Diane S. Srivastava, J. Emmett Duffy, Justin P. Wright, Amy L. Downing, Mahesh Sankaran, Claire Jouseau, Marc W. Cadotte, Ian T. Carroll, Jerome J. Weis, Andy Hector, and Michel Loreau. 2009. Effects of biodiversity on the functioning of ecosystems:A summary of 164 experimental manipulations of species richness. Ecology 90:854.",
                           name="species-exctinction-rates",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'richness': u'https://ndownloader.figshare.com/files/5603117'},
                           keywords=[u'Taxon > Animals'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3530825",
                           description="A summary of the results on the accelerating rates of species extinction")