#retriever
"""Retriever script for National Phenology Network data
The dataset contains observation data retrieved from start date to current date
date format YYYY-MM-DD
Data having a value -9999 or "-9999" are considered 'null' or 'empty
Data from the API is xml having both taxa(plantae and animalia)
"""
from future import standard_library

standard_library.install_aliases()
from builtins import str

<<<<<<< HEAD
import xml.etree.ElementTree as ET
import datetime

from retriever.lib.templates import Script
from retriever.lib.models import Table
from retriever import open_fr, open_fw, open_csvw, DATA_WRITE_PATH
=======
import os
import urllib.request, urllib.parse, urllib.error
import zipfile
from decimal import Decimal
from retriever.lib.templates import Script
from retriever.lib.models import Table, Cleanup, no_cleanup, correct_invalid_value
from pkg_resources import parse_version
import xml.etree.ElementTree as ET
import datetime
from retriever import open_fr, open_fw, open_csvw, DATA_WRITE_PATH, VERSION
from pkg_resources import parse_version
>>>>>>>     Updated internal variable names to match that of datapackage spec #765


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "USA National Phenology Network"
        self.name = "NPN"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '2.0.0'
        self.ref = "http://www.usanpn.org/results/data"
        self.keywords = ["Data Type > Phenology", "Spatial Scale > Continental"]
        self.description = "The data set was collected via Nature's Notebook phenology observation program (2009-present), and (2) Lilac and honeysuckle data (1955-present)"
        self.citation = "Schwartz, M. D., Ault, T. R., & J. L. Betancourt, 2012: Spring Onset Variations and Trends in the Continental USA: Past and Regional Assessment Using Temperature-Based Indices. International Journal of Climatology (published online, DOI: 10.1002/joc.3625)."

<<<<<<< HEAD
=======
        if parse_version(VERSION) < parse_version("2.1.dev"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

>>>>>>>     Updated internal variable names to match that of datapackage spec #765
    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        engine = self.engine
        csv_files = []
        request_src = "http://www.data-retriever.org/"
        base_url = "http://www.usanpn.org/npn_portal/observations/getObservations.xml?start_date={startYear}&end_date={endYear_date}&request_src={request_src}"
        header_values = ["observation_id",
                         "update_datetime",
                         "site_id",
                         "latitude",
                         "longitude",
                         "elevation_in_meters",
                         "state",
                         "species_id",
                         "genus",
                         "species",
                         "common_name",
                         "kingdom",
                         "individual_id",
                         "phenophase_id",
                         "phenophase_description",
                         "observation_date",
                         "day_of_year",
                         "phenophase_status",
                         "intensity_category_id",
                         "intensity_value",
                         "abundance_value"
                         ]

        columns = [("record_id", ("pk-auto",)),
                   ("observation_id", ("int",)),  # subsequently refered to as "status record"
                   ("update_datetime", ("char",)),
                   ("site_id", ("int",)),
                   ("latitude", ("double",)),
                   ("longitude", ("double",)),
                   ("elevation_in_meters", ("char",)),
                   ("state", ("char",)),
                   ("species_id", ("int",)),
                   ("genus", ("char",)),
                   ("species", ("char",)),
                   ("common_name", ("char",)),
                   ("kingdom", ("char",)),  # skip kingdom
                   ("individual_id", ("char",)),
                   ("phenophase_id", ("int",)),
                   ("phenophase_description", ("char",)),
                   ("observation_date", ("char",)),
                   ("day_of_year", ("char",)),
                   ("phenophase_status", ("char",)),
                   ("intensity_category_id", ("char",)),
                   ("intensity_value", ("char",)),
                   ("abundance_value", ("char",))
                   ]

        start_date = datetime.date(2009, 1, 1)
        end_date = datetime.date.today()

        while start_date < end_date:
            to_date = start_date + datetime.timedelta(90)
            if to_date >= end_date:
                data_url = base_url.format(startYear=str(start_date), endYear_date=str(end_date),
                                           request_src=request_src)
            else:
                data_url = base_url.format(startYear=str(start_date), endYear_date=str(to_date),
                                           request_src=request_src)

            xml_file_name = '{}'.format(start_date) + ".xml"
            engine.download_file(data_url, xml_file_name)

            # Create csv files for 3 months
            csv_observation = '{}'.format(start_date) + ".csv"
            csv_files.append(csv_observation)
            csv_buff = open_fw(engine.format_filename(csv_observation))
            csv_writer = open_csvw(csv_buff)

            csv_writer.writerow(header_values)

            # Parse xml to read data
            file_read = ""
            fname = DATA_WRITE_PATH.strip('{dataset}') + 'NPN/' + xml_file_name
            with open(fname, 'r') as fp1:
              file_read = fp1.read()

            root = ET.fromstring(file_read)

            for elements in root:
                index_map = {val: i for i, val in enumerate(header_values)}
                diction = sorted(elements.attrib.items(), key=lambda pair: index_map[pair[0]])
                csv_writer.writerow([x[1] for x in diction])

            csv_buff.close()
            start_date = to_date + datetime.timedelta(1)

        # Create table
        table = Table('obsercations', delimiter=',', pk='record_id', contains_pk=True)
        table.columns = columns
        engine.table = table
        engine.create_table()
        for data_file in csv_files:
            engine.insert_data_from_file(engine.find_file(data_file))
        return engine

SCRIPT = main()
