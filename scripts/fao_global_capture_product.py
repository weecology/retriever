# -*- coding: UTF-8 -*-
# retriever
from __future__ import absolute_import
from __future__ import print_function

import sys
from imp import reload

import xlrd

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    try:
        from retriever.lib.tools import open_fw, open_csvw, to_str
    except ImportError:
        from retriever.lib.scripts import open_fw, open_csvw, to_str
except ImportError:
    from retriever import open_fw, open_csvw, to_str

reload(sys)
if hasattr(sys, "setdefaultencoding"):
    sys.setdefaultencoding("UTF-8")


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = (
            "Commercial Fisheries Monthly Trade Data by Product, Country/Association"
        )
        self.name = "fao-global-capture-product"
        self.retriever_minimum_version = "2.1.dev"
        self.urls = {
            "capture": "http://www.fao.org/fishery/static/Data/Capture_2018.1.2.zip"
        }
        self.version = "1.0.0"
        self.ref = "http://www.fao.org/fishery/statistics/global-capture-production/"
        self.citation = (
            "FAO. 2018. FAO yearbook. Fishery and Aquaculture Statistics "
            "2016/FAO annuaire. Statistiques des pêches et de l'aquaculture "
            "2016/FAO anuario. Estadísticas de pesca y acuicultura 2016. "
            "Rome/Roma. 104pp."
        )
        self.description = (
            "Commercial Fisheries statistics provides a summary of "
            "commercial fisheries product data by individual country."
        )
        self.keywords = ["Fish", "Fisheries"]
        self.cleanup_func_table = Cleanup(correct_invalid_value, missingValues=["-"])
        self.encoding = "utf-8"

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        engine.download_files_from_archive(self.urls["capture"], archive_type="zip")

        # Convert xlsx to csv.
        xlsx_file = self.engine.format_filename("DSD_FI_CAPTURE.xlsx")
        file_path = self.engine.format_filename("DSD_CAPTURE.csv")
        book = xlrd.open_workbook(xlsx_file)
        sh = book.sheet_by_index(0)
        rows = sh.nrows

        # Creating data files
        new_data = open_fw(file_path)
        csv_writer = open_csvw(new_data)
        csv_writer.writerow(
            [
                "Order",
                "Concept_id",
                "Role_Type",
                "Codelist_id",
                "Codelist_Code_id",
                "Description",
            ]
        )

        for index in range(2, rows):
            row = sh.row(index)
            # Get each row and format the sell value.
            # Data starts at index 2
            row_as_list = [to_str(column_value.value) for column_value in row]
            csv_writer.writerow(row_as_list)
        new_data.close()

        file_names = [
            ("CL_FI_UNIT.csv", "unit_data"),
            ("CL_FI_WATERAREA_GROUPS.csv", "waterarea_groups"),
            ("DSD_CAPTURE.csv", "dsd_capture_data"),
            ("CL_FI_SPECIES_GROUPS.csv", "species_group"),
        ]

        for (filename, tablename) in file_names:
            data_path = self.engine.format_filename(filename)
            table = Table(tablename, delimiter=",", cleanup=self.cleanup_func_table)
            self.engine.auto_create_table(table, filename=filename)
            self.engine.insert_data_from_file(data_path)

        # File CL_FI_COUNTRY_GROUPS.csv has multi encoding
        file_names_encoded = [("CL_FI_COUNTRY_GROUPS.csv", "country_groups")]
        for (filename, tablename) in file_names_encoded:
            data_path = self.engine.format_filename(filename)
            table = Table(tablename, delimiter=",", cleanup=self.cleanup_func_table)
            table.columns = [
                ("UN_Code", ("int",)),
                ("Identifier", ("int",)),
                ("ISO2_Code", ("char", "5")),
                ("ISO3_Code", ("char", "5")),
                ("Name_En", ("char", "50")),
                ("Name_Fr", ("char", "50")),
                ("Name_Es", ("char", "50")),
                ("Name_Ar", ("char", "120")),
                ("Name_Cn", ("char", "90")),
                ("Name_Ru", ("char", "150")),
                ("Official_Name_En", ("char", "70")),
                ("Official_Name_Fr", ("char", "70")),
                ("Official_Name_Es", ("char", "70")),
                ("Official_Name_Ar", ("char", "1100")),
                ("Official_Name_Cn", ("char", "70")),
                ("Official_Name_Ru", ("char", "130")),
                ("Continent_Group", ("char", "15")),
                ("EcoClass_Group", ("char", "50")),
                ("GeoRegion_Group", ("char", "30")),
            ]
            self.engine.auto_create_table(table, filename=filename)
            self.engine.insert_data_from_file(data_path)

            # TS_FI_CAPTURE is
            file_names_encoded = [("TS_FI_CAPTURE.csv", "ts_capture_data")]
            for (filename, tablename) in file_names_encoded:
                data_path = self.engine.format_filename(filename)
                table = Table(tablename, delimiter=",", cleanup=self.cleanup_func_table)
                table.columns = [
                    ("COUNTRY", ("int",)),
                    ("FISHING_AREA", ("int",)),
                    ("SPECIES", ("char", "10")),
                    ("YEAR", ("int",)),
                    ("UNIT", ("char", "5")),
                    ("QUANTITY", ("double",)),
                    ("SYMBOL", ("char", "4")),
                ]
                self.engine.auto_create_table(table, filename=filename)
                self.engine.insert_data_from_file(data_path)


SCRIPT = main()
