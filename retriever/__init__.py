"""Data Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""
from __future__ import print_function
from __future__ import absolute_import
from builtins import str

import io
import os
import sys
import csv
from os.path import join, isfile, getmtime, exists
from pkg_resources import parse_version
import imp
import platform

from retriever.lib.compile import compile_json
from retriever._version import __version__

current_platform = platform.system().lower()
if current_platform != 'windows':
    import pwd

VERSION = __version__
COPYRIGHT = "Copyright (C) 2011-2016 Weecology University of Florida"
REPO_URL = "https://raw.github.com/weecology/retriever/"
MASTER_BRANCH = REPO_URL + "master/"
REPOSITORY = MASTER_BRANCH

# create the necessary directory structure for storing scripts/raw_data
# in the ~/.retriever directory
HOME_DIR = os.path.expanduser('~/.retriever/')
for dir in (HOME_DIR, os.path.join(HOME_DIR, 'raw_data'), os.path.join(HOME_DIR, 'scripts')):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
            if (current_platform != 'windows') and os.getenv("SUDO_USER"):
                # owner of .retriever should be user even when installing
                # w/sudo
                pw = pwd.getpwnam(os.getenv("SUDO_USER"))
                os.chown(dir, pw.pw_uid, pw.pw_gid)
        except OSError:
            print("The Retriever lacks permission to access the ~/.retriever/ directory.")
            raise
SCRIPT_SEARCH_PATHS = [
    "./",
    'scripts',
    os.path.join(HOME_DIR, 'scripts/')
]
SCRIPT_WRITE_PATH = SCRIPT_SEARCH_PATHS[-1]
DATA_SEARCH_PATHS = [
    "./",
    "{dataset}",
    "raw_data/{dataset}",
    os.path.join(HOME_DIR, 'raw_data/{dataset}'),
]
DATA_WRITE_PATH = DATA_SEARCH_PATHS[-1]

# Create default data directory
DATA_DIR = '.'


def open_fr(file_name, encoding='ISO-8859-1', encode=True):
    """Open file for reading respecting Python version and OS differences

    Sets newline to Linux line endings on Windows and Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if os.name == 'nt':
            file_obj = io.open(file_name, 'r', newline='', encoding=encoding)
        else:
            if encode:
                file_obj = io.open(file_name, "r", encoding=encoding)
            else:
                file_obj = io.open(file_name, "r")
    else:
        file_obj = io.open(file_name, "r", encoding=encoding)
    return file_obj


def open_fw(file_name, encoding='ISO-8859-1', encode=True):
    """Open file for writing respecting Python version and OS differences

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if encode:
            file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
        else:
            file_obj = io.open(file_name, 'w', newline='')
    else:
        file_obj = io.open(file_name, 'wb',)
    return file_obj


def open_csvw(csv_file, encode=True):
    """Open a csv writer forcing the use of Linux line endings on Windows

    Also sets dialect to 'excel' and escape characters to '\\'

    """
    if os.name == 'nt':
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\', lineterminator='\n')
    else:
        csv_writer = csv.writer(csv_file, dialect='excel', escapechar='\\')
    return csv_writer


def to_str(object, object_encoding=sys.stdout):
    if sys.version_info >= (3, 0, 0):
        enc = object_encoding.encoding
        return str(object).encode(enc, errors='backslashreplace').decode("latin-1")
    else:
        return object


def MODULE_LIST(force_compile=False):
    """Load scripts from scripts directory and return list of modules."""
    modules = []
    loaded_scripts = []

    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        to_compile = [
            file for file in os.listdir(search_path) if file[-5:] == ".json" and
            file[0] != "_" and (
                (not isfile(join(search_path, file[:-5] + '.py'))) or (
                    isfile(join(search_path, file[:-5] + '.py')) and (
                        getmtime(join(search_path, file[:-5] + '.py')) < getmtime(
                            join(search_path, file)))) or force_compile)]
        for script in to_compile:
            script_name = '.'.join(script.split('.')[:-1])
            compile_json(join(search_path, script_name))

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 '#retriever' in ' '.join(open(join(search_path, file), 'r').readlines()[:2]).lower()]

        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            if script_name not in loaded_scripts:
                loaded_scripts.append(script_name)
                file, pathname, desc = imp.find_module(script_name, [search_path])
                try:
                    new_module = imp.load_module(script_name, file, pathname, desc)
                    if hasattr(new_module.SCRIPT, "retriever_minimum_version"):
                        # a script with retriever_minimum_version should be loaded
                        # only if its compliant with the version of the retriever
                        if not parse_version(VERSION) >=  parse_version("{}".format(
                                new_module.SCRIPT.retriever_minimum_version)):
                            print("{} is supported by Retriever version {}".format(script_name,
                                                                                   new_module.SCRIPT.retriever_minimum_version))
                            print("Current version is {}".format(VERSION))
                            continue
                    # if the script wasn't found in an early search path
                    # make sure it works and then add it
                    new_module.SCRIPT.download
                    modules.append(new_module)
                except Exception as e:
                    sys.stderr.write("Failed to load script: %s (%s)\nException: %s \n" % (
                        script_name, search_path, str(e)))
    return modules


def SCRIPT_LIST(force_compile=False):
    return [module.SCRIPT for module in MODULE_LIST(force_compile)]


def ENGINE_LIST():
    from retriever.engines import engine_list
    return engine_list


def set_proxy():
    """Check for proxies and makes them available to urllib"""
    proxies = ["https_proxy", "http_proxy", "ftp_proxy",
               "HTTP_PROXY", "HTTPS_PROXY", "FTP_PROXY"]
    for proxy in proxies:
        if os.getenv(proxy):
            if len(os.environ[proxy]) != 0:
                for i in proxies:
                    os.environ[i] = os.environ[proxy]
                break

set_proxy()

sample_script = """
{
    "description": "S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.",
    "homepage": "http://esapubs.org/archive/ecol/E084/093/default.htm",
    "name": "MammalLH",
    "resources": [
        {
            "dialect": {},
            "mediatype": "text/csv",
            "name": "species",
            "schema": {},
            "url": "http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
        }
    ],
    "title": "Mammal Life History Database - Ernest, et al., 2003",
    "urls": {
        "species": "http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
    }
}
"""
CITATION = """Morris, B.D. and E.P. White. 2013. The EcoData Retriever: improving access to
existing ecological data. PLOS ONE 8:e65848.
http://doi.org/doi:10.1371/journal.pone.0065848

@article{morris2013ecodata,
  title={The EcoData Retriever: Improving Access to Existing Ecological Data},
  author={Morris, Benjamin D and White, Ethan P},
  journal={PLOS One},
  volume={8},
  number={6},
  pages={e65848},
  year={2013},
  publisher={Public Library of Science}
  doi={10.1371/journal.pone.0065848}
}
"""
