# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           version="1.2.1",
                           title="Foraging attributes for birds and mammals (Wilman, et al., 2014)",
                           citation="Hamish Wilman, Jonathan Belmaker, Jennifer Simpson, Carolina de la Rosa, Marcelo M. Rivadeneira, and Walter Jetz. 2014. EltonTraits 1.0: Species-level foraging attributes of the world's birds and mammals. Ecology 95:2027.",
                           name="elton-traits",
                           retriever_minimum_version="2.0.dev",
                           urls={u'BirdCitations': u'https://ndownloader.figshare.com/files/5631087', u'MammFuncDat': u'https://ndownloader.figshare.com/files/5631084', u'BirdFuncDat': u'https://ndownloader.figshare.com/files/5631081', u'MammCitations': u'https://ndownloader.figshare.com/files/5631090'},
                           keywords=[u'mammals', u'birds', u'literature-compilation'],
                           retriever=True,
                           ref="https://figshare.com/collections/EltonTraits_1_0_Species-level_foraging_attributes_of_the_world_s_birds_and_mammals/3306933",
                           description="Characterization of species by physiological, behavioral, and ecological attributes that are subjected to varying evolutionary and ecological constraints and jointly determine their role and function in ecosystems.")