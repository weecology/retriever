#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'biomass': Table('biomass', cleanup=Cleanup(correct_invalid_value, nulls=['NA']))},
                           description='Forest biomass data set of China which includes tree overstory components (stems, branches, leaves, and roots, among all other plant material), the understory vegetation (saplings, shrubs, herbs, and mosses), woody liana vegetation, and the necromass components of dead organic matter (litterfall, suspended branches, and dead trees).',
                           tags=['allocation > biomass > China > climate > forest type > necromass > stand structure'],
                           citation='Yunjian Luo, Xiaoquan Zhang, Xiaoke Wang, and Fei Lu. 2014. Biomass and its allocation in Chinese forest ecosystems. Ecology 95:2026.',
                           urls={'biomass': 'http://esapubs.org/archive/ecol/E095/177/CForBioData_v1.0.txt'},
                           shortname='CForBioData',
                           ref='http://esapubs.org/archive/ecol/E095/177/',
                           name='Biomass and Its Allocation in Chinese Forest Ecosystems - Luo, et al., 2014')