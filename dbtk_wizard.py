from dbtk_ernest2003 import *
from dbtk_pantheria import *
from dbtk_bbs import *
from dbtk_portal_mammals import *
import dbtk_ui

dbtk_list = [DbTk_Ernest(), DbTk_Pantheria(), DbTk_BBS(), DbTk_Portal_Mammals()]

dbtk_ui.launch_wizard(dbtk_list, all_engines)