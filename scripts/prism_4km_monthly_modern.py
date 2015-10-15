#retriever

"""Retriever script for direct download of PRISM climate data"""

from retriever.lib.templates import Script
import urlparse

class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.name = "PRISM Climate Data"
        self.shortname = "PRISM"
        self.ref = "http://prism.oregonstate.edu/"
        self.urls = {"climate": "http://services.nacse.org/prism/data/public/4km/"}

    def get_file_names(self, clim_var, mval, year, month):
        """Create a list of all filenames in a given monthly data zip file """

        file_extensions = ['bil', 'bil.aux.xml', 'hdr', 'info.txt', 'prj', 'stx', 'xml']
        file_names = []

        for extension in file_extensions:
            file_names.append("PRISM_{}_stable_4km{}_{}{}_bil.{}".format(clim_var,
                                                                         mval,
                                                                         year,
                                                                         month,
                                                                         extension))
        return file_names

    def download(self, engine=None, debug=False):
        if engine.name != "Download Only":
            raise Exception("The PRISM dataset contains only non-tabular data files, and can only be used with the 'download only' engine.")
        Script.download(self, engine, debug)

        clim_vars = ['ppt', 'tmax', 'tmean', 'tmin']
        years = range(1981, 2015)
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for clim_var in clim_vars:
            mval = "M3" if clim_var == 'ppt' else "M2"
            for year in years:
                for month in months:
                    file_names = self.get_file_names(clim_var, mval, year, month)
                    file_url = urlparse.urljoin(self.urls["climate"], "{}/{}{}".format(clim_var, year, month))
                    archivename = "PRISM_{}_stable_4km{}_{}{}_bil.zip".format(clim_var, mval, year, month)
                    self.engine.download_files_from_archive(file_url, file_names, archivename=archivename, keep_in_dir=True)
                    self.engine.register_files(file_names)

SCRIPT = main()
