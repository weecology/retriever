"""Database Toolkit Tools
This module contains functions used to run database toolkits.
"""

import warnings
from dbtk_engines import *

warnings.filterwarnings("ignore")

class DbTk:
    """This class represents a database toolkit script. Scripts should inherit from this class
    and execute their code in the download method."""
    name = ""
    url = ""
    def download(self, engine=None):
        pass
    def checkengine(self, engine=None):
        if not engine:
            opts = get_opts()        
            engine = choose_engine(opts)
        return engine
    
    
def correct_invalid_value(value, args):
    try:
        if value in args["nulls"]:            
            return None
        else:
            return value
    except ValueError:
        return value    
    

def final_cleanup():
    """Perform final cleanup operations after all scripts have run."""
    try:
        os.rmdir(raw_data_location)
    except OSError:
        pass