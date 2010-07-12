"""Database Toolkit for CRC Handbook of Avian Bird Masses companion CD

NOTE: This data is not publicly available. To download the data, you'll need
the CRC Avian Body Masses CD. Create a new directory at 
raw_data/AvianBodyMass and copy the contents of the CD there before running
this script.

"""

from dbtk_ui import *

class AvianBodyMass(DbTk):
    name = "CRC Avian Body Masses"
    shortname = "AvianBodyMass"
    public = False
    required_opts = []
    def download(self, engine=None):    
        # Variables to get text file/create database
        engine = self.checkengine(engine)
        
        
        
if __name__ == "__main__":
    me = AvianBodyMass()
    if len(sys.argv) == 1:                
        launch_wizard([me], ALL_ENGINES)
    else:
        me.download()
        final_cleanup()