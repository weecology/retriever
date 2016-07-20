#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={},
                           description="long term plant quadrats of northern mixed prairie in Montana.",
                           citation="Chengjin Chu, John Norman, Robert Flynn, Nicole Kaplan, William K. Lauenroth, and Peter B. Adler. 2013. Cover, density, and demographics of shortgrass steppe plants mapped 1997-2010 in permanent grazed and ungrazed quadrats. Ecology 94:1435.",
                           urls={'allrecords_cover': 'http://esapubs.org/archive/ecol/E092/143/allrecords_cover.csv', 'allrecords_density': 'http://esapubs.org/archive/ecol/E092/143/allrecords_density.csv', 'species_list': 'http://esapubs.org/archive/ecol/E092/143/species_list.csv'},
                           shortname="Anderson2011",
                           ref="http://dx.doi.org/10.1890/13-0121.1",
                           name="Northern mixed prairie maps - Anderson et al. 2011")