# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.0.1",
                           title="3-D maps of tree canopy geometries at leaf scale",
                           citation="Hervé Sinoquet, Sylvain Pincebourde, Boris Adam, Nicolas Donès, Jessada Phattaralerphong, Didier Combes, Stéphane Ploquin, Krissada Sangsing, Poonpipope Kasemsap, Sornprach Thanisawanyangkura, Géraldine Groussier-Bout, and Jérôme Casas. 2009. 3-D maps of tree canopy geometries at leaf scale. Ecology 90:283",
                           name="tree-canopy-geometries",
                           retriever_minimum_version="2.0.0-dev",
                           urls={u'Apple': u'https://ndownloader.figshare.com/files/5602697', u'Walnut': u'https://ndownloader.figshare.com/files/5602715', u'Rubber1': u'https://ndownloader.figshare.com/files/5602709', u'Mango1': u'https://ndownloader.figshare.com/files/5602703', u'Mango2': u'https://ndownloader.figshare.com/files/5602706', u'Rubber2': u'https://ndownloader.figshare.com/files/5602712'},
                           keywords=[u'Taxon > plants'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3530507",
                           description="This data set reports the three-dimensional geometry of a set of fruit and rubber trees at the leaf scale")