"""Database Toolkit Tests
Automated tests to check the known MD5 checksums of imported data against data
imported by DBTK scripts.

"""

import os
from hashlib import md5
import unittest
from dbtks_ernest2003 import *
from dbtks_pantheria import *
from dbtks_portal_mammals import *
import dbtk_ui
import time

TEST_DATA_LOCATION = "test_data"

try:
    os.makedirs(TEST_DATA_LOCATION)
except:
    pass

def getmd5(lines):
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

opts = get_opts()
opts["engine"] = "m"

class Tests(unittest.TestCase):
    def test_MammalLifeHistory(self):
        def strvalue(value, colnum):
            if value:
                if isinstance(value, str):
                    # Add double quotes to strings
                    return '"' + value + '"'
                else:
                    if len(str(value).split('.')) == 2:
                        while len(str(value).split('.')[-1]) < 2:
                            value = str(value) + "0"
                        return str(value)
                    else:
                        return str(value)
            else:
                return ""        
        # Download Mammal Lifehistory database to MySQL
        script = MammalLifeHistory()
        check = "afa09eed4ca4ce5db31d15c4daa49ed3"        
        engine = choose_engine(opts)
        engine.script = script
        script.download(engine)
        
        # Export MySQL data
        cursor = engine.connection.cursor()
        cursor.execute("SELECT * FROM " + engine.tablename() + " m ORDER BY " +
                       "m.sporder, m.family, m.genus, m.species")
        
        lines = []
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            lines.append(','.join([strvalue(row[i], i) for i in range(1, len(row))]) + "\n")
        lines = ''.join(lines)
        sum = getmd5(lines)
        checkfile = open(os.path.join(TEST_DATA_LOCATION, "lifehistories_manual.txt"), 'rb')
        check = getmd5(checkfile)
        checkfile.close()
        self.assertEqual(sum, check)
        
unittest.main()