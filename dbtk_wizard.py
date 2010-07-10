"""Database Toolkit Wizard
This module runs a wizard to download from multiple DBTK datasets.
"""

from dbtks_ernest2003 import *
from dbtks_pantheria import *
from dbtks_bbs import *
from dbtks_portal_mammals import *
import dbtk_ui

dbtk_list = [DbTk_Ernest(), DbTk_Pantheria(), DbTk_BBS(), DbTk_Portal_Mammals()]

dbtk_ui.launch_wizard(dbtk_list, all_engines)