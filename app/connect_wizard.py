"""Connection setup wizard.

"""

import os
import sys
import wx
import wx.html
import wx.wizard
from retriever.lib.models import Engine
from retriever.lib.tools import get_saved_connection, save_connection
from retriever.app.controls import *
from retriever.app.images import globe_icon

from retriever import VERSION


class ConnectWizard(wx.wizard.Wizard):
    def __init__(self, lists, engine_list, selected=None):
        wx.wizard.Wizard.__init__(self, None, -1, "Database Toolkit")
        
        self.SetIcon(globe_icon.GetIcon())
        
        welcome = """<h2>Connection Wizard</h2>
        
        <p>The EcoData Retriever downloads raw data files, stores them on your
        computer, and imports the data into your own local database.</p>
        <p>To begin, you'll need to set up your own database. Once you've done
        that, this wizard will walk you through the steps to connect to your
        database.</p>
        <p>Supported database systems currently include:</p>
        <ul>"""
        
        for db in engine_list:
            welcome += "<li>" + db.name + "</li>" 
        
        welcome += "</ul>"        
        
        self.pages = []
        self.lists = lists
        self.engine_list = engine_list
        self.selected = selected
        
        self.pages.append(TitledPage(self, "", ""))
        
        self.pages.append(ChooseDbPage(self, "Database", 
                                       "What kind of database are you using?"))
        
        self.pages.append(ConnectPage(self, 
                                      "Connection Info", 
                                      ""))

        self.TITLE, self.CHOOSEDB, self.CONNECTION = [self.pages[i] 
                                                      for i in range(len(self.pages))]
        
        self.TITLE.welcome = HtmlWindow(self.TITLE)
        self.TITLE.welcome.SetSize((450,400))
        self.TITLE.welcome.SetHtml(welcome)
        self.TITLE.sizer.Add(self.TITLE.welcome, 1, wx.EXPAND)
             
        self.CHOOSEDB.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CONNECTION.Draw)
        
        for i in range(len(self.pages) - 1):
            wx.wizard.WizardPageSimple_Chain(self.pages[i], self.pages[i + 1])
        
        for page in self.pages:
            self.FitToPage(page)
        
    
    def check_for_updates(self):
        reload(retriever)


class ChooseDbPage(TitledPage):
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        engine_list = parent.engine_list
        
        dblist = ListBox(self, -1, 
                         choices=[db.name for db in engine_list], 
                         style=wx.LB_SINGLE,
                         size=(-1,150))
        self.dblist = dblist
        if parent.selected:
            index = 0
            for i in range(len(engine_list)):
                if engine_list[i].name == parent.selected:
                    index = i                                    
            self.dblist.SetSelection(index)
        else:
            self.dblist.SetSelection(0)
        self.sizer.Add(self.dblist, -1, wx.EXPAND)
        
    def dirbtn_click(self, evt):
        dialog = wx.DirDialog(None, message="Choose a directory to " +
                                "download your data files.")            
        if dialog.ShowModal() == wx.ID_OK:            
           self.raw_data_dir.SetValue(dialog.GetPath())            
        else:
           pass
        dialog.Destroy()
                    

class ConnectPage(TitledPage):
    """The connection info page."""
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        self.option = dict()
        self.sel = ""
        self.fields = wx.BoxSizer(wx.VERTICAL)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.SaveConnection)
    def SaveConnection(self, evt):
        values_dict = dict()
        for key in self.option.keys():
            values_dict[key] = str(self.option[key].Value)
        save_connection(self.engine.name, values_dict)
    def Draw(self, evt):
        """When the page is drawn, it may need to update its fields if 
        the selected database has changed."""
        if len(self.Parent.CHOOSEDB.dblist.GetStringSelection()) == 0 and evt.Direction:
            evt.Veto()                  
        else:
            if self.sel != self.Parent.CHOOSEDB.dblist.GetStringSelection():
                self.sel = self.Parent.CHOOSEDB.dblist.GetStringSelection()
                self.engine = Engine()
                for db in self.Parent.engine_list:
                    if db.name == self.sel:
                        self.engine = db
                self.fields.Clear(True)     
                self.fields = wx.BoxSizer(wx.VERTICAL)
                if self.engine.instructions:
                    self.fields.Add(StaticText(self, -1, '\n' + self.engine.instructions + '\n\n'))
                self.fieldset = dict()
                self.option = dict()
                saved_opts = get_saved_connection(self.engine.name)
                for opt in self.engine.required_opts:
                    if opt[0] in saved_opts.keys():
                        default = saved_opts[opt[0]]
                    else:
                        default = opt[2]
                    self.fieldset[opt[0]] = wx.BoxSizer(wx.HORIZONTAL)
                    label = StaticText(self, -1, opt[0] + ": ", 
                                          size=wx.Size(90,35))
                    if opt[0] == "password":
                        txt = TextCtrl(self, -1, 
                                          str(default), 
                                          size=wx.Size(200,-1), 
                                          style=wx.TE_PASSWORD)
                    else:
                        txt = TextCtrl(self, -1, str(default),
                                          size=wx.Size(200,-1))
                    self.option[opt[0]] = txt
                    self.fieldset[opt[0]].AddMany([label, 
                                                   self.option[opt[0]]])
                    if opt[0] == "file":
                        def open_file_dialog(evt):
                            filter = ""
                            if opt[3]:
                                filter = opt[3] + "|"
                            filter += "All files (*.*)|*.*"                                    
                            dialog = wx.FileDialog(None, style = wx.OPEN,
                                                   wildcard = filter)
                            if dialog.ShowModal() == wx.ID_OK:
                                self.option[opt[0]].SetValue(dialog.GetPath())
                        self.browse = wx.Button(self, -1, "Choose...")
                        self.fieldset[opt[0]].Add(self.browse)
                        self.browse.Bind(wx.EVT_BUTTON, open_file_dialog)                        
                    self.fieldset[opt[0]].Layout()
                    self.fields.Add(self.fieldset[opt[0]])
                self.sizer.Add(self.fields)
                self.sizer.Layout()
