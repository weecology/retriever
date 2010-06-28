import wx
import dbtk_tools
from dbtk_ernest2003 import *
from dbtk_pantheria import *
from dbtk_bbs import *
from dbtk_portal_mammals import *

dbtk_list = [DbTk_Ernest(), DbTk_Pantheria(), DbTk_BBS(), DbTk_Portal_Mammals()]

for dbtk in dbtk_list:
    print dbtk.name