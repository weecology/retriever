# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.2.3",
                           description="A comprehensive compilation of data set on avian body sizes that would be useful for future comparative studies of avian biology.",
                           title="Bird Body Size and Life History (Lislevand et al. 2007)",
                           citation="Terje Lislevand, Jordi Figuerola, and Tamas Szekely. 2007. Avian body sizes in relation to fecundity, mating system, display behavior, and resource sharing. Ecology 88:1605.",
                           name="bird-size",
                           keywords=[u'birds', u'literature-compilation'],
                           retriever_minimum_version="2.0.dev",
                           tables={'species': Table('species', cleanup=Cleanup(correct_invalid_value, missing_values=[-999]),columns=[(u'Family', (u'int',)), (u'Species_number', (u'int',)), (u'Species_name', (u'char', u'133')), (u'English_name', (u'char', u'135')), (u'Subspecies', (u'char', u'121')), (u'M_mass', (u'double',)), (u'M_mass_N', (u'int',)), (u'F_mass', (u'double',)), (u'F_mass_N', (u'int',)), (u'unsexed_mass', (u'double',)), (u'unsexed_mass_N', (u'int',)), (u'M_wing', (u'double',)), (u'M_wing_N', (u'int',)), (u'F_wing', (u'double',)), (u'F_wing_N', (u'double',)), (u'Unsexed_wing', (u'double',)), (u'Unsexed_wing_N', (u'int',)), (u'M_tarsus', (u'double',)), (u'M_tarsus_N', (u'int',)), (u'F_tarsus', (u'double',)), (u'F_tarsus_N', (u'int',)), (u'Unsexed_tarsus', (u'double',)), (u'Unsexed_tarsus_N', (u'int',)), (u'M_bill', (u'double',)), (u'M_bill_N', (u'int',)), (u'F_bill', (u'double',)), (u'F_bill_N', (u'double',)), (u'Unsexed_bill', (u'double',)), (u'Unsexed_bill_N', (u'int',)), (u'M_tail', (u'double',)), (u'M_tail_N', (u'int',)), (u'F_tail', (u'double',)), (u'F_tail_N', (u'int',)), (u'Unsexed_tail', (u'double',)), (u'Unsexed_tail_N', (u'int',)), (u'Clutch_size', (u'double',)), (u'Egg_mass', (u'double',)), (u'Mating_System', (u'int',)), (u'Display', (u'int',)), (u'Resource', (u'int',)), (u'References', (u'char', u'130'))])},
                           urls={u'species': u'https://ndownloader.figshare.com/files/5599229'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3527864",
                           retriever=True)