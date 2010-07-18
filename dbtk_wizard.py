"""Database Toolkit Wizard
This module runs a wizard to download from multiple DBTK datasets.

"""

from dbtks_ernest2003 import *
from dbtks_pantheria import *
from dbtks_bbs import *
from dbtks_portal_mammals import *
from dbtks_gentry import *
from dbtks_avianbodymass import *
import dbtk_ui

DBTK_LIST = [MammalLifeHistory(), 
             Pantheria(), 
             BBS(), 
             PortalMammals(),
             Gentry(),
             AvianBodyMass()
             ]

dbtk_ui.launch_wizard(DBTK_LIST, ALL_ENGINES)