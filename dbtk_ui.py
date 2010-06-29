import wx
import wx.wizard
from dbtk_tools import *
from dbtk_ernest2003 import *
from dbtk_pantheria import *
from dbtk_bbs import *
from dbtk_portal_mammals import *

dbtk_list = [DbTk_Ernest(), DbTk_Pantheria(), DbTk_BBS(), DbTk_Portal_Mammals()]
engine_list = [MySQLEngine(), PostgreSQLEngine(), SQLiteEngine()]

class TitledPage(wx.wizard.WizardPageSimple):
    def __init__(self, parent, title):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        titleText = wx.StaticText(self, -1, title)
        titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


class DynamicPage(TitledPage):
    def __init__(self, parent, title):
        TitledPage.__init__(self, parent, title)
        #wx.wizard.EVT_WIZARD_PAGE_CHANGING(self, self.GetId(), self.Draw())        
        self.option = dict()
        self.sel = ""
    def Draw(self, evt):
        if len(page[1].dblist.GetStringSelection()) == 0 and evt.GetDirection():
            evt.Veto()                  
        else:
            if self.sel != page[1].dblist.GetStringSelection():
                self.sel = page[1].dblist.GetStringSelection()
                self.engine = Engine()
                for db in engine_list:
                    if db.name == self.sel:
                        self.engine = db     
                self.fields.Clear(True)
                self.fieldset = dict()
                for opt in self.engine.required_opts:
                    self.fieldset[opt[0]] = wx.BoxSizer(wx.HORIZONTAL)
                    label = wx.StaticText(self, -1, opt[0] + ": ", size=wx.Size(90,35))
                    if opt[0] == "password":
                        self.option[opt[0]] = wx.TextCtrl(self, -1, str(opt[2]), 
                                                          size=wx.Size(200,30), style=wx.TE_PASSWORD)
                    else:
                        self.option[opt[0]] = wx.TextCtrl(self, -1, str(opt[2]),
                                                          size=wx.Size(200,30))
                    self.fieldset[opt[0]].AddMany([label, self.option[opt[0]]])
                    self.fields.Add(self.fieldset[opt[0]])
                wizard.FitToPage(self)
        
        
class Wizard(wx.wizard.Wizard):
    def OnInit(self):
        wx.MessageBox("HI")
    pass
        
app = wx.App(False)
wizard = Wizard(None, -1, "Database Toolkit Wizard")
page = []
page.append(TitledPage(wizard, "Welcome"))
page[0].sizer.Add(wx.StaticText(page[0], -1, """Welcome to the Database Toolkit wizard.
 
This wizard will walk you through the process of downloading
and installing common ecological datasets to your own local 
database system."""))

page.append(TitledPage(wizard, "Select Database"))
page[1].sizer.Add(wx.StaticText(page[1], -1, "Please select your database platform:"))
page[1].dblist = wx.ListBox(page[1], -1, choices=[db.name for db in engine_list], style=wx.LB_SINGLE)
page[1].dblist.SetSelection(0)
page[1].sizer.Add(page[1].dblist,
                  0, wx.EXPAND | wx.ALL, 5)

page.append(DynamicPage(wizard, "Connection Info"))
page[2].sizer.Add(wx.StaticText(page[2], -1, "Please enter the following connection information: \n"))
page[2].fields = wx.BoxSizer(wx.VERTICAL)
page[2].sizer.Add(page[2].fields)
page[1].Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, page[2].Draw)

page.append(TitledPage(wizard, "Select Datasets"))
page[3].sizer.Add(wx.StaticText(page[3], -1, "Check each dataset to be downloaded:"))
page[3].scriptlist = wx.CheckListBox(page[3], -1, choices=[script.name for script in dbtk_list])
page[3].sizer.Add(page[3].scriptlist)

page.append(TitledPage(wizard, "Finished"))
page[4].sizer.Add(wx.StaticText(page[4], -1, "That's it! Your data will now be downloaded and installed."))

for i in range(0, 4):
    wx.wizard.WizardPageSimple_Chain(page[i], page[i + 1])
    
wizard.FitToPage(page[0])

if wizard.RunWizard(page[0]):
    engine = page[2].engine
    options = page[2].option
    opts = dict()
    for key in options.keys():
        opts[key] = options[key].GetValue()
    engine.opts = opts
    engine.get_cursor()
    
    for script in dbtk_list:
        if script.name in page[3].scriptlist.GetCheckedStrings():
            script.download(engine)