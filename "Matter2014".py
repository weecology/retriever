#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'Dispersal': Table('Dispersal', cleanup=Cleanup(correct_invalid_value, nulls=['n/a'])),'Landscape': Table('Landscape', cleanup=Cleanup(correct_invalid_value, nulls=['n/a'])),'PopulationAbunTransect': Table('PopulationAbunTransect', cleanup=Cleanup(correct_invalid_value, nulls=['n/a'])),'PopulationAbunMark_Recap': Table('PopulationAbunMark_Recap', cleanup=Cleanup(correct_invalid_value, nulls=['n/a']))},
                           description="Stephen F. Matter, Nusha Keyghobadhi, and Jens Roland. 2014. Ten years of abundance data within a spatial population network of the alpine butterfly, Parnassius smintheus. Ecology 95:2985.",
                           tags=['Taxon > Butterflies', 'Data Type > Observation', 'Spatial Scale > Metapopulation'],
                           citation="Matter, Stephen F., Nusha Keyghobadhi, and Jens Roland. 2014. Ten years of abundance data within a spatial population network of the alpine butterfly, Parnassius smintheus. Ecology 95:2985. Ecological Archives E095-258.",
                           urls={'Dispersal': 'http://esapubs.org/archive/ecol/E095/258/Dispersal.csv', 'Landscape': 'http://esapubs.org/archive/ecol/E095/258/Landscape.csv', 'PopulationAbunMark_Recap': 'http://esapubs.org/archive/ecol/E095/258/PopulationAbunMark-Recap.csv', 'PopulationAbunTransect': 'http://esapubs.org/archive/ecol/E095/258/PopulationAbunTransect.csv'},
                           shortname="Matter2014",
                           name="Spatial Population Data Alpine Butterfly -- Matter et al 2014")