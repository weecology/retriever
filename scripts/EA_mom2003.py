from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table

VERSION = '0.5'
## TO DO:
##   fix Error: list index out of range
##   get missing values replace to work
##   deal with the lack of a header in original file issue
##      header should read: Continent, Status, Order, Family, Genus, Species, Log Mass (grams), Combined Mass (grams), Reference

#replace = [("-999", "NULL")]

SCRIPT = BasicTextTemplate(
                           name="Masses of Mammals (Ecological Archives 2003)",
                           description="Felisa A. Smith, S. Kathleen Lyons, S. K. Morgan Ernest, Kate E. Jones, Dawn M. Kaufman, Tamar Dayan, Pablo A. Marquet, James H. Brown, and John P. Haskell. 2003. Body mass of late Quaternary mammals. Ecology 84:3403.",
                           shortname="MoM2003",
                           ref="http://www.esapubs.org/archive/ecol/E084/094/",
                           urls = {
                                   "MOM": "http://www.esapubs.org/Archive/ecol/E084/094/MOMv3.3.txt"
                                   },
                           #tables = {
                                     #"MOM": Table("MOM", replace_columns = replace)
                                     #}
                           )