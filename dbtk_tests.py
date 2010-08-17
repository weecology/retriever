"""Database Toolkit Tests
Automated tests to check the known MD5 checksums of imported data against data
imported by DBTK scripts.

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