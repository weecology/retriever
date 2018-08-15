# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.0.1",
                           name="streamflow-conditions",
                           title="A stream gage database for evaluating natural and altered flow conditions in the conterminous United States.",
                           citation="James A. Falcone, Daren M. Carlisle, David M. Wolock, and Michael R. Meador. 2010. GAGES:A stream gage database for evaluating natural and altered flow conditions in the conterminous United States. Ecology 91:621.",
                           retriever_minimum_version="2.0.0-dev",
                           tables={},
                           urls={u'nutrient_app': u'https://ndownloader.figshare.com/files/5608622', u'pest_app': u'https://ndownloader.figshare.com/files/5608625', u'lc01_mains800': u'https://ndownloader.figshare.com/files/5608613', u'bas_classif': u'https://ndownloader.figshare.com/files/5608571', u'hydromod_other': u'https://ndownloader.figshare.com/files/5608595', u'soils': u'https://ndownloader.figshare.com/files/5608637', u'prot_areas': u'https://ndownloader.figshare.com/files/5608628', u'regions': u'https://ndownloader.figshare.com/files/5608634', u'geology': u'https://ndownloader.figshare.com/files/5608586', u'lc_change92': u'https://ndownloader.figshare.com/files/5608607', u'c01_rip100': u'https://ndownloader.figshare.com/files/5608616', u'lc01_basin': u'https://ndownloader.figshare.com/files/5608604', u'lc01_rip800': u'https://ndownloader.figshare.com/files/5608619', u'hydro': u'https://ndownloader.figshare.com/files/5608589', u'infrastructure': u'https://ndownloader.figshare.com/files/5608598', u'census_block': u'https://ndownloader.figshare.com/files/5608577', u'reach': u'https://ndownloader.figshare.com/files/5608631', u'topo': u'https://ndownloader.figshare.com/files/5608640', u'basinid': u'https://ndownloader.figshare.com/files/5608568', u'climate': u'https://ndownloader.figshare.com/files/5608583', u'landscape_pat': u'https://ndownloader.figshare.com/files/5608601', u'census_county': u'https://ndownloader.figshare.com/files/5608580', u'hydromod_dams': u'https://ndownloader.figshare.com/files/5608592', u'ages_variable_desc': u'https://ndownloader.figshare.com/files/5608646', u'bas_morph': u'https://ndownloader.figshare.com/files/5608574', u'lc01_mains100': u'https://ndownloader.figshare.com/files/5608610'},
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3544358",
                           description="streamflow in ecosystems")