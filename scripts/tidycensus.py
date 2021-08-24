# -*- coding: utf-8 -*-
#retriever

import os
import re
import subprocess
import pandas as pd

try:
    import rpy2.robjects as ro
    import rpy2.robjects.packages as rpackages
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter
except ImportError:
    pass

from retriever.lib.models import Table, VectorDataset
from retriever.lib.templates import Script
from retriever.lib.defaults import DATA_WRITE_PATH

R_string = "Rscript -e \"install.packages('{package_name}')\""
exit_status = "had non-zero exit status"
unable_to_access = "unable to access index for repository"
packages = ['rgdal', 'units', 'sf', 'tigris', 'tidycensus']
file_paths = {}


def census_api_key():
    """Checks if the CENSUS_API_KEY is added to the .Renviron file"""
    r_string = '''
        home <- Sys.getenv("HOME")
        renv <- file.path(home, ".Renviron")
        readRenviron(renv)
        key <- Sys.getenv("CENSUS_API_KEY")
        '''

    ro.r(r_string)
    ro.r['options'](warn=-1)  # suppresses warnings from R console
    api_key = ro.r('key')[0]
    if not api_key:
        print('Add the CENSUS_API_KEY in your .Renviron file')
        return False
    else:
        return True


def install_tidycensus():
    """Installs the R packages required for installing the tidycensus package"""
    for package in packages:
        if not rpackages.isinstalled(package):
            output = subprocess.getoutput(R_string.format(package_name=package))
            if bool(re.search(exit_status, output)):
                print(output)
                print(
                    "*Please install the system dependencies for {} package*".format(
                        package))
                print("Installating R packages failed!!!")
                return False
            elif bool(re.search(unable_to_access, output)):
                print(output)
                return False
        print("Package {} is installed".format(package))
    print("Installing R packages completed!!!")
    return True


class main(Script):

    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Load US Census Boundary and Attribute Data as 'tidyverse' and " \
            "'sf'-Ready Data Frames"
        self.name = "tidycensus"
        self.retriever_minimum_version = '3.0.1-dev'
        self.version = '1.0.1'
        self.ref = "https://github.com/walkerke/tidycensus"
        self.citation = ""
        self.licenses = [{"name": "MIT"}]
        self.description = "An integrated R interface to the decennial US Census and American Community Survey APIs and" \
                           "the US Census Bureau's geographic boundary files. Allows R users to return Census and ACS data as" \
                           "tidyverse-ready data frames, and optionally returns a listcolumn with feature geometry for all Census" \
                           "geographies."
        self.keywords = ["census", "US", "tidycensus", "R", "geographic boundaries"]
        self.encoding = 'utf-8'

    def download_raw_data(self, datasets, engine):
        """Downloads the raw data files of all the datasets present in tidycensus"""
        # Load all the required libraries
        r_string = '''
        library(tidycensus)
        library(sf)
        library(readr)
        '''
        ro.r(r_string)
        for dataset_name in datasets:
            # saves mig_recodes raw data file
            if dataset_name == 'mig_recodes':
                path = os.path.normpath(engine.format_filename('mig_recodes.csv'))
                r_string = '''
                rdf = as.data.frame.data.frame({dataset})
                write_csv(rdf, "{path}", append=FALSE)
                '''.format(dataset=dataset_name, path=path)

                ro.r(r_string)

                df = pd.read_csv(path,
                                 encoding='cp1252',
                                 converters={'code': lambda x: str(x)})
                df.to_csv(path, encoding='utf-8', index=False)
                file_paths['mig_recodes'] = path

            # saves raw data files of county_laea and state_laea
            elif dataset_name in ['county_laea', 'state_laea']:
                path = os.path.normpath(
                    os.path.join(engine.format_data_dir(), str(dataset_name)))
                r_string = '''
                dir.create("{path}/")
                setwd("{path}/")
                st_write({dataset}, "{dataset}.shp", delete_layer=TRUE)
                setwd("../..")
                '''.format(path=path, dataset=dataset_name)

                ro.r(r_string)
                file_paths[dataset_name] = os.path.normpath(
                    os.path.join(path, '{}.shp'.format(dataset_name)))

            # saves raw data files of pums_variables and fips_codes
            else:
                r_string = '''
                rdf = as.data.frame.data.frame({})
                '''.format(dataset_name)

                ro.r(r_string)
                rdf = ro.r('rdf')

                with localconverter(ro.default_converter + pandas2ri.converter):
                    pdf = ro.conversion.rpy2py(rdf)
                path = os.path.normpath(
                    engine.format_filename('{}.csv'.format(dataset_name)))
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                pdf.to_csv(path, index=False)
                file_paths[dataset_name] = path

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        datasets = [
            'fips_codes', 'mig_recodes', 'pums_variables', 'state_laea', 'county_laea'
        ]
        data_path = os.path.normpath(DATA_WRITE_PATH.format(dataset='tidycensus'))
        if not os.path.exists(data_path):
            engine.create_raw_data_dir()
        elif engine.name == 'CSV':
            engine.data_path = engine.opts['data_dir']
            engine.create_raw_data_dir(engine.data_path)
        else:
            engine.data_path = engine.opts["path"]
            engine.create_raw_data_dir(engine.data_path)

        api_key = census_api_key()
        packages_remaining = len([x for x in packages if not rpackages.isinstalled(x)])
        if packages_remaining:
            print("Installing R package tidycensus...")
            installed = install_tidycensus()
            if not installed:
                exit()
        if api_key:
            self.download_raw_data(datasets, engine)
        else:
            exit()
        # state_laea dataset
        table = VectorDataset(name='state_laea')
        engine.table = table
        engine.auto_create_table(table, filename='state_laea/state_laea.shp')
        engine.insert_vector(file_paths['state_laea'])

        # county_laea dataset
        table = VectorDataset(name='county_laea')
        engine.table = table
        engine.auto_create_table(table, filename='county_laea/county_laea.shp')
        engine.insert_vector(file_paths['county_laea'])

        # mig_recodes dataset
        table = Table(name='mig_recodes', delimiter=",")
        table.columns = [
            ("characteristic", ("char",)),
            ("code", ("char",)),
            ("description", ("char",)),
            ("ordered", ("bool",))
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(file_paths['mig_recodes'])

        # pums_variables dataset
        engine.auto_create_table(Table('pums_variables', delimiter=','),
                                 filename='pums_variables.csv')
        engine.insert_data_from_file(file_paths['pums_variables'])

        # fips_codes
        table = Table(name='fips_codes', delimiter=",")
        table.columns = [
            ("state", ("char",)),
            ("state_code", ("char",)),
            ("state_name", ("char",)),
            ("county_code", ("char",)),
            ("county", ("char",))
        ]
        engine.table = table
        engine.create_table()
        engine.insert_data_from_file(file_paths['fips_codes'])


SCRIPT = main()
