"""Database Toolkit Tests

This module, when run, runs all unit tests from all DBTK scripts referenced in
dbtk_wizard.py, for each engine in ALL_ENGINES from dbtk_engines.py. In other
words, it runs tests for each possible combination of database platform and
script.

The tests generally run the script, import the resulting data, and check the
MD5 checksum against a known static value.

"""

import os
import unittest
from retriever.lib.tools import get_opts, choose_engine
from retriever import MODULE_LIST, ENGINE_LIST

MODULE_LIST = MODULE_LIST()
ENGINE_LIST = ENGINE_LIST()
TEST_ENGINES = {}
IGNORE = ["AvianBodyMass", "FIA"]

for engine in ENGINE_LIST:
    opts = get_opts()
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
            except Exception as e:
                print "ERROR."
                errors.append((key, module.__name__, e))

for error in errors:
    print error
