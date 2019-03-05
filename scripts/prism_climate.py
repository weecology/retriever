#retriever

"""Retriever script for direct download of PRISM climate data"""
from future import standard_library

standard_library.install_aliases()
from builtins import range
from retriever.lib.templates import Script
import requests
from pkg_resources import parse_version

from retriever.logger import getFileLogger
logger = getFileLogger(os.path.join(os.pardir, os.pardir, "logs"), "prism_climate.log")

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "PRISM Climate Data"
        self.name = "prism-climate"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.2.3'
        self.ref = "http://prism.oregonstate.edu/"
        self.urls = {
            "climate": "http://services.nacse.org/prism/data/public/4km/"}
        self.description = "The PRISM data set represents climate " \
                           "observations from a wide range of monitoring " \
                           "networks, applies sophisticated quality control " \
                           "measures, and develops spatial climate datasets " \
                           "to reveal short- and long-term climate patterns. "
        self.keywords = []

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def get_file_names(self, clim_var, mval, year, month):
        """Create a list of all filenames in a given monthly data zip file """

        file_extensions = [
            'bil',
            'bil.aux.xml',
            'hdr',
            'info.txt',
            'prj',
            'stx',
            'xml']
        file_names = []

        for extension in file_extensions:
            file_names.append(
                "PRISM_{}_stable_4km{}_{}{}_bil.{}".format(
                    clim_var, mval, year, month, extension))
        return file_names

    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            msg =   "The PRISM dataset contains only non-tabular "\
                    "data files, and can only be used with the "\
                    "'download only' engine."
            logger.error(msg)
            raise Exception(msg)
        Script.download(self, engine, debug)

        clim_vars = ['ppt', 'tmax', 'tmean', 'tmin']
        years = list(range(1981, 2015))
        months = ["{:02d}".format(i) for i in range(1, 13)]
        for clim_var in clim_vars:
            mval = "M3" if clim_var == 'ppt' else "M2"
            for year in years:
                for month in months:
                    file_names = self.get_file_names(
                        clim_var, mval, year, month)
                    file_url = requests.compat.urljoin(
                        self.urls["climate"], "{}/{}{}".format(clim_var, year, month))
                    archive_name = "PRISM_{}_stable_4km{}_{}{}_bil.zip".format(
                        clim_var, mval, year, month)
                    self.engine.download_files_from_archive(
                        file_url, file_names, "zip", True, archive_name)
                    self.engine.register_files(file_names)


SCRIPT = main()
