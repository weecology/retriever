from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'PlantTaxonomy': Table('PlantTaxonomy', columns=[('record_id', ('pk-auto',)), ('symbol', ('char', '7')), ('synonym_symbol', ('char', '7')), ('scientific_name', ('char', '20')), ('common_name', ('char', '20')), ('family', ('char', '20'))])},
                           name="USDA plants",
                           tags=['Plants', 'Taxonomy'],
                           ref="http://plants.usda.gov",
                           urls={'PlantTaxonomy': 'http://plants.usda.gov/java/downloadData?fileName=plantlst.txt&static=true'},
                           shortname="PlantTaxonomy",
                           description="Plant taxonomy system available on the USDA plants sitee.")