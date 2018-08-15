# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'monthly_ppt': Table('monthly_ppt', replace_columns=[[u'jan', u'january'], [u'feb', u'february'], [u'mar', u'march'], [u'apr', u'april'], [u'jun', u'june'], [u'jul', u'july'], [u'aug', u'august'], [u'sep', u'september'], [u'oct', u'october'], [u'nov', u'november'], [u'dec', u'december']]),'monthly_sno': Table('monthly_sno', replace_columns=[[u'jan', u'january'], [u'feb', u'february'], [u'mar', u'march'], [u'apr', u'april'], [u'jun', u'june'], [u'jul', u'july'], [u'aug', u'august'], [u'sep', u'september'], [u'oct', u'october'], [u'nov', u'november'], [u'dec', u'december']]),'monthly_mean_temp': Table('monthly_mean_temp', replace_columns=[[u'jan', u'january'], [u'feb', u'february'], [u'mar', u'march'], [u'apr', u'april'], [u'jun', u'june'], [u'jul', u'july'], [u'aug', u'august'], [u'sep', u'september'], [u'oct', u'october'], [u'nov', u'november'], [u'dec', u'december']])},
                           version="1.2.1",
                           title="Sagebrush steppe mapped plant quadrats (Zachmann et al. 2010)",
                           citation="Luke Zachmann, Corey Moffet, and Peter Adler. 2010. Mapped quadrats in sagebrush steppe:long-term data for analyzing demographic rates and plant-plant interactions. Ecology 91:3427.",
                           name="mapped-plant-quads-id",
                           retriever_minimum_version="2.0.dev",
                           urls={u'density': u'https://ndownloader.figshare.com/files/5617443', u'taxonomy': u'https://ndownloader.figshare.com/files/5617464', u'quad_inventory': u'https://ndownloader.figshare.com/files/5617458', u'monthly_sno': u'https://ndownloader.figshare.com/files/5617473', u'cover': u'https://ndownloader.figshare.com/files/5617446', u'grazing': u'https://ndownloader.figshare.com/files/5617455', u'quad_info': u'https://ndownloader.figshare.com/files/5617452', u'monthly_ppt': u'https://ndownloader.figshare.com/files/5617470', u'counts': u'https://ndownloader.figshare.com/files/5617476', u'monthly_mean_temp': u'https://ndownloader.figshare.com/files/5617467', u'species': u'https://ndownloader.figshare.com/files/5617461'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3550215",
                           description="This data set consists of 26 permanent 1-m2 quadrats located on sagebrush steppe in eastern Idaho, USA.")