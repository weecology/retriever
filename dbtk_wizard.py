"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

"""

import os
from dbtks_EA_ernest2003 import *
from dbtks_EA_pantheria import *
from dbtks_bbs import *
from dbtks_EA_portal_mammals import *
from dbtks_gentry import *
from dbtks_CRC_avianbodymass import *
from dbtks_EA_avianbodysize2007 import *
import dbtk_ui

DBTK_LIST = [EAMammalLifeHistory2003(), 
             EAPantheria(), 
             EAPortalMammals(),
             EAAvianBodySize2007(),
             BBS(),
             Gentry(),
             CRCAvianBodyMass()
             ]

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
    dbtk_ui.launch_wizard(DBTK_LIST + other_dbtks, ALL_ENGINES)