#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'diet': Table('diet', cleanup=Cleanup(correct_invalid_value, nulls=['NA']),columns=[('TaxonID', ('pk-int',)), ('TaxonOrder', ('char',)), ('Family', ('char',)), ('Genus', ('char',)), ('Species', ('char',)), ('Animal', ('int',)), ('Vertebrate', ('int',)), ('Mammal', ('int',)), ('Bird', ('int',)), ('Herptile', ('int',)), ('Fish', ('int',)), ('Invertebrate', ('int',)), ('Plant', ('int',)), ('Seed', ('int',)), ('Fruit', ('int',)), ('Nectar', ('int',)), ('Root', ('int',)), ('Leaf', ('int',)), ('Woody', ('int',)), ('Herbaceous', ('int',)), ('Other', ('int',)), ('TaxonomicNote', ('char',)), ('FillCode', ('double',)), ('TrophicLevel', ('char',)), ('MammalEater', ('int',)), ('Insectivore', ('int',)), ('Frugivore', ('int',)), ('Granivore', ('int',)), ('Folivore', ('int',)), ('DataSource', ('char',))],contains_pk=True)},
                           description='MammalDIET provides a comprehensive, unique and freely available dataset on diet preferences for all terrestrial mammals worldwide.',
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation='Kissling WD, Dalby L, Flojgaard C, Lenoir J, Sandel B, Sandom C, Trojelsgaard K, Svenning J-C (2014) Establishing macroecological trait datasets:digitalization, extrapolation, and validation of diet preferences in terrestrial mammals worldwide. Ecology and Evolution, online in advance of print. doi:10.1002/ece3.1136',
                           urls={'diet': 'http://datadryad.org/bitstream/handle/10255/dryad.64565/MammalDIET_v1.0.txt'},
                           shortname='MammalDIET',
                           name='MammalDIET')