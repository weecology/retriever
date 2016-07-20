#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description="Community abundance data for fish, reptiles, amphibians, beetles, spiders, and birds, compiled from the literature by Elita Baldridge.",
                           citation="Baldridge, Elita, A Data-intensive Assessment of the Species Abundance Distribution(2013). All Graduate Theses and Dissertations. Paper 4276.",
                           urls={'citations': 'http://files.figshare.com/2023506/Citations_table_abundances.csv', 'main': 'http://files.figshare.com/2023547/Species_abundances.csv', 'sites': 'http://files.figshare.com/2023504/Sites_table_abundances.csv'},
                           shortname="MiscAbundanceDB",
                           name="Miscellaneous Abundance Database (figshare 2012)")