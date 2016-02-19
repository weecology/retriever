"""Attempt to install all datasets into all database management systems

This module, when run, attempts to install datasets from all Retriever scripts
in the /scripts folder (except for those listed in IGNORE), for each engine in
ENGINE_LIST() from __init__.py. In other words, it runs trys to install using
all possible combinations of database platform and script and checks to
see if there are any errors. It does not check the values in the database.

"""

import os
import sys
from retriever.lib.tools import choose_engine
from retriever import MODULE_LIST, ENGINE_LIST, SCRIPT_LIST

MODULE_LIST = MODULE_LIST()
ENGINE_LIST = ENGINE_LIST()
if len(sys.argv) > 1:
    ENGINE_LIST = [
                    e for e in ENGINE_LIST
                    if e.name in sys.argv[1:] or
                    e.abbreviation in sys.argv[1:]
    ]
SCRIPT_LIST = SCRIPT_LIST()
TEST_ENGINES = {}
IGNORE = ["AvianBodyMass", "FIA"]

for engine in ENGINE_LIST:
    opts = {}
    print "** %s **" % engine.name
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
        if value and module.SCRIPT.shortname not in IGNORE:
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
