"""Database Toolkit UI

This module contains the UI elements of the database toolkit platform. 

This module should not be run directly; instead, individual scripts, when run,
should run the launch_wizard function.

"""

import sys
import wx
import wx.wizard
from threading import Thread
from tools import final_cleanup
from dbtk.lib.ui_pages import DbTkWizard
from dbtk.lib.engines import ALL_ENGINES


def launch_wizard(lists):    
    """Launches the download wizard."""
    print "Launching Database Toolkit wizard . . ."                    
    
    # Create the wxPython app and wizard 
    app = wx.PySimpleApp(False)
    wizard = DbTkWizard(None, -1, "Database Toolkit Wizard", 
                        lists, ALL_ENGINES)

    # Run the wizard
    wizard.RunWizard(wizard.TITLE)
        
    #app.MainLoop()
