"""EcoData Retriever Tools

This module contains miscellaneous classes and functions used in Retriever 
scripts.

"""

import os
import sys
import warnings
import unittest
from decimal import Decimal
from hashlib import md5
from retriever.lib.models import *

warnings.filterwarnings("ignore")

TEST_ENGINES = dict()


class ScriptTest(unittest.TestCase):
    """Automates the process of creating unit tests for Retriever scripts.
    Uses the Python unittest module."""
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
        """The default unit test. Tests in ScriptTest classes can simply call 
        this function with the appropriate paramaters. The "script" property 
        should be an instance of Script, and tables is a list consisting of 
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
                
                
def name_matches(scripts, arg):
    return [script for script in scripts 
            if arg.lower() in
            (script.shortname.lower(), script.name.lower(), script.filename.lower())
            or arg.lower() in [tag.strip().lower() for tagset in script.tags for tag in tagset.split('>')]
            or arg.lower() == 'all'
            ]
                
                
def get_opts(scripts, args=sys.argv[1:]):
    """Checks for command line arguments"""
    optsdict = dict()
    n = 0
    while n < len(args):
        opt = args[n]
        try:
            if opt in ("help", "--help"):
                pass
            elif opt in ("update", "--update"):
                optsdict["update"] = True
            elif opt in ("force", "--force", "compile", "--compile"):
                optsdict["force"] = True
            elif opt in ("-s", "--script", "install"):
                n += 1
                try:
                    matches = name_matches(scripts, args[n])
                    if len(matches) == 1:
                        optsdict["script"] = matches[0]
                    elif len(matches) > 1:
                        optsdict["script"] = matches
                except IndexError:
                    pass
            elif opt in ("-e", "--engine"):
                n += 1
                optsdict["engine"] = args[n]
                engine = choose_engine(optsdict, choice=False)
                if engine:
                    defaults = engine.required_opts
                for default in defaults:
                    if not default[0] in optsdict.keys() and default[2]:
                        optsdict[default[0]] = default[2]
            elif opt in ("-u", "--user"):
                n += 1
                optsdict["username"] = args[n]
            elif opt in ("-p", "--password"): 
                n += 1    
                optsdict["password"] = args[n]
            elif opt in ("-h", "--host"):
                n += 1
                optsdict["hostname"] = args[n]
            elif opt in ("-o", "--port"): 
                n += 1
                try:
                    optsdict["port"] = int(args[n])
                except ValueError:
                    print "Invalid port number:", args[n]
                    optsdict["port"] = "default"                 
            elif opt in ("-f", "--file"):
                n += 1
                optsdict["file"] = args[n]
            elif opt in ("-d", "--database"): 
                n += 1
                optsdict["database"] = args[n]
            elif opt in ("--debug",):
                optsdict["debug"] = True
            elif opt[:2] == '--':
                opt = opt[2:]
                n += 1
                try:
                    optsdict[opt] = eval(args[n])
                except:
                    optsdict[opt] = args[n]

            n += 1

        except IndexError:
            print "Not enough arguments to", args[n-1]
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
    pass
        

def get_saved_connection(engine_name):
    """Given the name of an engine, returns the stored connection for that engine
    from connections.config."""
    parameters = dict()
    if os.path.isfile("connections.config"):
        config = open("connections.config", "rb")
        for line in config:
            values = line.rstrip('\n').split(',')
            if values[0] == engine_name:
                try:
                    parameters = eval(','.join(values[1:]))
                except:
                    pass
    return parameters    


def save_connection(engine_name, values_dict):
    """Saves connection information for an engine in connections.config."""
    lines = []
    if os.path.isfile("connections.config"):
        config = open("connections.config", "rb")
        for line in config:
            if line.split(',')[0] != engine_name:
                lines.append('\n' + line.rstrip('\n'))
        config.close()
        os.remove("connections.config")
        config = open("connections.config", "wb")
    else:
        config = open("connections.config", "wb")
    config.write(engine_name + "," + str(values_dict))
    for line in lines:
        config.write(line)
    config.close()
    
    
def get_default_connection():
    """Gets the first (most recently used) stored connection from 
    connections.config."""
    if os.path.isfile("connections.config"):
        config = open("connections.config", "rb")
        default_connection = config.readline().split(",")[0]
        config.close()
        return default_connection
    else:
        return None


def choose_engine(opts, choice=True):
    """Prompts the user to select a database engine"""    
    from retriever import ENGINE_LIST
    ENGINE_LIST = ENGINE_LIST()
    
    if "engine" in opts.keys():
        enginename = opts["engine"]    
    else:
        if not choice: return None
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
