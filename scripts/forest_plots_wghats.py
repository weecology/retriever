# -*- coding: UTF-8 -*-
#retriever

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script
from retriever.lib.defaults import VERSION
from pkg_resources import parse_version


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Indian Forest Stand Structure and Composition (Ramesh et al. 2010)"
        self.name = "forest-plots-wghats"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.0'
        self.ref = "https://figshare.com/collections/Forest_stand_structure_and_composition_in_96_sites_" \
                   "along_environmental_gradients_in_the_central_Western_Ghats_of_India/3303531"
        self.urls = {'data': 'https://ndownloader.figshare.com/files/5617140'}
        self.citation = "B. R. Ramesh, M. H. Swaminath, Santoshgouda V. Patil, Dasappa, Raphael Pelissier, P. " \
                        "Dilip Venugopal, S. Aravajy, Claire Elouard, and S. Ramalingam. 2010. Forest stand " \
                        "structure and composition in 96 sites along environmental gradients in the central " \
                        "Western Ghats of India. Ecology 91:3118."
        self.description = "This data set reports woody plant species abundances in a network of 96 sampling " \
                           "sites spread across 22000 km2 in central Western Ghats region, Karnataka, India."
        self.keywords = ['plants', 'regional-scale', 'observational']

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value, nulls=['NA'])
        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value, missing_values=['NA'])

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        files = ["Macroplot_data_Rev.txt", "Microplot_data.txt", "Site_variables.txt", "Species_list.txt"]
        engine.download_files_from_archive(self.urls["data"], files, filetype="zip")

        # Create table species
        engine.auto_create_table(Table('species', cleanup=self.cleanup_func_table),
                                 filename="Species_list.txt")
        engine.insert_data_from_file(engine.format_filename("Species_list.txt"))

        # Create table sites
        engine.auto_create_table(Table('sites', cleanup=self.cleanup_func_table),
                                 filename="Site_variables.txt")
        engine.insert_data_from_file(engine.format_filename("Site_variables.txt"))

        # Create table microplots
        table = Table('microplots')
        table.columns = [('record_id', ('pk-auto',)), ('SpCode', ('char', '30')), ('Count', ('ct-int',))]
        table.ct_names = ['BSP1', 'BSP2', 'BSP3', 'BSP4', 'BSP5', 'BSP6', 'BSP7', 'BSP8', 'BSP9',
                          'BSP10', 'BSP11', 'BSP12', 'BSP13', 'BSP14', 'BSP15', 'BSP16', 'BSP17',
                          'BSP18', 'BSP20', 'BSP21', 'BSP22', 'BSP23', 'BSP24', 'BSP25', 'BSP26',
                          'BSP27', 'BSP28', 'BSP29', 'BSP30', 'BSP31', 'BSP33', 'BSP34', 'BSP35',
                          'BSP36', 'BSP37', 'BSP41', 'BSP42', 'BSP43', 'BSP44', 'BSP45', 'BSP46',
                          'BSP47', 'BSP48', 'BSP49', 'BSP50', 'BSP51', 'BSP52', 'BSP53', 'BSP54',
                          'BSP55', 'BSP56', 'BSP57', 'BSP58', 'BSP59', 'BSP60', 'BSP61', 'BSP62',
                          'BSP63', 'BSP64', 'BSP65', 'BSP66', 'BSP67', 'BSP68', 'BSP69', 'BSP70',
                          'BSP71', 'BSP72', 'BSP73', 'BSP74', 'BSP75', 'BSP76', 'BSP78', 'BSP79',
                          'BSP80', 'BSP82', 'BSP83', 'BSP84', 'BSP85', 'BSP86', 'BSP87', 'BSP88',
                          'BSP89', 'BSP90', 'BSP91', 'BSP92', 'BSP93', 'BSP94', 'BSP95', 'BSP96',
                          'BSP97', 'BSP98', 'BSP99', 'BSP100', 'BSP101', 'BSP102', 'BSP104']
        table.ct_column = 'PlotID'
        engine.auto_create_table(table, filename="Microplot_data.txt")
        engine.insert_data_from_file(engine.format_filename("Microplot_data.txt"))

        # Create table microplots
        table = Table('macroplots')
        table.ct_names = ['TreeGirth1', 'TreeGirth2', 'TreeGirth3', 'TreeGirth4', 'TreeGirth5']
        table.ct_column = 'Tree'
        table.columns = [('record_id', ('pk-auto',)), ('PlotID', ('char', '20')), ('SpCode', ('char', '30')),
                         ('Girth', ('ct-int',))]
        engine.auto_create_table(table, filename="Macroplot_data_Rev.txt")
        engine.insert_data_from_file(engine.format_filename("Macroplot_data_Rev.txt"))


SCRIPT = main()
