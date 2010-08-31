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
from dbtk_wizard import *

TEST_DATA_LOCATION = "test_data"

try:
    os.makedirs(TEST_DATA_LOCATION)
except:
    pass

for engine in ALL_ENGINES:
    opts = get_opts()
    opts["engine"] = engine.abbreviation
    
    TEST_ENGINES[engine.abbreviation] = choose_engine(opts)
    TEST_ENGINES[engine.abbreviation].get_cursor()
                
unittest.main()