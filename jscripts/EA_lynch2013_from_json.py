#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description='The data set represents the accumulation of 19 years of seabird population abundance data which was collected by the Antarctic Site Inventory, an opportunistic vessel-based monitoring program surveying the Antarctic Peninsula and associated sub-Antarctic Islands.',
                           tags=['Taxon > Birds'],
                           citation='Heather J. Lynch, Ron Naveen, and Paula Casanovas. 2013. Antarctic Site Inventory breeding bird survey data, 1994-2013. Ecology 94:2653.',
                           urls={'species': 'http://esapubs.org/archive/ecol/E094/243/Antarctic_Site_Inventory_census_data_1994_2012.csv'},
                           shortname='ArcticBreedBird',
                           ref='http://esapubs.org/archive/ecol/E094/243/',
                           name='Antarctic Site Inventory breeding bird survey data, 1994-2013')