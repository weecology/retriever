# retriever
"""EcoData Retriever script for the Vegetation plots del Moral"""
import os

from retriever.lib.templates import Script
from retriever.lib.models import Table


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Vegetation plots - del Moral, 2010"
        self.shortname = "DelMoral2010"
        self.ref = "http://esapubs.org/archive/ecol/E091/152/"
        self.urls = {
            'species_plot_year': 'http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_PLOT_YEAR.csv',
            'species': 'http://esapubs.org/archive/ecol/E091/152/MSH_SPECIES_DESCRIPTORS.csv',
            'structure_plot_year': 'http://esapubs.org/archive/ecol/E091/152/MSH_STRUCTURE_PLOT_YEAR.csv',
            'plots': 'http://esapubs.org/archive/ecol/E091/152/MSH_PLOT_DESCRIPTORS.csv'
        }
        self.description = "Documenting vegetation recovery from volcanic disturbances using the most common species found in non-forested habitats on Mount St. Helens."
        self.citation = "Roger del Moral. 2010. Thirty years of permanent vegetation plots, Mount St. Helens, Washington. Ecology 91:2185.",
        self.tags = ['Taxon > Plants', 'Spatial Scale > Local', 'Data Type > Time Series', 'Data Type > Observational']

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        # structure_plot_year table
        self.engine.auto_create_table(Table("structure_plot_year"), url=self.urls["structure_plot_year"])
        self.engine.insert_data_from_url(self.urls["structure_plot_year"])

        # structure_plot_year table
        self.engine.auto_create_table(Table("plots"), url=self.urls["plots"])
        self.engine.insert_data_from_url(self.urls["plots"])

        # species_plot_year tables
        table = Table("species_plot_year")
        table.delimiter = ','
        table.columns = [
            ('record_id', ('pk-auto',)),
            ('plot_id_year', ('char',)),
            ('plot_name', ('char',)),
            ('plot_number', ('int',)),
            ('year', ('int',)),
            ('species', ('ct_column',)),
            ('count', ('ct-double',))
        ]

        table.ct_column = 'species'
        table.ct_names = ['Abilas', 'Abipro', 'Achmil', 'Achocc', 'Agoaur', 'Agrexa', 'Agrpal', 'Agrsca', 'Alnvir',
                          'Anamar', 'Antmic', 'Antros', 'Aqifor', 'Arcnev', 'Arnlat', 'Astled', 'Athdis', 'Blespi',
                          'Brocar', 'Brosit', 'Carmer', 'Carmic', 'Carpac', 'Carpay', 'Carpha', 'Carros', 'Carspe',
                          'Casmin', 'Chaang', 'Cirarv', 'Cisumb', 'Crycas', 'Danint', 'Descae', 'Elyely', 'Epiana',
                          'Eriova', 'Eripyr', 'Fesocc', 'Fravir', 'Gencal', 'Hiealb', 'Hiegra', 'Hyprad', 'Junmer',
                          'Junpar', 'Juncom', 'Leppun', 'Lommar', 'Luepec', 'Luihyp', 'Luplat', 'Luplep', 'Luzpar',
                          'Maiste', 'Pencar', 'Pencon', 'Penser', 'Phahas', 'Phlalp', 'Phldif', 'Phyemp', 'Pincon',
                          'Poasec', 'Poldav', 'Polmin', 'Pollon', 'Poljun', 'Popbal', 'Potarg', 'Psemen', 'Raccan',
                          'Rumace', 'Salsit', 'Saxfer', 'Senspp', 'Sibpro', 'Sorsit', 'Spiden', 'Trispi', 'Tsumer',
                          'Vacmem', 'Vervir', 'Vioadu', 'Xerten']

        self.engine.table = table
        self.engine.create_table()
        self.engine.insert_data_from_url(self.urls["species_plot_year"])

        # species table  produces error('utf8' codec can't decode byte 0xf6") if we do not encode('utf-8')
        self.engine.download_file(self.urls["species"], "original_MSH_SPECIES_DESCRIPTORS.csv")
        data_path = self.engine.format_filename("MSH_SPECIES_DESCRIPTORS.csv")

        old_data = os.path.normpath(self.engine.find_file("original_MSH_SPECIES_DESCRIPTORS.csv"))

        with open(old_data, 'rU') as infile, open(data_path, 'w', newline="\n")as new_data:
            for line in infile:
                line = line.encode('utf-8')
                new_data.write(line)
        infile.close()
        new_data.close()
        self.engine.auto_create_table(Table("species"),
                                      filename="MSH_SPECIES_DESCRIPTORS.csv")
        self.engine.insert_data_from_file(data_path)


SCRIPT = main()
