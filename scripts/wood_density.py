#retriever
"""Retriever script for Zanne et al. Global wood density database.

"""
from builtins import range

import sys
import os
import xlrd
from imp import reload

from retriever.lib.templates import Script
from retriever.lib.models import Table
from retriever.lib.excel import Excel
from retriever import HOME_DIR, open_fr, open_fw, open_csvw, to_str

class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "Global wood density database - Zanne et al. 2009"
        self.shortname = "wood-density"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.2.1'
        self.urls = {"GWDD": "http://datadryad.org/bitstream/handle/10255/dryad.235/GlobalWoodDensityDatabase.xls?sequence=1"}
        self.tags = ["Taxon > Plants", "Spatial Scale > Global",
                     "Data Type > Observational"]
        self.ref = "http://datadryad.org/resource/doi:10.5061/dryad.234"
        self.description = "A collection  and collation of data on the major wood functional traits, including the largest wood density database to date (8412 taxa), mechanical strength measures and anatomical features, as well as clade-specific features such as secondary chemistry."
        self.citation = "Chave J, Coomes DA, Jansen S, Lewis SL, Swenson NG, Zanne AE (2009) Towards a worldwide wood economics spectrum. Ecology Letters 12(4): 351-366. http://dx.doi.org/10.1111/j.1461-0248.2009.01285.x and Zanne AE, Lopez-Gonzalez G, Coomes DA, Ilic J, Jansen S, Lewis SL, Miller RB, Swenson NG, Wiemann MC, Chave J (2009) Data from: Towards a worldwide wood economics spectrum. Dryad Digital Repository. http://dx.doi.org/10.5061/dryad.234"
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
        reload(sys)
        if hasattr(sys, 'setdefaultencoding'):
            sys.setdefaultencoding("utf-8")

        self.engine.download_file(self.urls["GWDD"], "GlobalWoodDensityDatabase.xls")
        filename = os.path.basename("GlobalWoodDensityDatabase.xls")
        book = xlrd.open_workbook(self.engine.format_filename(filename))
        sh = book.sheet_by_index(1)
        rows = sh.nrows

        # Creating data files
        file_path = self.engine.format_filename("gwdd_data.csv")
        gwdd_data = open_fw(file_path)
        csv_writer = open_csvw(gwdd_data)
        csv_writer.writerow(["Number", "Family", "Binomial", "Wood_Density", "Region", "Reference_Number"])

        for index in range(1, rows):
            row = sh.row(index)
            # get each row and format the sell value.
            row_as_list = [to_str(column_value.value) for column_value in row]
            csv_writer.writerow(row_as_list)
        gwdd_data.close()

        table = Table("data", delimiter=",")
        table.columns = [("Number", ("pk-int",)),
                         ("Family", ("char",)),
                         ("Binomial", ("char",)),
                         ("Wood_Density", ("double",)),
                         ("Region", ("char",)),
                         ("Reference_Number", ("int",))]
        table.pk = 'Number'
        table.contains_pk = True

        self.engine.table = table
        self.engine.create_table()
        self.engine.insert_data_from_file(engine.format_filename(file_path))

        # Creating reference tale file
        file_path = self.engine.format_filename("gwdd_ref.csv")
        ref_file = open_fw(file_path)
        csv_writerd = open_csvw(ref_file)
        csv_writerd.writerow(["Reference_Number", "Reference"])
        sh = book.sheet_by_index(2)
        rows = sh.nrows
        for index in range(1, rows):
            row = sh.row(index)
            # get each row and format the sell value.
            row_as_list = [to_str(column_value.value, object_encoding=sys.stdout) for column_value in row]
            csv_writerd.writerow(row_as_list)
        ref_file.close()

        table = Table("reference", delimiter=",")
        table.columns = [("Reference_Number", ("pk-int",)), ("Reference", ("char",))]
        table.pk = 'Reference_Number'
        table.contains_pk = True
        self.engine.table = table
        self.engine.create_table()
        self.engine.insert_data_from_file(engine.format_filename(file_path))

        return self.engine

SCRIPT = main()
