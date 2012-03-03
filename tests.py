"""Database Toolkit Tests

This module, when run, runs all unit tests from all Retriever scripts in
the /scripts folder (except for those listed in IGNORE), for each engine in
ENGINE_LIST() from __init__.py. In other words, it runs tests for each possible
combination of database platform and script. 

The tests generally run the script, import the resulting data, and checks to
see if there are any errors. It does not check the values in the database.

"""

import os
import unittest
from retriever.lib.tools import get_opts, choose_engine
from retriever import MODULE_LIST, ENGINE_LIST, SCRIPT_LIST

MODULE_LIST = MODULE_LIST()
ENGINE_LIST = ENGINE_LIST()
SCRIPT_LIST = SCRIPT_LIST()
TEST_ENGINES = {}
IGNORE = ["AvianBodyMass", "FIA"]

for engine in ENGINE_LIST:
    opts = get_opts(SCRIPT_LIST, args=[])
    opts["engine"] = engine.abbreviation

    try:
        TEST_ENGINES[engine.abbreviation] = choose_engine(opts)
        TEST_ENGINES[engine.abbreviation].get_cursor()
    except:
        TEST_ENGINES[engine.abbreviation] = None
        pass
    
    
errors = []
for module in MODULE_LIST:
    for (key, value) in TEST_ENGINES.items():
        if value and not module.SCRIPT.shortname in IGNORE:
            print "==>", module.__name__, value.name
            try:
                module.SCRIPT.download(value)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print "ERROR."
                errors.append((key, module.__name__, e))

print('')
if errors:
    print("Engine, Dataset, Error")
    for error in errors:
        print(error)
else:
    print("All tests passed")
