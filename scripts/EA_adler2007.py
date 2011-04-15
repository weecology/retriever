from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'monthly_temp': Table('monthly_temp', replace_columns=[('jan', 'january'), ('feb', 'february'), ('mar', 'march'), ('apr', 'april'), ('jun', 'june'), ('jul', 'july'), ('aug', 'august'), ('sep', 'september'), ('oct', 'october'), ('nov', 'november'), ('dec', 'december')],cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'monthly_ppt': Table('monthly_ppt', replace_columns=[('jan', 'january'), ('feb', 'february'), ('mar', 'march'), ('apr', 'april'), ('jun', 'june'), ('jul', 'july'), ('aug', 'august'), ('sep', 'september'), ('oct', 'october'), ('nov', 'november'), ('dec', 'december')],cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'quadrat_inventory': Table('quadrat_inventory', cleanup=Cleanup(correct_invalid_value, nulls=['NA']))},
                           name="Kansas plant quadrats (Ecological Archives 2007)",
                           tags=['Plants'],
                           ref="http://esapubs.org/archive/ecol/E088/161/",
                           urls={'quadrat_inventory': 'http://esapubs.org/archive/ecol/E088/161/quadrat_inventory.csv', 'monthly_temp': 'http://esapubs.org/archive/ecol/E088/161/monthly_temp.csv', 'quadrat_info': 'http://esapubs.org/archive/ecol/E088/161/quadrat_info.csv', 'monthly_ppt': 'http://esapubs.org/archive/ecol/E088/161/monthly_ppt.csv', 'main': 'http://esapubs.org/archive/ecol/E088/161/allrecords.csv', 'species': 'http://esapubs.org/archive/ecol/E088/161/species_list.csv'},
                           shortname="Adler2007",
                           description="Peter B. Adler, William R. Tyburczy, and William K. Lauenroth. 2007. Long-term mapped quadrats from Kansas prairie:demographic information for herbaceaous plants. Ecology 88:2673.")