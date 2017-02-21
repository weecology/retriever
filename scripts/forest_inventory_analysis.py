#retriever
"""Retriever script for Forest Inventory and Analysis

"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()

import os

from retriever.lib.templates import Script
from retriever.lib.models import Table
from retriever import open_fr, open_fw


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Forest Inventory and Analysis"
        self.shortname = "forest-inventory-analysis"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.1'
        self.ref = "http://fia.fs.fed.us/"
        self.urls = {"main": "https://apps.fs.usda.gov/fiadb-downloads/CSV/",
                     'species': 'https://apps.fs.usda.gov/fiadb-downloads/CSV/REF_SPECIES.csv'}
        self.tags = ["plants", "continental-scale", "observational"]
        self.citation = "DATEOFDOWNLOAD. Forest Inventory and Analysis Database, St. Paul, MN: U.S. Department of Agriculture, Forest Service, Northern Research Station. [Available only on internet: http://apps.fs.fed.us/fiadb-downloads/datamart.html]"
        self.description = """WARNING: This dataset requires downloading many large files and will probably take several hours to finish installing."""
        self.addendum = """This dataset requires downloading many large files - please be patient."""

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # download and create species table
        table = Table('species')
        self.engine.auto_create_table(table, url=self.urls['species'])
        self.engine.insert_data_from_url(self.urls['species'])

        # State abbreviations with the year annual inventory began for that state
        stateslist = [('AL', 2001), ('AK', 2004), ('AZ', 2001), ('AR', 2000),
                      ('CA', 2001), ('CO', 2002), ('CT', 2003), ('DE', 2004),
                      ('FL', 2003), ('GA', 1998), ('ID', 2004), ('IL', 2001),
                      ('IN', 1999), ('IA', 1999), ('KS', 2001), ('KY', 1999),
                      ('LA', 2001), ('ME', 1999), ('MD', 2004), ('MA', 2003),
                      ('MI', 2000), ('MN', 1999), ('MO', 1999), ('MS', 2006),
                      ('MT', 2003), ('NE', 2001), ('NV', 2004), ('NH', 2002),
                      ('NJ', 2004), ('NM', 1999), ('NY', 2002), ('NC', 2003),
                      ('ND', 2001), ('OH', 2001), ('OK', 2008), ('OR', 2001),
                      ('PA', 2000), ('RI', 2003), ('SC', 1999), ('SD', 2001),
                      ('TN', 2000), ('TX', 2001), ('UT', 2000), ('VT', 2003),
                      ('VA', 1998), ('WA', 2002), ('WV', 2004), ('WI', 2000),
                      ('WY', 2000), ('PR', 2001)]

        tablelist = ["SURVEY", "PLOT", "COND", "SUBPLOT", "SUBP_COND", "TREE", "SEEDLING"]

        for table in tablelist:
            for state, year in stateslist:
                engine.download_files_from_archive(self.urls["main"] + state + "_" + table + ".ZIP",
                                                   [state + "_" + table + ".csv"])

        for table in tablelist:
            print("Scanning data for table %s..." % table)
            prep_file_name = "%s.csv" % table
            prep_file = open_fw(engine.format_filename(prep_file_name))
            this_file = open_fr(engine.format_filename(stateslist[0][0] + "_" + table + ".csv"))
            col_names = this_file.readline()
            prep_file.write(col_names)
            column_names = [col.strip('"') for col in col_names.split(',')]
            year_column = column_names.index("INVYR")
            this_file.close()

            for state, year in stateslist:
                this_file = open_fr(engine.format_filename(state + "_" + table + ".csv"))
                this_file.readline()
                for line in this_file:
                    values = line.split(',')
                    this_year = values[year_column]
                    if int(this_year) >= year:
                        prep_file.write(line)
            prep_file.close()
            engine.auto_create_table(Table(table), filename=prep_file_name)

            engine.insert_data_from_file(engine.format_filename(prep_file_name))

            try:
                os.remove(engine.format_filename(prep_file_name))
            except:
                pass

        return engine


SCRIPT = main()
