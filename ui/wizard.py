"""Database Toolkit UI

This module contains the UI elements of the database toolkit platform. 

This module should not be run directly; instead, individual scripts, when run,
should run the launch_wizard function.

"""

import sys
import wx
import wx.wizard
from threading import Thread
from dbtk.lib.tools import final_cleanup
from dbtk.ui.pages import *
from dbtk.ui.download_page import DownloadPage
from dbtk import ENGINE_LIST

ENGINE_LIST = ENGINE_LIST()


class DbTkWizard(wx.wizard.Wizard):
    def __init__(self, parent, id, title, lists, engine_list):
        wx.wizard.Wizard.__init__(self, parent, id, title)
        
        welcome = """<h2>Welcome to the Database Toolkit wizard.</h2>
        
        <p>This wizard will walk you through the process of downloading and 
        installing ecological datasets.</p>
        <p>This wizard requires that you have one or more of the supported database 
        systems installed. You must also have either an active connection to the 
        internet, or the raw data files stored locally on your computer.</p>
        <p>Supported database systems currently include:</p>
        <ul>"""
        
        for db in engine_list:
            welcome += "<li>" + db.name + "</li>" 
        
        welcome += """</ul>
        <p><i>Version """ + VERSION + """</i></p>
        <p><a href="http://www.ecologicaldata.org">http://www.ecologicaldata.org</a></p>"""        
        
        self.pages = []
        self.lists = lists
        self.engine_list = engine_list
        
        self.pages.append(TitledPage(self, "", ""))
        
        self.pages.append(ChooseDbPage(self, "Select Database", 
                                      "Please select your database platform:\n"))
        
        self.pages.append(ConnectPage(self, 
                                     "Connection Info", 
                                     "Please enter your connection information: \n"))

        if len(self.lists) > 1:        
            self.pages.append(CategoriesPage(self, "Categories",
                                                 "Choose the dataset categories to be shown."))
        
        self.pages.append(DatasetPage(self, "Select Datasets", 
                               "Check each dataset to be downloaded:\n"))
        
        self.pages.append(FinishPage(self, "", ""))
        
        self.pages.append(DownloadPage(self, "", ""))

        
        if len(self.lists) > 1:
            (self.TITLE, self.CHOOSEDB, self.CONNECTION, self.CAT, self.DATASET, 
             self.FINISH, self.DOWNLOAD) = [self.pages[i] for i in range(7)]
        else:
            (self.TITLE, self.CHOOSEDB, self.CONNECTION, self.DATASET, 
             self.FINISH, self.DOWNLOAD) = [self.pages[i] for i in range(6)]
            self.dbtk_list = self.lists[0].scripts
            self.DATASET.Draw(None) 
            
        self.TITLE.welcome = HtmlWindow(self.TITLE)
        self.TITLE.welcome.SetPage(welcome)
        self.TITLE.sizer.Add(self.TITLE.welcome, 1, wx.EXPAND)
             
        self.CHOOSEDB.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CONNECTION.Draw)
        
        self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.Abort)

        
        for i in range(len(self.pages) - 1):
            wx.wizard.WizardPageSimple_Chain(self.pages[i], self.pages[i + 1])
        
        for page in self.pages:
            self.FitToPage(page)
        
    
    def check_for_updates(self):
        reload(dbtk)
        
                
    def Abort(self, evt):
        if self.DOWNLOAD.worker:
            self.DOWNLOAD.worker.output_lock.acquire()
        if self.GetCurrentPage() == self.DOWNLOAD:
            sys.exit()



def launch_wizard(lists):    
    """Launches the download wizard."""
    print "Launching Database Toolkit wizard..."                    
    
    # Create the wxPython app and wizard 
    app = wx.PySimpleApp(False)
    wizard = DbTkWizard(None, -1, "Database Toolkit", 
                        lists, ENGINE_LIST)

    # Run the wizard
    wizard.RunWizard(wizard.TITLE)
