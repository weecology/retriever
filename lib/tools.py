"""Database Toolkit Tools

This module contains miscellaneous classes and functions used in DBTK scripts.

"""

import os
import sys
import warnings
import unittest
import getopt
from decimal import Decimal
from hashlib import md5
from dbtk.lib.models import Database, Engine, Cleanup, correct_invalid_value

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()

    
            
class DbTkTest(unittest.TestCase):    
    def strvalue(self, value, col_num):
        """Returns a string representing the cleaned value from a SELECT 
        statement, for use in tests.
        
        Arguments: value -- the value to be converted,
                   col_num -- the column number of the value (starting from 0)
                   
                   col_num is not used in this function, but may be
                   useful when overriding this function
                       
        """
        if value != None:
            if isinstance(value, str) or isinstance(value, unicode):
                # If the value is a string or unicode, it's not a number and
                # should be surrounded by quotes.
                return '"' + str(value) + '"'
            elif value == 0:
                return "0.00"
            elif isinstance(value, Decimal) or (Decimal("-0.01") < 
                                                Decimal(str(value)) < 
                                                Decimal("0.01")):
                try:
                    if Decimal("-0.01") < Decimal(str(value)) < Decimal("0.01"):                            
                        dec = len(str(value).split('.')[-1].strip('0')) - 1
                        value = ("%." + str(dec) + "e") % value
                        value = str(value)
                        strippedvalue = value.split("e")
                        return (strippedvalue[0].rstrip("0") + 
                                "e" + strippedvalue[1])
                except:
                    pass
                
                value = str(value).rstrip('0')
                if not '.' in value:
                    value += ".0"
                if len(value.split('.')) == 2:
                    while len(value.split('.')[-1]) < 2:
                        value = value + "0"                        
                return value
            else:
                value = str(value)
                if '.' in value:
                    value = value.rstrip('0')
                else:
                    value += ".0"
                if len(str(value).split('.')) == 2:
                    while len(str(value).split('.')[-1]) < 2:
                        value = str(value) + "0"                        
                    return str(value)
                else:
                    return str(value)
        else:
            return ""                
    
    def default_test(self, script, tables, include_pk = False):
        """The default unit test. Tests in DbTkTest classes can simply call 
        this function with the appropriate paramaters. The "script" property 
        should be an instance of DbTk, and tables is a list consisting of 
        tuples in the following format:
        
        (table name, MD5 sum, [order by statement])
        
        """
        for engine_letter in [engine.abbreviation for engine in ENGINES_TO_TEST]:
            engine = TEST_ENGINES[engine_letter]
            engine.script = script
            
            print "Testing with " + engine.name
            script.download(engine)
            
            print "Testing data . . ."
            
            for table in tables:
                tablename = table[0]
                checksum = table[1]
                if len(table) > 2:
                    orderby = table[2]
                    
                cursor = engine.connection.cursor()
                engine.table.tablename = tablename
                select_statement = "SELECT * FROM " + engine.tablename()
                if orderby:
                    select_statement += " ORDER BY " + orderby
                select_statement += ";"
                cursor.execute(select_statement)
                engine.connection.commit()
                
                lines = []
                for row in cursor.fetchall():
                    if include_pk:
                        start = 0
                    else:
                        start = 1
                    newline = ','.join([self.strvalue(row[i], i - 1)
                                        for i 
                                        in range(start, len(row))])
                    lines.append(newline + "\r\n")
                    
                # If a test fails, you can temporarily  uncomment this line
                # to print each line that doesn't match up together with the
                # line from the test file; this can be useful to find the
                # discrepancies
                # checkagainstfile(lines, "PanTHERIA_manual.txt")
                
                lines = ''.join(lines)                
                sum = getmd5(lines)
                
                self.assertEqual(sum, checksum)
                
                
def get_opts():
    """Checks for command line arguments"""
    optsdict = dict()
    #
    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:u:p:hod", ["engine=", "user=", "password=", "host=", "port=", "database="])        
        for opt, arg in opts:            
            if opt in ("-e", "--engine"):      
                optsdict["engine"] = arg                            
            if opt in ("-u", "--user"):      
                optsdict["username"] = arg                            
            elif opt in ("-p", "--password"):     
                optsdict["password"] = arg
            elif opt in ("-h", "--host"):                 
                if arg == "":
                    optsdict["hostname"] = "default"
                else:
                    optsdict["hostname"] = arg
            elif opt in ("-o", "--port"): 
                try:
                    optsdict["port"] = int(arg)
                except ValueError:
                    optsdict["port"] = "default"                 
            elif opt in ("-d", "--database"): 
                if arg == "":
                    optsdict["database"] = "default"
                else:
                    optsdict["database"] = arg                                 
                 
    except getopt.GetoptError:
        pass
    
    return optsdict

def getmd5(lines):
    """Get MD5 value of a set of lines."""
    sum = md5()
    for line in lines:
        sum.update(line)
    return sum.hexdigest()

def checkagainstfile(lines, filename):
    """Checks a set of lines against a file, and prints all lines that don't
    match."""
    TEST_DATA_LOCATION = "test_data"
    
    testfile = open(os.path.join(TEST_DATA_LOCATION, filename), 'rb')
    i = 0        
    for line in lines:
        i += 1
        print i
        line2 = testfile.readline()
        if line != line2:
            print i
            print "LINE1: " + line
            print "LINE2: " + line2
            values1 = line.split(',')
            values2 = line2.split(',')
            for i in range(0, len(values1)):
                if values1[i] != values2[i]:
                    print str(i) + ": " + values1[i] + ", " + values2[i]
    testfile.close()    
    

def final_cleanup(engine):
    """Perform final cleanup operations after all scripts have run."""
    # Delete empty directories in RAW_DATA_LOCATION, then delete that
    # directory if empty.
    engine.final_cleanup()
    try:
       data_dirs = os.listdir(engine.RAW_DATA_LOCATION)
       for dir in data_dirs:
           try:
               os.rmdir(os.path.join(engine.RAW_DATA_LOCATION, dir))
           except OSError:
               pass
    except OSError:
        pass
    try:
        os.rmdir(engine.RAW_DATA_LOCATION)
    except OSError:
        pass
        

def get_saved_connection(engine_name):
    parameters = dict()
    if os.path.isfile("connections.config"):
        config = open("connections.config", "rb")
        for line in config:
            values = line.rstrip('\n').split(',')
            if values[0] == engine_name:
                values = values[1:]
                for value in values:
                    parameter = value.split('::')[0]
                    saved_value = value.split('::')[1]
                    parameters[parameter] = saved_value
    return parameters    


def choose_engine(opts):
    """Prompts the user to select a database engine"""    
    from dbtk import ENGINE_LIST
    ENGINE_LIST = ENGINE_LIST()
    
    if "engine" in opts.keys():
        enginename = opts["engine"]    
    else:
        print "Choose a database engine:"
        for engine in ENGINE_LIST:
            if engine.abbreviation:
                abbreviation = "(" + engine.abbreviation + ") "
            else:
                abbreviation = ""
            print "    " + abbreviation + engine.name
        enginename = raw_input(": ")
        enginename = enginename.lower()
    
    engine = Engine()
    if not enginename:
        engine = ENGINE_LIST[0]
    else:
        for thisengine in ENGINE_LIST:
            if (enginename == thisengine.name.lower() 
                              or thisengine.abbreviation
                              and enginename == thisengine.abbreviation):
                engine = thisengine
        
    engine.opts = opts
    return engine    
