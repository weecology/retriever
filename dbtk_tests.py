"""Database Toolkit Tests
Automated tests to check the known MD5 checksums of imported data against data
imported by DBTK scripts.

"""

import os
from hashlib import md5
import unittest
from math import fabs
from decimal import Decimal
import dbtk_ui

from dbtks_EA_ernest2003 import *
from dbtks_EA_pantheria import *
from dbtks_bbs import *
from dbtks_portal_mammals import *
from dbtks_gentry import *
from dbtks_CRC_avianbodymass import *
from dbtks_EA_avianbodysize2007 import *

TEST_DATA_LOCATION = "test_data"

try:
    os.makedirs(TEST_DATA_LOCATION)
except:
    pass

def getmd5(lines):
    # Get MD5 value of a set of lines
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()
def checkagainstfile(lines, filename):
    # Checks a set of lines against a file, and prints all lines that don't
    # match
    testfile = open(os.path.join(TEST_DATA_LOCATION, filename), 'rb')
    i = 0        
    for line in lines:
        i += 1
        line2 = testfile.readline()
        if line != line2:
            print i 
            print "LINE1:" + line
            print "LINE2:" + line2
            print len(line), len(line2)
            print "\n" in line, "\n" in line2
    testfile.close()    

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
        script = EAMammalLifeHistory2003()
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
            lines.append(','.join([strvalue(row[i], i) for i in range(1, len(row))]) + "\r\n")            
        lines = ''.join(lines)
        sum = getmd5(lines)
        self.assertEqual(sum, check)
        
        
    def test_Pantheria(self):
        def strvalue(value, colnum):
            if value != None:
                if isinstance(value, str):
                    # Add double quotes to strings
                    return '"' + value + '"'
                elif isinstance(value, Decimal):
                    if value == 0:
                        return "0.00"
                    try:
                        if Decimal("-0.01") < value < Decimal("0.01"):                            
                            dec = len(str(value).split('.')[-1].strip('0')) - 1
                            value = ("%." + str(dec) + "e") % value
                            value = str(value)
                            strippedvalue = value.split("e")
                            return (strippedvalue[0].rstrip("0") + 
                                    "e" + strippedvalue[1])
                    except:
                        pass
                    value = str(value).rstrip('0')
                    if len(value.split('.')) == 2:
                        while len(value.split('.')[-1]) < 2:
                            value = value + "0"                        
                    return value
                else:
                    if len(str(value).split('.')) == 2:
                        while len(str(value).split('.')[-1]) < 2:
                            value = str(value) + "0"                        
                        return str(value)
                    else:
                        return str(value)
            else:
                return ""
        # Download database to MySQL
        script = EAPantheria()
        check = "4d2d9c2f57f6ae0987aafd140aace1e3"        
        engine = choose_engine(opts)
        engine.script = script
        script.download(engine)
        
        # Export MySQL data
        cursor = engine.connection.cursor()
        cursor.execute("SELECT * FROM " + engine.tablename() + " m ORDER BY " +
                       "m.sporder, m.family, m.genus, m.species")
        
        lines = []
        for n in range(cursor.rowcount):
            row = cursor.fetchone()
            lines.append(','.join([strvalue(row[i], i) for i in range(1, len(row))]) + "\r\n")             
        lines = ''.join(lines)
        
        sum = getmd5(lines)
        self.assertEqual(sum, check)        
        
unittest.main()