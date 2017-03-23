# -*- coding: UTF-8 -*-
#retriever

"""Retriever script for direct download of vertnet-amphibians data"""
from builtins import str
import os

from retriever.lib.models import Table
from retriever.lib.templates import Script
 
class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Aquatic Animal Excretion"
        self.shortname = "aquatic-animal-excretion"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.0.0'
        self.ref = "http://onlinelibrary.wiley.com/doi/10.1002/ecy.1792/abstract"
        self.urls = {
            'aquatic_animals': 'http://onlinelibrary.wiley.com/store/10.1002/ecy.1792/asset/supinfo/ecy1792-sup-0001-DataS1.zip?v=1&s=3a9094a807bbc2d03ba43045d2b72782bfb348ef'
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
        self.tags = ['Aquatic']

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

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
        if not os.path.isfile(engine.format_filename(filename)):
            engine.download_files_from_archive(self.urls[tablename], [filename], filetype="zip")

        engine.create_table()
        engine.insert_data_from_file(engine.format_filename(str(filename)))


SCRIPT = main()
