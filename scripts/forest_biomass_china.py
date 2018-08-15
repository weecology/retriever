# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'biomass': Table('biomass', cleanup=Cleanup(correct_invalid_value, missing_values=[u'NA']))},
                           version="1.2.1",
                           title="Biomass and Its Allocation in Chinese Forest Ecosystems (Luo, et al., 2014)",
                           citation="Yunjian Luo, Xiaoquan Zhang, Xiaoke Wang, and Fei Lu. 2014. Biomass and its allocation in Chinese forest ecosystems. Ecology 95:2026.",
                           name="forest-biomass-china",
                           retriever_minimum_version="2.0.dev",
                           urls={u'biomass': u'https://ndownloader.figshare.com/files/5631069'},
                           keywords=[u'biomass', u'China', u'climate', u'forest'],
                           retriever=True,
                           ref="https://figshare.com/collections/Biomass_and_its_allocation_of_Chinese_forest_ecosystems/3306930",
                           description="Forest biomass data set of China which includes tree overstory components (stems, branches, leaves, and roots, among all other plant material), the understory vegetation (saplings, shrubs, herbs, and mosses), woody liana vegetation, and the necromass components of dead organic matter (litterfall, suspended branches, and dead trees).")