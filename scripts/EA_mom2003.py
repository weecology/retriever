from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

VERSION = '0.5'
SCRIPT = BasicTextTemplate(
                           name="Masses of Mammals (Ecological Archives 2003)",
                           description="Felisa A. Smith, S. Kathleen Lyons, S. K. Morgan Ernest, Kate E. Jones, Dawn M. Kaufman, Tamar Dayan, Pablo A. Marquet, James H. Brown, and John P. Haskell. 2003. Body mass of late Quaternary mammals. Ecology 84:3403.",
                           shortname="MoM2003",
                           tags=["Animals", "Mammals"],
                           ref="http://www.esapubs.org/archive/ecol/E084/094/",
                           urls = {
                                   "MOM": "http://www.esapubs.org/Archive/ecol/E084/094/MOMv3.3.txt"
                                   },
                           tables = {
                                     "MOM": Table("MOM", 
                                                  cleanup=Cleanup(correct_invalid_value,
                                                                  nulls=[-999]),
                                                  columns=[("record_id"             ,   ("pk-auto",)    ),
                                                           ("continent"             ,   ("char", 7)     ),
                                                           ("status"                ,   ("char", 7)     ),
                                                           ("sporder"               ,   ("char", 20)    ),
                                                           ("family"                ,   ("char", 20)    ),
                                                           ("genus"                 ,   ("char", 20)    ),
                                                           ("species"               ,   ("char", 20)    ),
                                                           ("log_mass_g"            ,   ("double",)     ),
                                                           ("comb_mass_g"           ,   ("double",)     ),
                                                           ("reference"             ,   ("char", 10)    ),
                                                           ]
                                                  )
                                     }
                           )
