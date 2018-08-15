# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'ranges': Table('ranges', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA', u'\\']))},
                           version="1.1.2",
                           title="Database of Vertebrate Home Range Sizes - Tamburello et al., 2015",
                           citation="Tamburello N, Cote IM, Dulvy NK (2015) Energy and the scaling of animal space use. The American Naturalist 186(2):196-211. http://dx.doi.org/10.1086/682070.",
                           name="home-ranges",
                           retriever_minimum_version="2.0.dev",
                           urls={u'ranges': u'http://datadryad.org/bitstream/handle/10255/dryad.84768/Tamburelloetal_HomeRangeDatabase.csv'},
                           keywords=[u'literature-compilation', u'birds', u'mammals', u'reptiles', u'fishes'],
                           retriever=True,
                           ref="http://datadryad.org/resource/doi:10.5061/dryad.q5j65/1",
                           description="Database of mean species masses and corresponding empirically measured home range sizes for 569 vertebrate species from across the globe, including birds, mammals, reptiles, and fishes.")