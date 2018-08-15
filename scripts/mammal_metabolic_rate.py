# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'MammalMR2010': Table('MammalMR2010', cleanup=Cleanup(correct_invalid_value, missing_values=[-9999]))},
                           version="1.2.1",
                           title="Phylogeny and metabolic rates in mammals (Ecological Archives 2010)",
                           citation="Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783-2793.",
                           name="mammal-metabolic-rate",
                           retriever_minimum_version="2.0.dev",
                           urls={u'MammalMR2010': u'https://ndownloader.figshare.com/files/5616942'},
                           keywords=[u'mammals', u'literature-compilation', u'physiology'],
                           retriever=True,
                           ref="https://figshare.com/collections/Phylogeny_and_metabolic_scaling_in_mammals/3303477",
                           description="Data on basal metabolic rate (BMR) with experimental animal body mass, field metabolic rate (FMR) with wild animal body mass, and sources of the data. Ecological Archives E091-198-S1.")