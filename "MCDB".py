#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description="This data set includes species lists for 1000 mammal communities, excluding bats, with species-level abundances available for 940 of these communities.",
                           tags=['Taxon > Mammals', 'Spatial Scale > Global', 'Data Type > Observational'],
                           citation="Katherine M. Thibault, Sarah R. Supp, Mikaelle Giffin, Ethan P. White, and S. K. Morgan Ernest. 2011. Species composition and abundance of mammalian communities. Ecology 92:2316.",
                           urls={'communities': 'http://esapubs.org/archive/ecol/E092/201/data/MCDB_communities.csv', 'species': 'http://esapubs.org/archive/ecol/E092/201/data/MCDB_species.csv', 'references': 'http://esapubs.org/archive/ecol/E092/201/data/MCDB_references.csv', 'trapping': 'http://esapubs.org/archive/ecol/E092/201/data/MCDB_trapping.csv', 'sites': 'http://esapubs.org/archive/ecol/E092/201/data/MCDB_sites.csv'},
                           shortname="MCDB",
                           ref="http://esapubs.org/archive/ecol/E092/201/",
                           name="Mammal Community DataBase (Ecological Archives 2011)")