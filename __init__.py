"""EcoData Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""

import os
import imp
from lib.compile import compile_script


VERSION = 'master'

REPO_URL = "https://raw.github.com/croryx/retriever/"
MASTER_BRANCH = REPO_URL + "master/"
REPOSITORY = REPO_URL + "v" + VERSION + "/"


def MODULE_LIST():
    """Load scripts from scripts directory and return list of modules."""
    to_compile = [file for file in os.listdir("scripts")
                  if file[-7:] == ".script" and file[0] != "_"
                  and ((not os.path.isfile("scripts/" + file[:-7] + '.py')) or 
                       (os.path.isfile("scripts/" + file[:-7] + '.py') and
                        os.path.getmtime("scripts/" + file[:-7] + '.py') < 
                        os.path.getmtime("scripts/" + file))
                       )]
    for script in to_compile:
        script_name = '.'.join(script.split('.')[:-1])
        compile_script("scripts/" + script_name)
    
    files = [file for file in os.listdir("scripts")
             if file[-3:] == ".py" and file[0] != "_"]
    
    modules = []
    for script in files:
        script_name = '.'.join(script.split('.')[:-1])
        file, pathname, desc = imp.find_module(script_name, ["scripts"])
        try:
            new_module = imp.load_module(script_name, file, pathname, desc)
            new_module.SCRIPT
            modules.append(new_module)
        except:
            print "Failed to load script: " + script_name
    
    return modules


def SCRIPT_LIST():
    return [module.SCRIPT for module in MODULE_LIST()]


def ENGINE_LIST():
    engines = [
               "mysql",
               "postgres",
               "sqlite",
               "msaccess",
               ]

    ENGINE_MODULE_LIST = [
                          __import__("retriever.engines." + module, fromlist="engines")
                          for module in engines
                          ]
    
    return [module.engine() for module in ENGINE_MODULE_LIST]
