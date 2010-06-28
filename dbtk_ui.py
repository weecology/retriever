import wx
from dbtk_tools import *
from dbtk_ernest2003 import *
from dbtk_pantheria import *
from dbtk_bbs import *
from dbtk_portal_mammals import *

dbtk_list = [DbTk_Ernest(), DbTk_Pantheria(), DbTk_BBS(), DbTk_Portal_Mammals()]

opts = get_opts()
engine = choose_engine(opts)
    
for dbtk in dbtk_list:
    print "Downloading " + dbtk.name    
    dbtk.download(engine)