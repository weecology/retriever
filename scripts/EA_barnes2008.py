from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'main': Table('main', cleanup=Cleanup(correct_invalid_value, nulls=['n/a', '0.0000E+00']))},
                           name="Marine Predator and Prey Body Sizes (Ecological Archives 2008)",
                           tags=['Animals', 'Marine'],
                           urls={'main': 'http://www.esapubs.org/Archive/ecol/E089/051/Predator_and_prey_body_sizes_in_marine_food_webs_vsn3.txt'},
                           shortname="MarineSize",
                           description="C. Barnes et al. 2008. Predator and prey body sizes in marine food webs. Ecology 89:881.")