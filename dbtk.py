"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

"""

import os
from scripts import *
from lib.ui import *

MODULE_LIST = [EA_ernest2003,
               EA_pantheria,
               EA_portal_mammals,
               EA_avianbodysize2007,
               bbs,
               gentry,
               CRC_avianbodymass]

DBTK_LIST = [module.main() for module in MODULE_LIST]

# Get list of additional datasets from dbtk.config file
other_dbtks = []
if os.path.isfile("dbtk.config"):
    config = open("dbtk.config", 'rb')
    for line in config:
        if line:
            line = line.rstrip("\n")
            values = line.split(', ')
            try:
                dbname, tablename, url = (values[0], values[1], values[2])
                other_dbtks.append(AutoDbTk(
                                            dbname + "." + tablename, 
                                            dbname, 
                                            tablename, 
                                            url))
            except:
                pass


if __name__ == "__main__":
    launch_wizard(DBTK_LIST + other_dbtks, ALL_ENGINES)