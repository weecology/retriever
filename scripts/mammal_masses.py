# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(version="1.3.2",
                           description="A data set of compiled body mass information for all mammals on Earth.",
                           title="Masses of Mammals (Smith et al. 2003)",
                           citation="Felisa A. Smith, S. Kathleen Lyons, S. K. Morgan Ernest, Kate E. Jones, Dawn M. Kaufman, Tamar Dayan, Pablo A. Marquet, James H. Brown, and John P. Haskell. 2003. Body mass of late Quaternary mammals. Ecology 84:3403.",
                           name="mammal-masses",
                           keywords=[u'mammals', u'literature-compilation', u'size'],
                           retriever_minimum_version="2.0.dev",
                           tables={'MammalMasses': Table('MammalMasses', header_rows=0,cleanup=Cleanup(correct_invalid_value, missing_values=[-999]),columns=[(u'record_id', (u'pk-auto',)), (u'continent', (u'char', u'20')), (u'status', (u'char', u'20')), (u'sporder', (u'char', u'20')), (u'family', (u'char', u'20')), (u'genus', (u'char', u'20')), (u'species', (u'char', u'20')), (u'log_mass_g', (u'double',)), (u'comb_mass_g', (u'double',)), (u'reference', (u'char',))])},
                           urls={u'MammalMasses': u'https://ndownloader.figshare.com/files/5593343'},
                           licenses=[{u'name': u'CC0-1.0'}],
                           ref="https://figshare.com/articles/Data_Paper_Data_Paper/3523112",
                           retriever=True)