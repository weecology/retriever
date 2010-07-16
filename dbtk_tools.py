"""Database Toolkit Tools
This module contains functions used to run database toolkits.
"""

import warnings
import xlrd
from dbtk_engines import *

warnings.filterwarnings("ignore")

class DbTk:
    """This class represents a database toolkit script. Scripts should inherit
    from this class and execute their code in the download method."""
    name = ""
    shortname = ""
    url = ""
    public = True
    def download(self, engine=None):
        pass
    def checkengine(self, engine=None):
        if not engine:
            opts = get_opts()        
            engine = choose_engine(opts)
        engine.script = self            
        return engine
    
    
def correct_invalid_value(value, args):
    try:
        if value in args["nulls"]:            
            return None
        else:
            return value
    except ValueError:
        return value    
    

def final_cleanup(RAW_DATA_LOCATION):
    """Perform final cleanup operations after all scripts have run."""
    # Delete empty directories in RAW_DATA_LOCATION, then delete that
    # directory if empty.
    try:
       data_dirs = os.listdir(RAW_DATA_LOCATION)
       for dir in data_dirs:
           try:
               os.rmdir(os.path.join(RAW_DATA_LOCATION, dir))
           except OSError:
               pass
    except OSError:
        pass
    try:
        os.rmdir(RAW_DATA_LOCATION)
    except OSError:
        pass
    
    
class DbtkError(Exception):
    pass            

def emptycell(cell):
    """Tests whether an excel cell is empty or contains only
    whitespace"""
    if cell.ctype == 0:
        return True
    if str(cell.value).strip() == "":
        return True
    return False

def cellvalue(cell):
    """Returns the string value of an excel spreadsheet cell"""
    return str(cell.value).strip()    