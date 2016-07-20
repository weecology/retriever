#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description="characterization of Species by physiological, behavioral, and ecological attributes that are subjected to varying evolutionary and ecological constraints and jointly determine their role and function in ecosystems.",
                           tags=['Taxon > Mammals', 'Taxon > Birds', 'Data Type > Compilation'],
                           citation="Hamish Wilman, Jonathan Belmaker, Jennifer Simpson, Carolina de la Rosa, Marcelo M. Rivadeneira, and Walter Jetz. 2014. EltonTraits 1.0:Species-level foraging attributes of the world's birds and mammals. Ecology 95:2027.",
                           urls={'BirdCitations': 'http://esapubs.org/archive/ecol/E095/178/BirdFuncDatSources.txt', 'MammFuncDat': 'http://esapubs.org/archive/ecol/E095/178/MamFuncDat.txt', 'BirdFuncDat': 'http://esapubs.org/archive/ecol/E095/178/BirdFuncDat.txt', 'MammCitations': 'http://esapubs.org/archive/ecol/E095/178/MamFuncDatSources.txt'},
                           shortname="EltonTraits",
                           name="Mammal and Bird foraging attributes -- Wilman, et al., 2014")