import wx
from dbtk.lib.templates import TEMPLATES
from dbtk.wizard.controls import *


class AddDatasetWizard(wx.wizard.Wizard):
    """Wizard for adding custom datasets"""
    def __init__(self, parent, id, title):
        wx.wizard.Wizard.__init__(self, parent, id, title)
        
        self.bgcolor = parent.bgcolor
        
        self.SetBackgroundColour(self.bgcolor)
        
        self.pages = []
        self.pages.append(self.ChooseTemplatePage(self, "Choose a Template", 
                                                  "Select a dataset template."))
        self.pages.append(self.AddDatasetPage(self, "Add Dataset", ""))
        
        for i in range(len(self.pages) - 1):
            wx.wizard.WizardPageSimple_Chain(self.pages[i], self.pages[i + 1])
        
        for page in self.pages:
            self.FitToPage(page)
            
        
    class ChooseTemplatePage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            parent.templates = ListBox(self, -1, 
                            choices=[template[0] for template in TEMPLATES], 
                            style=wx.LB_SINGLE)
            parent.templates.SetSelection(0)
            self.sizer.Add(parent.templates, 0, wx.EXPAND)
            
                            
    class AddDatasetPage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            self.AddSpace()
            parent.url = TextCtrl(self, -1, "http://",
                                     size=wx.Size(250,-1))
            parent.dbname = TextCtrl(self, -1, "",
                                        size=wx.Size(250,-1))
            parent.tablename = TextCtrl(self, -1, "",
                                           size=wx.Size(250,-1))
            
            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.hbox = dict()            
            for item in [(parent.url, "URL:"),
                         (parent.dbname, "Database Name:"),
                         (parent.tablename, "Table Name:")]:
                self.hbox[item[1]] = wx.BoxSizer(wx.HORIZONTAL)
                label = StaticText(self, -1, item[1], size=wx.Size(120,35))                        
                self.hbox[item[1]].AddMany([label,
                                            item[0]])
                self.hbox[item[1]].Layout()
                self.vbox.Add(self.hbox[item[1]])
            
            self.vbox.Layout()
            self.sizer.Add(self.vbox)
            self.sizer.Layout()
