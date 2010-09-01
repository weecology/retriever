"""Database Toolkit Wizard

This module contains a list of all current DBTK scripts.

Running this module directly will launch the download wizard, allowing the user
to choose from all scripts.

"""

from dbtks_EA_ernest2003 import *
from dbtks_EA_pantheria import *
from dbtks_bbs import *
from dbtks_EA_portal_mammals import *
from dbtks_gentry import *
#from dbtks_CRC_avianbodymass import *
from dbtks_EA_avianbodysize2007 import *
import dbtk_ui

DBTK_LIST = [EAMammalLifeHistory2003(), 
             EAPantheria(), 
             BBS(), 
             EAPortalMammals(),
             Gentry(),
             #CRCAvianBodyMass(),
             EAAvianBodySize2007()
             ]

if __name__ == "__main__":
    dbtk_ui.launch_wizard(DBTK_LIST, ALL_ENGINES)