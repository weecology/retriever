# -*- coding: UTF-8 -*-
#retriever

"""Retriever script for direct download of vertnet-amphibians data"""
from builtins import str
import os

from retriever.lib.models import Table
from retriever.lib.templates import Script
from pkg_resources import parse_version
try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Aquatic Animal Excretion"
        self.name = "aquatic-animal-excretion"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.1.2'
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1792/abstract"
        self.urls = {
            'aquatic_animals': 'https://esajournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Fecy.1792&attachmentId=123472854'
        }
        self.citation = "Vanni, M. J., McIntyre, P. B., Allen, D., Arnott, D. L., Benstead, J. P., Berg, D. J., " \
                        "Brabrand, Å., Brosse, S., Bukaveckas, P. A., Caliman, A., Capps, K. A., Carneiro, L. S., " \
                        "Chadwick, N. E., Christian, A. D., Clarke, A., Conroy, J. D., Cross, W. F., Culver, D. A., " \
                        "Dalton, C. M., Devine, J. A., Domine, L. M., Evans-White, M. A., Faafeng, B. A., " \
                        "Flecker, A. S., Gido, K. B., Godinot, C., Guariento, R. D., Haertel-Borer, S., Hall, " \
                        "R. O., Henry, R., Herwig, B. R., Hicks, B. J., Higgins, K. A., Hood, J. M., Hopton, M. E., " \
                        "Ikeda, T., James, W. F., Jansen, H. M., Johnson, C. R., Koch, B. J., Lamberti, G. A., " \
                        "Lessard-Pilon, S., Maerz, J. C., Mather, M. E., McManamay, R. A., Milanovich, J. R., " \
                        "Morgan, D. K. J., Moslemi, J. M., Naddafi, R., Nilssen, J. P., Pagano, M., Pilati, A., " \
                        "Post, D. M., Roopin, M., Rugenski, A. T., Schaus, M. H., Shostell, J., Small, G. E., " \
                        "Solomon, C. T., Sterrett, S. C., Strand, O., Tarvainen, M., Taylor, J. M., Torres-Gerald, " \
                        "L. E., Turner, C. B., Urabe, J., Uye, S.-I., Ventelä, A.-M., Villeger, S., Whiles, M. R., " \
                        "Wilhelm, F. M., Wilson, H. F., Xenopoulos, M. A. and Zimmer, K. D. (2017), " \
                        "A global database of nitrogen and phosphorus excretion rates of aquatic animals. " \
                        "Ecology. Accepted Author Manuscript. doi:10.1002/ecy.1792"
        self.description = "Dataset containing the nutrient cycling rates of individual animals."
        self.keywords = ['Aquatic']

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        filenames = ['Aquatic_animal_excretion_data.csv', 'Aquatic_animal_excretion_variable_descriptions.csv']
        for file_paths in filenames:
            if not os.path.isfile(engine.format_filename(file_paths)):
                engine.download_files_from_archive(self.urls["aquatic_animals"], filenames, filetype="zip")

        # processing Aquatic_animal_excretion_data.csv
        filename = 'Aquatic_animal_excretion_data.csv'
        tablename = 'aquatic_animals'
        table = Table(str(tablename), delimiter=',')
        table.columns = [
            ("index", ("pk-int",)),
            ("sourcenumber", ("int",)),
            ("sourcename", ("char",)),
            ("speciesname", ("char",)),
            ("speciescode", ("char",)),
            ("invert/vert", ("char",)),
            ("phylum", ("char",)),
            ("class", ("char",)),
            ("order", ("char",)),
            ("family", ("char",)),
            ("trophicgild", ("char",)),
            ("drymass", ("double",)),
            ("logdrymass", ("double",)),
            ("ecosystemtype", ("char",)),
            ("energysource", ("char",)),
            ("habitat", ("char",)),
            ("residentecosystem", ("char",)),
            ("temperature", ("double",)),
            ("nexcretionrate", ("double",)),
            ("pexcretionrate", ("double",)),
            ("lognexcretionrate", ("double",)),
            ("logpexcretionrate", ("double",)),
            ("incubationtime", ("double",)),
            ("nform", ("char",)),
            ("pform", ("char",)),
            ("bodyc", ("double",)),
            ("bodyn", ("double",)),
            ("bodyp", ("double",)),
            ("bodyc:n", ("double",)),
            ("bodyc:p", ("double",)),
            ("bodyn:p", ("double",)),
            ("bodydatasource", ("char",)),
            ("datasource", ("char",)),
            ("dataproviders", ("char",))]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(str(filename)))

        # processing Aquatic_animal_excretion_variable_descriptions.csv
        filename = 'Aquatic_animal_excretion_variable_descriptions.csv'
        tablename = 'variable_descriptions'
        table = Table(str(tablename), delimiter=',')
        table.columns = [
            ("Column", ("char",)),
            ("Variable", ("char",)),
            ("Description", ("char",)),
            ("Data Class", ("char",)),
            ("Units", ("char",)),
            ("Minimum_value", ("char",)),
            ("Maximum_value", ("char",)),
            ("Possible_values", ("char",)),
            ("Missing_data_symbol", ("char",)),
            ("Notes", ("char",))]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(str(filename)))


SCRIPT = main()
