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
                    if colnum == 11:
                        # For column 11, remove trailing zero
                        return str(int(value))
                    else:
                        # Otherwise, if the value is numerical, give it two
                        # trailing zeroes 
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
        md5 = "afa09eed4ca4ce5db31d15c4daa49ed3"        
        engine = choose_engine(opts)
        engine.script = script
        script.download(engine)
        
        # Export MySQL data
        cursor = engine.connection.cursor()
        cursor.execute("SELECT * FROM " + engine.tablename())
        
        filename = os.path.join(TEST_DATA_LOCATION, "mammaltest.csv")
        file = open(filename, 'wb')
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            line = ','.join([strvalue(row[i], i) for i in range(len(row))])
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