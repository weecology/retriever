# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'PlantTaxonomy': Table('PlantTaxonomy', columns=[(u'record_id', (u'pk-auto',)), (u'symbol', (u'char', u'7')), (u'synonym_symbol', (u'char', u'7')), (u'scientific_name', (u'char',)), (u'common_name', (u'char', u'50')), (u'family', (u'char', u'30'))],do_not_bulk_insert=True)},
                           version="1.1.3",
                           title="USDA plant list - taxonomy for US plant species",
                           citation="USDA, NRCS. 2017. The PLANTS Database (http://plants.usda.gov, DATEOFDOWNLOAD). National Plant Data Team, Greensboro, NC 27401-4901 USA.",
                           name="plant-taxonomy-us",
                           retriever_minimum_version="2.0.dev",
                           urls={u'PlantTaxonomy': u'http://plants.usda.gov/java/downloadData?fileName=plantlst.txt&static=true'},
                           keywords=[u'plants', u'taxonomy'],
                           retriever=True,
                           ref="http://plants.usda.gov",
                           description="Plant taxonomy data for the United States from the USDA plants website")