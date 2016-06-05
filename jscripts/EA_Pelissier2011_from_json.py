#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'ind_loc_girth': Table('ind_loc_girth', cleanup=Cleanup(correct_invalid_value, nulls=['NA'])),'sp_list': Table('sp_list', cleanup=Cleanup(correct_invalid_value, nulls=['NA']))},
                           description='A data set on demography of trees monitored over 20 years in Uppangala permanent sample plot (UPSP).',
                           tags=['Taxon > Plants', 'Data Type > Time Series', 'Data Type > Observational'],
                           citation='Raphael Pelissier, Jean-Pierre Pascal, N. Ayyappan, B. R. Ramesh, S. Aravajy, and S. R. Ramalingam. 2011. Twenty years tree demography in an undisturbed Dipterocarp permanent sample plot at Uppangala, Western Ghats of India. Ecology 92:1376.',
                           urls={'ind_loc_girth': 'http://esapubs.org/archive/ecol/E092/115/UPSP_Demo_data.txt', 'sp_list': 'http://esapubs.org/archive/ecol/E092/115/UPSP_Species_list2.txt'},
                           shortname='TreeWesternGhats',
                           name='Twenty years tree demography in Western Ghats of India - Pelissier, et al., 2011')