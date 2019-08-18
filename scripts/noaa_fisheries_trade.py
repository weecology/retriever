# -*- coding: UTF-8 -*-
#retriever

from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Commercial Fisheries Monthly Trade Data by Product, Country/Association"
        self.name = "noaa-fisheries-trade"
        self.retriever_minimum_version = '2.1.dev'
        self.urls = {
            "imports": "https://www.st.nmfs.noaa.gov/pls/webpls/trade_prdct_cntry_ind_mth.results?"
                       "qtype=IMP&qmonthfrom=01&qmonthto=12&qyearfrom=1975&qyearto=2018"
                       "&qprod_name=%25&qcountry=%25&qsort=COUNTRY&qoutput=ASCII+FILE",

            "exports": "https://www.st.nmfs.noaa.gov/pls/webpls/trade_prdct_cntry_ind_mth.results?"
                       "qtype=EXP&qmonthfrom=01&qmonthto=12&qyearfrom=1975&qyearto=2018"
                       "&qprod_name=%25&qcountry=%25&qsort=COUNTRY&qoutput=ASCII+FILE",

            "rexport": "https://www.st.nmfs.noaa.gov/pls/webpls/trade_prdct_cntry_ind_mth.results?"
                       "qtype=REX&qmonthfrom=01&qmonthto=12&qyearfrom=1975&qyearto=2018"
                       "&qprod_name=%25&qcountry=%25&qsort=COUNTRY&qoutput=ASCII+FILE"
        }
        self.version = '1.0.0'
        self.ref = "https://www.st.nmfs.noaa.gov/commercial-fisheries/foreign-trade/" \
                   "applications/monthly-product-by-countryassociation"
        self.citation = "No known Citation"
        self.description = "Commercial Fisheries statistics provides a summary of " \
                           "commercial fisheries product data by individual country."
        self.keywords = ["Fish", "Fisheries"]

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        for key in self.urls:
            original_file_name = "trade_prdct_{}.txt".format(key)
            new_file_name = "trade_prdct_{}.csv".format(key)

            engine.download_file(self.urls[key], original_file_name)

            old_path = self.engine.format_filename(original_file_name)
            new_path = self.engine.format_filename(new_file_name)

            # Re-write the file with one delimeter
            old_data = open_fr(old_path)
            new_data = open_fw(new_path)

            # Read header line and convert "," to "|"
            line1 = old_data.readline().strip().replace(",", "|")
            new_data.write(line1 + "\n")
            for line in old_data:
                # Remove leading "|" from the data
                new_data.write(line.strip("|"))
            new_data.close()
            old_data.close()
            table = Table(key, delimiter="|")
            engine.auto_create_table(table, filename=new_file_name)
            engine.insert_data_from_file(new_path)


SCRIPT = main()
