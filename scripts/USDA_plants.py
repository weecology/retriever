name: USDA plants
description: Plant taxonomy system available on the USDA plants sitee.
shortname: PlantTaxonomy
tags: Plants, Taxonomy
url: http://plants.usda.gov

table: PlantTaxonomy, http://plants.usda.gov/java/downloadData?fileName=plantlst.txt&static=true
nulls: 
column: record_id, pk-auto
column: symbol, char, 7
column: synonym_symbol, char, 7
column: scientific_name, char, 20
column: common_name, char, 20
column: family, char, 20