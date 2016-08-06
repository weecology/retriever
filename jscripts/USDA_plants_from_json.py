#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'PlantTaxonomy': Table('PlantTaxonomy', columns=[('record_id', ('pk-auto',)), ('symbol', ('char', '7')), ('synonym_symbol', ('char', '7')), ('scientific_name', ('char',)), ('common_name', ('char', '50')), ('family', ('char', '30'))],do_not_bulk_insert=True)},
                           description='Plant taxonomy system available on the USDA plants site.',
                           tags=['Taxon > Plants', 'Data Type > Taxonomy'],
                           urls={'PlantTaxonomy': 'http://plants.usda.gov/java/downloadData?fileName=plantlst.txt&static=true'},
                           shortname='PlantTaxonomy',
                           ref='http://plants.usda.gov',
                           name='USDA plants')