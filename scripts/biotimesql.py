# -*- coding: utf-8 -*-
#retriever

import csv
from pkg_resources import parse_version

from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw, open_csvw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Commercial Fisheries Monthly Trade Data by Product, Country/Association"
        self.name = "biotimesql"
        self.retriever_minimum_version = "2.2.0"
        self.urls = {
            "sql_file": "https://zenodo.org/record/2602708/files/BioTIMESQL02_04_2018.sql?download=1",
        }
        self.version = "1.0.1"
        self.ref = "https://zenodo.org/record/1095628#.WskN7dPwYyn"
        self.citation = "Dornelas M, Antão LH, Moyes F, et al. BioTIME: A database of biodiversity time series for the Anthropocene. Global Ecology & Biogeography. 2018; 00:1 - 26. https://doi.org/10.1111/geb.12729."
        self.description = "The BioTIME database has species identities and abundances in ecological assemblages through time."
        self.keywords = ["Time series", "Anthropocene", "Global"]
        self.licenses = [{"name": "CC BY 4.0"}]
        self.encoding = "latin1"

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        original_sql_file = "BioTIMESQL02_04_2018.sql"
        engine.download_file(self.urls["sql_file"], original_sql_file)
        sql_data = open_fr(self.engine.format_filename(original_sql_file))

        set_open = False
        csv_writer = None
        csv_file = None
        table_name = None
        NULL = None
        for line in sql_data:
            table_indicator = "-- Table structure for table "
            if line.startswith(table_indicator):
                st = line[len(table_indicator):].replace("`", "")
                table_name = st.strip()
                current_file_process = table_name
                current_file_open = current_file_process
                if set_open and not current_file_process == current_file_open:
                    csv_file.close()
                    set_open = False
                else:
                    out_file = "{name}.csv".format(name=table_name)
                    csv_file = open_fw(engine.format_filename(out_file))
                    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                    set_open = True

            if line.startswith("INSERT INTO `{table_name}`".format(table_name=table_name)):
                row_val = line[line.index("VALUES (") + 8:-3]
                table_rows = row_val.replace("\r\n","").split("),(")
                for i_row in table_rows:
                    v = eval('[' + str(i_row) + ']')
                    csv_writer.writerows([v])
        if csv_file:
            csv_file.close()

        # Create abundance table
        table = Table("ID_ABUNDANCE", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_ABUNDANCE", ("int",)),
            ("ABUNDANCE_TYPE", ("char", "100")),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("abundance.csv"))

        # Create allrawdata table
        table = Table("allrawdata", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_ALL_RAW_DATA", ("int",)),
            ("ABUNDANCE", ("double",)),
            ("BIOMASS", ("double",)),
            ("ID_SPECIES", ("int",)),
            ("SAMPLE_DESC", ("char", 200)),
            ("PLOT", ("char", 150)),
            ("LATITUDE", ("double",)),
            ("LONGITUDE", ("double",)),
            ("DEPTH", ("double",)),
            ("DAY", ("int",)),
            ("MONTH", ("int",)),
            ("YEAR", ("int",)),
            ("STUDY_ID", ("int",)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("allrawdata.csv"))

        # Create biomass table
        table = Table("biomass", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [("ID_BIOMASS", ("int",)), ("BIOMASS_TYPE", ("char", "100"))]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("biomass.csv"))

        # Create citation1 table
        table = Table("citation1", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_CITATION1", ("int",)),
            ("STUDY_ID", ("int",)),
            ("CITATION_LINE", ("char",)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("citation1.csv"))

        # Create contacts table
        table = Table("contacts", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_CONTACTS", ("int",)),
            ("STUDY_ID", ("int",)),
            ("CONTACT_1", ("char", 500)),
            ("CONTACT_2", ("char", 500)),
            ("CONT_1_MAIL", ("char", 60)),
            ("CONT_2_MAIL", ("char", 60)),
            ("LICENSE", ("char", 200)),
            ("WEB_LINK", ("char", 200)),
            ("DATA_SOURCE", ("char", 250)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("contacts.csv"))

        # Create countries table
        table = Table("countries", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [("COUNT_ID", ("int",)), ("COUNTRY_NAME", ("char", 200))]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("countries.csv"))

        # Create curation table
        table = Table("curation", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_CURATION", ("int",)),
            ("STUDY_ID", ("int",)),
            ("LINK_ID", ("int",)),
            ("COMMENTS", ("char",)),
            ("DATE_STUDY_ADDED", ("char", 50)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("curation.csv"))

        # Create datasets table
        table = Table("datasets", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_DATASETS", ("int",)),
            ("STUDY_ID", ("int",)),
            ("TAXA", ("char", 50)),
            ("ORGANISMS", ("char", 200)),
            ("TITLE", ("char",800)),
            ("AB_BIO", ("char", 2)),
            ("HAS_PLOT", ("char", 10)),
            ("DATA_POINTS", ("char",)),
            ("START_YEAR", ("char",)),
            ("END_YEAR", ("char",)),
            ("CENT_LAT", ("double",)),
            ("CENT_LONG", ("double",)),
            ("NUMBER_OF_SPECIES", ("char",)),
            ("NUMBER_OF_SAMPLES", ("char",)),
            ("NUMBER_LAT_LONG", ("char",)),
            ("TOTAL", ("char",)),
            ("GRAIN_SIZE_TEXT", ("char",)),
            ("GRAIN_SQ_KM", ("double",)),
            ("AREA_SQ_KM", ("double",)),
            ("AB_TYPE", ("char", )),
            ("BIO_TYPE", ("char",)),
            ("SAMPLE_TYPE", ("char",)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("datasets.csv"))

        # Create downloads table
        table = Table("downloads", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("D_ID", ("int",)),
            ("STUDY", ("char", 25)),
            ("NAME", ("char", 150)),
            ("EMAIL", ("char", 150)),
            ("COUNTRY", ("char", 200)),
            ("ROLE", ("char", 150)),
            ("PURPOSE", ("char", 500)),
            ("LOCATION", ("char", 250)),
            ("DATE_STAMP", ("char",)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("downloads.csv"))

        # Create methods table
        table = Table("methods", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_METHODS", ("int",)),
            ("STUDY_ID", ("int",)),
            ("METHODS", ("char",)),
            ("SUMMARY_METHODS", ("char", 500)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("methods.csv"))

        # Create sample table
        table = Table("sample", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_SAMPLE", ("int",)),
            ("ID_TREAT", ("int",)),
            ("SAMPLE_DESC_NAME", ("char", 200)),
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("sample.csv"))

        # Create site table
        table = Table("site", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_SITE", ("int",)),
            ("STUDY_ID", ("int",)),
            ("REALM", ("char", 11)),
            ("CLIMATE", ("char", 20)),
            ("GENERAL_TREAT", ("char", 200)),
            ("TREATMENT", ("char", 200)),
            ("TREAT_COMMENTS", ("char", 250)),
            ("TREAT_DATE", ("char", 100)),
            ("CEN_LATITUDE", ("double",)),
            ("CEN_LONGITUDE", ("double",)),
            ("HABITAT", ("char", 100)),
            ("PROTECTED_AREA", ("char", 50)),
            ("AREA", ("double",)),
            ("BIOME_MAP", ("char", 500))
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("site.csv"))

        # Create species table
        table = Table("species", delimiter=",", header_rows=0, contains_pk=False)
        table.columns = [
            ("ID_SPECIES", ("int",)),
            ("GENUS", ("char", 100)),
            ("SPECIES", ("char", 100)),
            ("GENUS_SPECIES", ("char", 100))
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(engine.format_filename("species.csv"))


SCRIPT = main()
