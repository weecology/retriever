from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '1.0'

SCRIPT = BasicTextTemplate(tables={'MammalMR2010': Table('MammalMR2010', cleanup=Cleanup(correct_invalid_value, nulls=['-9999']))},
                           name="Phylogeny and metabolic rates in mammals (Ecological Archives 2010)",
                           tags=['Animals', 'Mammals'],
                           urls={'MammalMR2010': 'http://www.esapubs.org/archive/ecol/E091/198/data.txt'},
                           shortname="MammalMR2010",
                           description="Isabella Capellini, Chris Venditti, and Robert A. Barton. 2010. Phylogeny and metabolic rates in mammals. Ecology 20:2783-2793.")