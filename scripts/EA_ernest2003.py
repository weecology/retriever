from retriever.lib.templates import BasicTextTemplate
from retriever.lib.tools import ScriptTest

VERSION = '0.5'

SCRIPT = BasicTextTemplate(
                           name="Mammal Life History Database (Ecological Archives 2003)",
                           description="S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
                           shortname="MammalLH",
                           urls = {"species": "http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"}
                           )


class EAErnest2003Test(ScriptTest):
    def test_EAErnest2003(self):        
        ScriptTest.default_test(self,
                                main(),
                                [("species",
                                  "afa09eed4ca4ce5db31d15c4daa49ed3",
                                  "sporder, family, genus, species")
                                ])
