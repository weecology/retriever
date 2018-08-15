# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.2.1",
                           title="Mammal Community DataBase (Thibault et al. 2011)",
                           citation="Katherine M. Thibault, Sarah R. Supp, Mikaelle Giffin, Ethan P. White, and S. K. Morgan Ernest. 2011. Species composition and abundance of mammalian communities. Ecology 92:2316.",
                           name="mammal-community-db",
                           retriever_minimum_version="2.0.dev",
                           urls={u'communities': u'https://ndownloader.figshare.com/files/5620542', u'trapping': u'https://ndownloader.figshare.com/files/5620554', u'references': u'https://ndownloader.figshare.com/files/5620545', u'sites': u'https://ndownloader.figshare.com/files/5620548', u'species': u'https://ndownloader.figshare.com/files/5620551'},
                           keywords=[u'mammals', u'global-scale', u'observational', u'literature-compilation'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3552243",
                           description="This data set includes species lists for 1000 mammal communities, excluding bats, with species-level abundances available for 940 of these communities.")