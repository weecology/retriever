#retriever
"""Retriever script for National Phenology Network data
"""
from future import standard_library
standard_library.install_aliases()
from builtins import range

import os
import urllib.request, urllib.parse, urllib.error
import zipfile
from decimal import Decimal
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, no_cleanup, correct_invalid_value

VERSION = '0.5'


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "USA National Phenology Network"
        self.shortname = "NPN"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.0'
        self.ref = "http://www.usanpn.org/results/data"
        self.tags = ["Data Type > Phenology", "Spatial Scale > Continental"]
        self.description = "The data set was collected via Nature's Notebook phenology observation program (2009-present), and (2) Lilac and honeysuckle data (1955-present)"
        self.citation = "Schwartz, M. D., Ault, T. R., & J. L. Betancourt, 2012: Spring Onset Variations and Trends in the Continental USA: Past and Regional Assessment Using Temperature-Based Indices. International Journal of Climatology (published online, DOI: 10.1002/joc.3625)."
    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        engine = self.engine

        taxa = ('Plant', 'Animal')

        for tax in taxa:
            table = Table(tax.lower() + 's', delimiter=',', header_rows = 3, pk='record_id', contains_pk=True)

            columns =     [("record_id"             ,   ("pk-int",)     ),
                           ("station_id"            ,   ("int",)        ),
                           ("obs_date"              ,   ("char",)       ),
                           ("ind_id"                ,   ("int",)        ),
                           ("sci_name"              ,   ("char",)       ),
                           ("com_name"              ,   ("char",)       ),
                           ("kingdom"               ,   ("char",)       ),
                           ("pheno_cat"             ,   ("char",)       ),
                           ("pheno_name"            ,   ("char",)       ),
                           ("pheno_status"          ,   ("char",)       ),
                           ("lat"                   ,   ("double",)     ),
                           ("lon"                   ,   ("double",)     ),
                           ("elevation"             ,   ("int",)        ),
                           ("network_name"          ,   ("char",)       )]
            table.columns = columns

            engine.table = table
            engine.create_table()

            base_url = 'http://www.usanpn.org/getObs/observations/'
            years = list(range(2009, 2013))

            for year in years:
                if year == 2009 and tax == 'Animal': continue

                url = base_url + 'get%s%sDataNoDefinitions' % (year, tax)

                filename = '%s_%s.csv' % (tax, year)
                engine.download_file(url, filename)

                engine.insert_data_from_file(engine.find_file(filename))

        return engine


SCRIPT = main()
