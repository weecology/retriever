#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'MOM': Table('MOM', cleanup=Cleanup(correct_invalid_value, nulls=[-999]),columns=[('record_id', ('pk-auto',)), ('continent', ('char', '20')), ('status', ('char', '20')), ('sporder', ('char', '20')), ('family', ('char', '20')), ('genus', ('char', '20')), ('species', ('char', '20')), ('log_mass_g', ('double',)), ('comb_mass_g', ('double',)), ('reference', ('char',))])},
                           description="A data set of compiled body mass information for all mammals on Earth.",
                           tags=['Taxon > Mammals', 'Data Type > Compilation'],
                           citation="Felisa A. Smith, S. Kathleen Lyons, S. K. Morgan Ernest, Kate E. Jones, Dawn M. Kaufman, Tamar Dayan, Pablo A. Marquet, James H. Brown, and John P. Haskell. 2003. Body mass of late Quaternary mammals. Ecology 84:3403.",
                           urls={'MOM': 'http://www.esapubs.org/Archive/ecol/E084/094/MOMv3.3.txt'},
                           shortname="MoM2003",
                           ref="http://www.esapubs.org/archive/ecol/E084/094/",
                           name="Masses of Mammals (Ecological Archives 2003)")