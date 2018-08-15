# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'monthly_temp': Table('monthly_temp', replace_columns=[[u'jan', u'january'], [u'feb', u'february'], [u'mar', u'march'], [u'apr', u'april'], [u'jun', u'june'], [u'jul', u'july'], [u'aug', u'august'], [u'sep', u'september'], [u'oct', u'october'], [u'nov', u'november'], [u'dec', u'december']],cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'monthly_ppt': Table('monthly_ppt', replace_columns=[[u'jan', u'january'], [u'feb', u'february'], [u'mar', u'march'], [u'apr', u'april'], [u'jun', u'june'], [u'jul', u'july'], [u'aug', u'august'], [u'sep', u'september'], [u'oct', u'october'], [u'nov', u'november'], [u'dec', u'december']],cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA'])),'quadrat_inventory': Table('quadrat_inventory', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']))},
                           version="1.2.1",
                           title="Mapped plant quadrat time-series from Kansas (Adler et al. 2007)",
                           citation="Peter B. Adler, William R. Tyburczy, and William K. Lauenroth. 2007. Long-term mapped quadrats from Kansas prairie:demographic information for herbaceaous plants. Ecology 88:2673.",
                           name="mapped-plant-quads-ks",
                           retriever_minimum_version="2.0.dev",
                           urls={u'quadrat_inventory': u'https://ndownloader.figshare.com/files/5599940', u'monthly_temp': u'https://ndownloader.figshare.com/files/5599946', u'quadrat_info': u'https://ndownloader.figshare.com/files/5599937', u'monthly_ppt': u'https://ndownloader.figshare.com/files/5599949', u'main': u'https://ndownloader.figshare.com/files/5599934', u'species': u'https://ndownloader.figshare.com/files/5599943'},
                           keywords=[u'plants', u'local-scale', u'time-series', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3528368",
                           description="Demographic data for testing current theories in plant ecology and forecasting the effects of global change.")