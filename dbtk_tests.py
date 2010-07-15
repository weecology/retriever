"""Database Toolkit Tests
Automated tests to check the known MD5 checksums of imported data against data
imported by DBTK scripts.

"""

import os
import hashlib
import unittest
from dbtks_ernest2003 import *
from dbtks_pantheria import *
from dbtks_portal_mammals import *
import dbtk_ui

TEST_DATA_LOCATION = "test_data"

try:
    os.makedirs(TEST_DATA_LOCATION)
except:
    pass        
opts = {"engine":"m"}

def strvalue(value):
    if value:
        if isinstance(value, str):
            return '"' + value + '"'
        else:
            return str(value)
    else:
        return ""

class Tests(unittest.TestCase):
    def test_MammalLifeHistory(self):
        # Download Mammal Lifehistory database to MySQL
        script = MammalLifeHistory()
        md5 = "afa09eed4ca4ce5db31d15c4daa49ed3"
        opts = get_opts()
        opts["engine"] = "m"        
        engine = choose_engine(opts)
        engine.script = script
        script.download(engine)
        
        # Export MySQL data
        cursor = engine.connection.cursor()
        cursor.execute("SELECT * FROM " + engine.tablename())
        
        filename = os.path.join(TEST_DATA_LOCATION, "mammaltest.csv")
        file = open(filename, 'wb')
        for i in range(cursor.rowcount):
            line = ','.join([strvalue(value) for value in cursor.fetchone()])
            print line
            file.write(line + "\n")            
        file.close
        
        file = open(filename, 'r')
        sum = hashlib.md5()
        while True:
            data = file.read(128)
            if not data:
                break
            sum.update(data)
        sum = sum.hexdigest()
        self.assertEqual(md5, sum)
        
unittest.main()