"""EcoData Retriever

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""

import os
import imp


VERSION = '0.5'

REPOSITORY = 'http://www.ecologicaldata.org/ecodataretriever/'


def MODULE_LIST():
    """Load scripts from scripts directory and return list of modules."""
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
            pass
    
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
