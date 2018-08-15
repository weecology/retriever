# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'quad_info': Table('quad_info', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'allrecords_density': Table('allrecords_density', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'quad_inventory': Table('quad_inventory', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'species_list': Table('species_list', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'quad_stocking_rate': Table('quad_stocking_rate', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'daily_climate': Table('daily_climate', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'species_name_changes': Table('species_name_changes', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'allrecords_cover': Table('allrecords_cover', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']))},
                           version="1.2.1",
                           title="Shortgrass steppe mapped plants quads - Chu et al. 2013",
                           citation="Cover, density, and demographics of shortgrass steppe plants mapped 1997-2010 in permanent grazed and ungrazed quadrats. Chengjin Chu, John Norman, Robert Flynn, Nicole Kaplan, William K. Lauenroth, and Peter B. Adler. Ecology 2013 94:6, 1435-1435.",
                           name="mapped-plant-quads-co",
                           retriever_minimum_version="2.0.dev",
                           urls={u'quad_info': u'https://ndownloader.figshare.com/files/5626710', u'allrecords_density': u'https://ndownloader.figshare.com/files/5626698', u'quad_inventory': u'https://ndownloader.figshare.com/files/5626707', u'species_list': u'https://ndownloader.figshare.com/files/5626719', u'quad_stocking_rate': u'https://ndownloader.figshare.com/files/5626713', u'daily_climate': u'https://ndownloader.figshare.com/files/5626716', u'species_name_changes': u'https://ndownloader.figshare.com/files/5626722', u'allrecords_cover': u'https://ndownloader.figshare.com/files/5626701'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3556779",
                           description="This data set maps and analyzes demographic rates of many common plant species in the shortgrass steppe of North America under grazed and ungrazed conditions.")