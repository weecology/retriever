#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'monthly_temp': Table('monthly_temp', cleanup=Cleanup(correct_invalid_value, nulls=['NA']),replace_columns=[['jan', 'january'], ['feb', 'february'], ['mar', 'march'], ['apr', 'april'], ['jun', 'june'], ['jul', 'july'], ['aug', 'august'], ['sep', 'september'], ['oct', 'october'], ['nov', 'november'], ['dec', 'december']]),'monthly_ppt': Table('monthly_ppt', cleanup=Cleanup(correct_invalid_value, nulls=['NA']),replace_columns=[['jan', 'january'], ['feb', 'february'], ['mar', 'march'], ['apr', 'april'], ['jun', 'june'], ['jul', 'july'], ['aug', 'august'], ['sep', 'september'], ['oct', 'october'], ['nov', 'november'], ['dec', 'december']]),'quadrat_inventory': Table('quadrat_inventory', cleanup=Cleanup(correct_invalid_value, nulls=['NA']))},
                           description='Demographic data for testing current theories in plant ecology and forecasting the effects of global change.',
                           tags=['Taxon > Plants', 'Spatial Scale > Local', 'Data Type > Time Series', 'Data Type > Observational'],
                           citation='Peter B. Adler, William R. Tyburczy, and William K. Lauenroth. 2007. Long-term mapped quadrats from Kansas prairie:demographic information for herbaceaous plants. Ecology 88:2673.',
                           urls={'monthly_temp': 'http://esapubs.org/archive/ecol/E088/161/monthly_temp.csv', 'quadrat_info': 'http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv', 'monthly_ppt': 'http://esapubs.org/archive/ecol/E088/161/monthly_ppt.csv', 'quadrat_inventory': 'http://esapubs.org/archive/ecol/E088/161/quadrat_inventory.csv', 'main': 'http://esapubs.org/archive/ecol/E088/161/allrecords.csv', 'species': 'http://esapubs.org/archive/ecol/E088/161/species_list.csv'},
                           shortname='Adler2007',
                           ref='http://esapubs.org/archive/ecol/E088/161/',
                           name='Kansas plant quadrats (Ecological Archives 2007)')