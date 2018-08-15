# -*- coding: latin-1  -*-
#retriever
from retriever.lib.templates import BasicTextTemplate
from retriever.lib.models import Table, Cleanup, correct_invalid_value

SCRIPT = BasicTextTemplate(tables={'species_plot_year': Table('species_plot_year', ct_names=[u'Abilas', u'Abipro', u'Achmil', u'Achocc', u'Agoaur', u'Agrexa', u'Agrpal', u'Agrsca', u'Alnvir', u'Anamar', u'Antmic', u'Antros', u'Aqifor', u'Arcnev', u'Arnlat', u'Astled', u'Athdis', u'Blespi', u'Brocar', u'Brosit', u'Carmer', u'Carmic', u'Carpac', u'Carpay', u'Carpha', u'Carros', u'Carspe', u'Casmin', u'Chaang', u'Cirarv', u'Cisumb', u'Crycas', u'Danint', u'Descae', u'Elyely', u'Epiana', u'Eriova', u'Eripyr', u'Fesocc', u'Fravir', u'Gencal', u'Hiealb', u'Hiegra', u'Hyprad', u'Junmer', u'Junpar', u'Juncom', u'Leppun', u'Lommar', u'Luepec', u'Luihyp', u'Luplat', u'Luplep', u'Luzpar', u'Maiste', u'Pencar', u'Pencon', u'Penser', u'Phahas', u'Phlalp', u'Phldif', u'Phyemp', u'Pincon', u'Poasec', u'Poldav', u'Polmin', u'Pollon', u'Poljun', u'Popbal', u'Potarg', u'Psemen', u'Raccan', u'Rumace', u'Salsit', u'Saxfer', u'Senspp', u'Sibpro', u'Sorsit', u'Spiden', u'Trispi', u'Tsumer', u'Vacmem', u'Vervir', u'Vioadu', u'Xerten'],delimiter=',',columns=[(u'record_id', (u'pk-auto',)), (u'plot_id_year', (u'char', u'20')), (u'plot_name', (u'char', u'4')), (u'plot_number', (u'int',)), (u'year', (u'int',)), (u'count', (u'ct-double',))],ct_column='species'),'species': Table('species', do_not_bulk_insert=True)},
                           version="1.2.2",
                           title="Mount St. Helens vegetation recovery plots (del Moral 2010)",
                           citation="Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. Helens, Washington. Ecology 91:2185.",
                           name="mt-st-helens-veg",
                           retriever_minimum_version="2.0.dev",
                           urls={u'species_plot_year': u'https://ndownloader.figshare.com/files/5613783', u'species': u'https://ndownloader.figshare.com/files/5613789', u'structure_plot_year': u'https://ndownloader.figshare.com/files/5613786', u'plots': u'https://ndownloader.figshare.com/files/5613792'},
                           keywords=[u'plants', u'local-scale', u'time-serie', u'observational'],
                           retriever=True,
                           ref="https://figshare.com/collections/Thirty_years_of_permanent_vegetation_plots_Mount_St_Helens_Washington_USA/3303093",
                           description="Documenting vegetation recovery from volcanic disturbances using the most common species found in non-forested habitats on Mount St. Helens.")