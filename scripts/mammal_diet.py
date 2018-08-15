# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.1.2",
                           name="mammal-diet",
                           title="MammalDIET",
                           citation="Kissling WD, Dalby L, Flojgaard C, Lenoir J, Sandel B, Sandom C, Trojelsgaard K, Svenning J-C (2014) Establishing macroecological trait datasets:digitalization, extrapolation, and validation of diet preferences in terrestrial mammals worldwide. Ecology and Evolution, online in advance of print. doi:10.1002/ece3.1136",
                           retriever_minimum_version="2.0.dev",
                           tables={'diet': Table('diet', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']),columns=[(u'TaxonID', (u'pk-int',)), (u'TaxonOrder', (u'char',)), (u'Family', (u'char',)), (u'Genus', (u'char',)), (u'Species', (u'char',)), (u'Animal', (u'int',)), (u'Vertebrate', (u'int',)), (u'Mammal', (u'int',)), (u'Bird', (u'int',)), (u'Herptile', (u'int',)), (u'Fish', (u'int',)), (u'Invertebrate', (u'int',)), (u'Plant', (u'int',)), (u'Seed', (u'int',)), (u'Fruit', (u'int',)), (u'Nectar', (u'int',)), (u'Root', (u'int',)), (u'Leaf', (u'int',)), (u'Woody', (u'int',)), (u'Herbaceous', (u'int',)), (u'Other', (u'int',)), (u'TaxonomicNote', (u'char',)), (u'FillCode', (u'double',)), (u'TrophicLevel', (u'char',)), (u'MammalEater', (u'int',)), (u'Insectivore', (u'int',)), (u'Frugivore', (u'int',)), (u'Granivore', (u'int',)), (u'Folivore', (u'int',)), (u'DataSource', (u'char',))],contains_pk=True)},
                           urls={u'diet': u'http://datadryad.org/bitstream/handle/10255/dryad.64565/MammalDIET_v1.0.txt'},
                           keywords=[u'mammals', u'literature-compilation'],
                           retriever=True,
                           description="MammalDIET provides a comprehensive, unique and freely available dataset on diet preferences for all terrestrial mammals worldwide.")