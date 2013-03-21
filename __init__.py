"""EcoData Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""

import os
from os.path import join, isfile, getmtime, exists
import imp
from lib.compile import compile_script


VERSION = 'v1.5'
MASTER = True

REPO_URL = "https://raw.github.com/weecology/retriever/"
MASTER_BRANCH = REPO_URL + "master/"
REPOSITORY = MASTER_BRANCH if MASTER else REPO_URL + VERSION + "/"

# create the necessary directory structure for storing scripts/raw_data
# in the ~/.retriever directory
HOME_DIR = os.path.expanduser('~/.retriever/')
for dir in (HOME_DIR, os.path.join(HOME_DIR, 'raw_data'), os.path.join(HOME_DIR, 'scripts')):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError:
            print "The Retriever lacks permission to access the ~/.retriever/ directory."
            raise
SCRIPT_SEARCH_PATHS =   [
                         "./",
                         "scripts",
                         os.path.join(HOME_DIR, 'scripts/'),
                         ]
SCRIPT_WRITE_PATH =     SCRIPT_SEARCH_PATHS[-1]
DATA_SEARCH_PATHS =     [
                         "./",
                         "{dataset}",
                         "raw_data/{dataset}",
                         os.path.join(HOME_DIR, 'raw_data/{dataset}'),
                         ]
DATA_WRITE_PATH =       DATA_SEARCH_PATHS[-1]


def MODULE_LIST(force_compile=False):
    """Load scripts from scripts directory and return list of modules."""
    modules = []
    
    for search_path in [search_path for search_path in SCRIPT_SEARCH_PATHS if exists(search_path)]:
        to_compile = [file for file in os.listdir(search_path)
                      if file[-7:] == ".script" and file[0] != "_"
                      and ((not isfile(join(search_path, file[:-7] + '.py'))) or 
                           (isfile(join(search_path, file[:-7] + '.py')) and
                            (getmtime(join(search_path, file[:-7] + '.py')) < 
                             getmtime(join(search_path, file))))
                            or force_compile)
                          ]
        for script in to_compile:
            script_name = '.'.join(script.split('.')[:-1])
            compile_script(join(search_path, script_name))
    
        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_"
                 and '#retriever' in open(join(search_path, file), 'r').readline().lower()]
    
        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            file, pathname, desc = imp.find_module(script_name, [search_path])
            try:
                new_module = imp.load_module(script_name, file, pathname, desc)
                new_module.SCRIPT.download
                modules.append(new_module)
            except:
                print "Failed to load script: %s (%s)" % (script_name, search_path)
                raise
    
    return modules


def SCRIPT_LIST(force_compile=False):
    return [module.SCRIPT for module in MODULE_LIST(force_compile)]


def ENGINE_LIST():
    from retriever.engines import engine_list
    return engine_list


sample_script = """# basic information about the script
name: Mammal Life History Database - Ernest, et al., 2003
shortname: MammalLH
description: S. K. Morgan Ernest. 2003. Life history characteristics of placental non-volant mammals. Ecology 84:3402.
tags: Taxon > Mammals, Data Type > Compilation

# tables
table: species, http://esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"""