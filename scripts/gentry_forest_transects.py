#retriever
"""Retriever script for Alwyn H. Gentry Forest Transect Dataset

"""
from __future__ import print_function
# from __future__ import unicode_literals
from builtins import str
from builtins import range

import os
import sys
import zipfile
import xlrd
from retriever.lib.templates import Script
from retriever.lib.models import Table
from retriever.lib.excel import Excel
from retriever import open_fr, open_fw, open_csvw, to_str

TAX_GROUPS = 9756 #9819


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Alwyn H. Gentry Forest Transect Dataset"
        self.shortname = "gentry-forest-transects"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.3.1'
        self.urls = {"stems": "http://www.mobot.org/mobot/gentry/123/all_Excel.zip",
                     "sites": "https://ndownloader.figshare.com/files/5515373",
                     "species": "",
                     "counts": ""}
        self.tags = ["plants", "global-scale", "observational"]
        self.ref = "http://www.mobot.org/mobot/research/gentry/welcome.shtml"
        self.citation = "Phillips, O. and Miller, J.S., 2002. Global patterns of plant diversity: Alwyn H. Gentry's forest transect data set. Missouri Botanical Press."
        self.addendum = """Researchers who make use of the data in publications are requested to acknowledge Alwyn H. Gentry, the Missouri Botanical Garden, and collectors who assisted Gentry or contributed data for specific sites. It is also requested that a reprint of any publication making use of the Gentry Forest Transect Data be sent to:

Bruce E. Ponman
Missouri Botanical Garden
P.O. Box 299
St. Louis, MO 63166-0299
U.S.A. """

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.auto_create_table(Table("sites"), url=self.urls["sites"], filename='gentry_sites.csv')
        self.engine.insert_data_from_url(self.urls["sites"])

        self.engine.download_file(self.urls["stems"], "all_Excel.zip")
        local_zip = zipfile.ZipFile(self.engine.format_filename("all_Excel.zip"))
        filelist = local_zip.namelist()
        local_zip.close()
        self.engine.download_files_from_archive(self.urls["stems"], filelist)

        filelist = [os.path.basename(filename) for filename in filelist]

        # Currently all_Excel.zip is missing CURUYUQU.xls
        # Download it separately and add it to the file list
        if not self.engine.find_file('CURUYUQU.xls'):
            self.engine.download_file("http://www.mobot.org/mobot/gentry/123/samerica/CURUYUQU.xls", "CURUYUQU.xls")
            filelist.append('CURUYUQU.xls')

        lines = []
        tax = []
        for filename in filelist:
            print("Extracting data from " + filename + "...")
            book = xlrd.open_workbook(self.engine.format_filename(filename))
            sh = book.sheet_by_index(0)
            rows = sh.nrows
            cn = {'stems': []}
            n = 0
            for colnum, c in enumerate(sh.row(0)):
                if not Excel.empty_cell(c):
                    cid = c.value.lower().strip()
                    # line number column is sometimes named differently
                    if cid in ["sub", "number"]:
                        cid = "line"
                    # the "number of individuals" column is named in various
                    # different ways; they always at least contain "nd"
                    if "nd" in cid:
                        cid = "count"
                    # in QUIAPACA.xls the "number of individuals" column is
                    # misnamed "STEMDBH" just like the stems columns, so weep
                    # for the state of scientific data and then fix manually
                    if filename == "QUIAPACA.xls" and colnum == 13:
                        cid = "count"

                    # if column is a stem, add it to the list of stems;
                    # otherwise, make note of the column name/number
                    if "stem" in cid or "dbh" in cid:
                        cn["stems"].append(n)
                    else:
                        cn[cid] = n
                n += 1
            # sometimes, a data file does not contain a liana or count column
            if not "liana" in list(cn.keys()):
                cn["liana"] = -1
            if not "count" in list(cn.keys()):
                cn["count"] = -1
            for i in range(1, rows):
                row = sh.row(i)
                cellcount = len(row)
                # make sure the row is real, not just empty cells
                if not all(Excel.empty_cell(cell) for cell in row):
                    try:
                        this_line = {}

                        # get the following information from the appropriate columns
                        for i in ["line", "family", "genus", "species",
                                  "liana", "count"]:
                            if cn[i] > -1:
                                if row[cn[i]].ctype != 2:
                                    # if the cell type(ctype) is not a number
                                    this_line[i] = row[cn[i]].value.lower().strip().replace("\\", "/").replace('"', '')
                                else:
                                    this_line[i] = row[cn[i]].value
                                if this_line[i] == '`':
                                    this_line[i] = 1
                        this_line["stems"] = [row[c]
                                              for c in cn["stems"]
                                              if not Excel.empty_cell(row[c])]
                        this_line["site"] = filename[0:-4]

                        # Manually correct CEDRAL data, which has a single line
                        # that is shifted by one to the left starting at Liana
                        if this_line["site"] == "CEDRAL" and type(this_line["liana"]) == float:
                            this_line["liana"] = ""
                            this_line["count"] = 3
                            this_line["stems"] = [2.5, 2.5, 30, 18, 25]

                        lines.append(this_line)

                        # Check how far the species is identified
                        full_id = 0
                        if len(this_line["species"]) < 3:
                            if len(this_line["genus"]) < 3:
                                id_level = "family"
                            else:
                                id_level = "genus"
                        else:
                            id_level = "species"
                            full_id = 1
                        tax.append((this_line["family"],
                                    this_line["genus"],
                                    this_line["species"],
                                    id_level,
                                    str(full_id)))
                    except:
                        raise
                        pass

        tax = sorted(tax, key=lambda group: group[0] + " " + group[1] + " " + group[2])
        unique_tax = []
        tax_dict = {}
        tax_count = 0

        # Get all unique families/genera/species
        print("\n")
        for group in tax:
            if not (group in unique_tax):
                unique_tax.append(group)
                tax_count += 1
                tax_dict[group[0:3]] = tax_count
                if tax_count % 10 == 0:
                    msg = "Generating taxonomic groups: " + str(tax_count) + " / " + str(TAX_GROUPS)
                    sys.stdout.flush()
                    sys.stdout.write(msg + "\b" * len(msg))
        print("\n")
        # Create species table
        table = Table("species", delimiter=",")
        table.columns=[("species_id"            ,   ("pk-int",)    ),
                       ("family"                ,   ("char", )    ),
                       ("genus"                 ,   ("char", )    ),
                       ("species"               ,   ("char", )    ),
                       ("id_level"              ,   ("char", 10)    ),
                       ("full_id"               ,   ("int",)       )]

        data = [[str(tax_dict[group[:3]])] + ['"%s"' % g for g in group]
                for group in unique_tax]
        table.pk = 'species_id'
        table.contains_pk = True

        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table(data)

        # Create stems table
        table = Table("stems", delimiter=",")
        table.columns=[("stem_id"               ,   ("pk-auto",)    ),
                       ("line"                  ,   ("int",)        ),
                       ("species_id"            ,   ("int",)        ),
                       ("site_code"             ,   ("char", 12)    ),
                       ("liana"                 ,   ("char", 10)    ),
                       ("stem"                  ,   ("double",)     )]
        stems = []
        counts = []
        for line in lines:
            try:
                liana = line["liana"]
            except KeyError:
                liana = ""
            species_info = [line["line"],
                            tax_dict[(line["family"],
                                      line["genus"],
                                      line["species"])],
                            line["site"],
                            liana
                            ]
            try:
                counts.append([value for value in species_info + [line["count"]]])
            except KeyError:
                pass

            for i in line["stems"]:
                stem = species_info + [str(i)]
                stems.append(stem)

        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table(stems)

        # Create counts table
        table = Table("counts", delimiter=",", contains_pk=False)
        table.columns=[("count_id"              ,   ("pk-auto",)    ),
                       ("line"                  ,   ("int",)        ),
                       ("species_id"            ,   ("int",)        ),
                       ("site_code"             ,   ("char", 12)    ),
                       ("liana"                 ,   ("char", 10)    ),
                       ("count"                 ,   ("double",)     )]
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table(counts)

        return self.engine
SCRIPT = main()
