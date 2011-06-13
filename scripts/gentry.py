"""Retriever script for Alwyn H. Gentry Forest Transect Dataset

"""

import os
import sys
import zipfile
import xlrd
from retriever.lib.templates import Script
from retriever.lib.tools import ScriptTest
from retriever.lib.models import Table
from retriever.lib.excel import Excel

VERSION = '1.0.1'

TAX_GROUPS = 9756 #9819


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Alwyn H. Gentry Forest Transect Dataset"
        self.shortname = "Gentry"
        self.urls = {"stems": "http://www.mobot.org/mobot/gentry/123/all_Excel.zip",
                     "sites": "http://www.ecologicaldata.org/sites/default/files/gentry_sites_data.txt",
                     "species": "",
                     "counts": ""}
        self.tags = ["Taxon > Plants", "Spatial Scale > Global"]
        self.ref = "http://www.wlbcenter.org/gentry_data.htm"
        self.addendum = """Researchers who make use of the data in publications are requested to acknowledge Alwyn H. Gentry, the Missouri Botanical Garden, and collectors who assisted Gentry or contributed data for specific sites. It is also requested that a reprint of any publication making use of the Gentry Forest Transect Data be sent to:

Bruce E. Ponman
Missouri Botanical Garden
P.O. Box 299
St. Louis, MO 63166-0299
U.S.A. """
    def download(self, engine=None):
        Script.download(self, engine)
        
        self.engine.auto_create_table(Table("sites"), url=self.urls["sites"])
        self.engine.insert_data_from_url(self.urls["sites"])
              
        self.engine.download_file(self.urls["stems"], "all_Excel.zip")
        local_zip = zipfile.ZipFile(self.engine.format_filename("all_Excel.zip"))        
        filelist = local_zip.namelist()
        local_zip.close()        
        self.engine.download_files_from_archive(self.urls["stems"], filelist)
        
        filelist = [os.path.basename(filename) for filename in filelist]
        
        lines = []
        tax = []
        for filename in filelist:
            print "Extracting data from " + filename + "..."
            book = xlrd.open_workbook(self.engine.format_filename(filename))
            sh = book.sheet_by_index(0)
            rows = sh.nrows
            cn = {'stems': []}
            n = 0
            for c in sh.row(0):
                if not Excel.empty_cell(c):
                    cid = Excel.cell_value(c).lower()
                    # line number column is sometimes named differently
                    if cid in ["sub", "number"]:
                        cid = "line"
                    # the "number of individuals" column is named in various
                    # different ways; they always at least contain "nd"
                    if "nd" in cid:
                        cid = "count"
                    # if column is a stem, add it to the list of stems;
                    # otherwise, make note of the column name/number
                    if "stem" in cid:
                        cn["stems"].append(n)
                    else:
                        cn[cid] = n
                n += 1
            # sometimes, a data file does not contain a liana or count column
            if not "liana" in cn.keys():
                cn["liana"] = -1
            if not "count" in cn.keys():
                cn["count"] = -1
            for i in range(1, rows):
                row = sh.row(i)
                cellcount = len(row)
                # make sure the row is real, not just empty cells
                if cellcount > 4 and not Excel.empty_cell(row[0]):
                    try:
                        this_line = {}
                        
                        def format_value(s):
                            s = Excel.cell_value(s)
                            return str(s).title().replace("\\", "/")
                        
                        # get the following information from the appropriate columns
                        for i in ["line", "family", "genus", "species", 
                                  "liana", "count"]:
                            if cn[i] > -1:
                                this_line[i] = format_value(row[cn[i]])

                        this_line["stems"] = [Excel.cell_value(row[c]) 
                                              for c in cn["stems"]
                                              if not Excel.empty_cell(row[c])]
                        this_line["site"] = filename[0:-4]
                        
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
                                    this_line["species"].lower(), 
                                    id_level, 
                                    str(full_id)))
                    except:
                        raise
                        pass                    
        
        tax = sorted(tax, key=lambda group: group[0] + " " + group[1] + " " + group[2])
        unique_tax = []
        tax_dict = dict()
        tax_count = 0
        
        # Get all unique families/genera/species
        for group in tax:
            if not (group in unique_tax):
                unique_tax.append(group)
                tax_count += 1
                tax_dict[group[0:3]] = tax_count
                if tax_count % 10 == 0:
                    msg = "Generating taxonomic groups: " + str(tax_count) + " / " + str(TAX_GROUPS)
                    sys.stdout.write(msg + "\b" * len(msg))
        
        
        # Create species table
        table = Table("species", delimiter="::")
        table.columns=[("species_id"            ,   ("pk-auto",)    ),
                       ("family"                ,   ("char", 20)    ),
                       ("genus"                 ,   ("char", 20)    ),
                       ("species"               ,   ("char", 20)    ),
                       ("id_level"              ,   ("char", 10)    ),
                       ("full_id"               ,   ("bool",)       )]

        table.source = ['::'.join(group) 
                        for group in unique_tax]
        
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table()        
        
        
        # Create stems table
        table = Table("stems", delimiter="::", contains_pk=False)
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
                                      line["species"].lower())],
                            line["site"],
                            liana
                            ]
            try:
                counts.append([str(value) for value in species_info + [line["count"]]])
            except KeyError:
                pass

            for i in line["stems"]:
                stem = species_info + [i]
                stems.append([str(value) for value in stem])
            
        table.source = ['::'.join(stem) for stem in stems]
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table()
        
        
        # Create counts table
        table = Table("counts", delimiter="::", contains_pk=False)
        table.columns=[("count_id"              ,   ("pk-auto",)    ),
                       ("line"                  ,   ("int",)        ),
                       ("species_id"            ,   ("int",)        ),
                       ("site_code"             ,   ("char", 12)    ),
                       ("liana"                 ,   ("char", 10)    ),
                       ("count"                 ,   ("double",)     )]
        table.source = ['::'.join(count) for count in counts]
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table()
            
        return self.engine
    
    
class GentryTest(ScriptTest):
    def strvalue(self, value, col_num):
        value = DbTkTest.strvalue(self, value, col_num)
        if value[-3:] == ".00":
            value = value[0:len(value) - 3]
        return value
    def test_Gentry(self):
        ScriptTest.default_test(self,
                                main(),
                                [("species",
                                  "8673559a7e35f1d2925d4add6d7347f7",
                                  "species_id")
                                ],
                                include_pk = True)


SCRIPT = main()
