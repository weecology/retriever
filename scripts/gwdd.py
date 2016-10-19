#retriever
"""Retriever script for Zanne et al. Global wood density database.

"""
from builtins import str
from builtins import range

import os
import sys
import xlrd
from retriever.lib.templates import Script
from retriever.lib.models import Table
from retriever.lib.excel import Excel



class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Zanne et al. Global wood density database."
        self.shortname = "GWDD"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.0'
        self.urls = {"GWDD": "http://datadryad.org/bitstream/handle/10255/dryad.235/GlobalWoodDensityDatabase.xls?sequence=1"}
        self.tags = ["Taxon > Plants", "Spatial Scale > Global",
                     "Data Type > Observational"]
        self.ref = "http://datadryad.org/resource/doi:10.5061/dryad.234"
        self.description = "A collection  and collation of data on the major wood functional traits, including the largest wood density database to date (8412 taxa), mechanical strength measures and anatomical features, as well as clade-specific features such as secondary chemistry."
        self.citation = "Chave J, Coomes DA, Jansen S, Lewis SL, Swenson NG, Zanne AE (2009) Towards a worldwide wood economics spectrum. Ecology Letters 12(4): 351-366. http://dx.doi.org/10.1111/j.1461-0248.2009.01285.x"
        self.addendum = """ *Correspondence for updates to the database: G.Lopez-Gonzalez@leeds.ac.uk
        For descriptions of the database, see Chave et al. 2009. Towards a worldwide wood economics spectrum. Ecology Letters. Identifier: http://hdl.handle.net/10255/dryad.234

        Below we list the rules of use for the Global wood density database. 
        These are developed based on the rules of use for the Glopnet dataset (www.nature.com/nature/journal/v428/n6985/full/nature02403.html) and Cedar Creek LTER and Related Data (http://www.lter.umn.edu/cgi-bin/register). 
        If you would like to use the Global wood density database, we request that you:
        1. Notify the main address of correspondence (Gaby Lopez-Gonzalo) if you plan to use the database in a publication.
        2. Provide recognition of the efforts of this group in the assembly of the data by using the citation for the database above.
        3. Recognize that these data were assembled by the group for various analyses and research questions. If any of these uses overlap with your interests, you recognize that group has precedence in addressing these questions."""

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        self.engine.download_file(self.urls["GWDD"], "GlobalWoodDensityDatabase.xls")
        filename = os.path.basename("GlobalWoodDensityDatabase.xls")

        book = xlrd.open_workbook(self.engine.format_filename(filename))
        sh = book.sheet_by_index(1)
        rows = sh.nrows

        #Creating data table
        lines = []
        for i in range(1, rows):
            row = sh.row(i)
            if not all(Excel.empty_cell(cell) for cell in row):
                this_line = {}
                def format_value(s):
                    s = Excel.cell_value(s)
                    return str(s).title().replace("\\", "/").replace('"', '')
                for num, label in enumerate(["Number", "Family", "Binomial", "Wood_Density",
                            "Region", "Reference_Number"]):
                    this_line[label] = format_value(row[num])
                lines.append(this_line)

        table = Table("data", delimiter="\t")
        table.columns=[("Number"                ,   ("pk-int",) ),
                       ("Family"                ,   ("char",)   ),
                       ("Binomial"              ,   ("char",)   ),
                       ("Wood_Density"          ,   ("double",) ),
                       ("Region"                ,   ("char",)   ),
                       ("Reference_Number"      ,   ("int",)    )]
        table.pk = 'Number'
        table.contains_pk = True

        gwdd = []
        for line in lines:
            gwdd_data = [line["Number"],
                         line["Family"],
                         line["Binomial"],
                         line["Wood_Density"],
                         line["Region"],
                         line["Reference_Number"]]
            gwdd.append(gwdd_data)

        data = ['\t'.join(gwdd_line) for gwdd_line in gwdd]
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table(data)

        #Creating reference table
        lines = []
        sh = book.sheet_by_index(2)
        rows = sh.nrows
        for i in range(1, rows):
            row = sh.row(i)
            if not all(Excel.empty_cell(cell) for cell in row):
                this_line = {}
                def format_value(s):
                    s = Excel.cell_value(s)
                    return str(s).title().replace("\\", "/").replace('"', '')
                for num, label in enumerate(["Reference_Number", "Reference"]):
                    this_line[label] = format_value(row[num])
                lines.append(this_line)

        table = Table("reference", delimiter="\t")
        table.columns=[("Reference_Number"  ,   ("pk-int",) ),
                       ("Reference"         ,   ("char",)   )]
        table.pk = 'Reference_Number'
        table.contains_pk = True

        gwdd = []
        for line in lines:
            gwdd_ref = [line["Reference_Number"],
                        line["Reference"]]
            gwdd.append(gwdd_ref)

        data = ['\t'.join(gwdd_line) for gwdd_line in gwdd]
        self.engine.table = table
        self.engine.create_table()
        self.engine.add_to_table(data)
        self.engine.find_file("GlobalWoodDensityDatabase.xls")

        return self.engine

SCRIPT = main()

