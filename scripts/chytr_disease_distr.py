# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.2",
                           title="The distribution and host range of the pandemic disease chytridiomycosis in Australia, spanning surveys from 1956-2007.",
                           citation="Kris Murray, Richard Retallick, Keith R. McDonald, Diana Mendez, Ken Aplin, Peter Kirkpatrick, Lee Berger, David Hunter, Harry B. Hines, R. Campbell, Matthew Pauza, Michael Driessen, Richard Speare, Stephen J. Richards, Michael Mahony, Alastair Freeman, Andrea D. Phillott, Jean-Marc Hero, Kerry Kriger, Don Driscoll, Adam Felton, Robert Puschendorf, and Lee F. Skerratt. 2010. The distribution and host range of the pandemic disease chytridiomycosis in Australia, spanning surveys from 1956-2007. Ecology 91:1557.",
                           name="chytr-disease-distr",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'Chytridiomycosis_data': u'https://ndownloader.figshare.com/files/5613237'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3547077",
                           description="The data is of a distribution and host range of this invasive disease in Australia")