"""Database Toolkit

This package contains a framework for creating and running scripts designed to
download published ecological data, and store the data in a database.

"""

import os
import imp
import re


VERSION = '0.3'

REPOSITORY = 'http://www.ecologicaldata.org/dbtk/'

CATEGORIES = [
              "birds",
              "mammals",
              ]

scripts = [
           "bbs",
           "CRC_avianbodymass",
           "EA_avianbodysize2007",
           "EA_ernest2003",
           "EA_pantheria",
           "EA_portal_mammals",
           "gentry",
           ]
           
engines = [
           "mysql",
           "postgres",
           "sqlite",
           "msaccess",
           ]


def DBTK_LIST():    
    """Load scripts from scripts directory and return list of DbTk classes."""
    path = os.path.join(os.getcwd(), "scripts")
    files = [file for file in os.listdir(path)
             if file[-3:] == ".py" and file[0] != "_"]
             
    modules = []
    for script in scripts:
        file, pathname, description = imp.find_module(script, [path])
        modules.append(imp.load_module(script, file, pathname, description))
    
    return [module.main() for module in modules]


def ENGINE_LIST():
    ENGINE_MODULE_LIST = [
                          __import__("dbtk.engines." + module, fromlist="engines")
                          for module in engines
                          ]
    
    return [module.engine() for module in ENGINE_MODULE_LIST]
