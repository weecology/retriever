import sys
import wx
import wx.wizard
from dbtk_tools import *

def launch_wizard(dbtk_list, engine_list):
    print "Launching Database Toolkit wizard . . ."
    
    def download_scripts():
        engine = page[2].engine
        options = page[2].option
        engine.keep_raw_data = page[1].keepdata.Value
        opts = dict()
        for key in options.keys():
            opts[key] = options[key].GetValue()
        engine.opts = opts
        engine.get_cursor()
        
        scripts = []
        for script in dbtk_list:
            dl = False
            if len(dbtk_list) > 1:
                if script.name in page[3].scriptlist.GetCheckedStrings():
                    dl = True
            else:
                dl = True
            if dl:
                scripts.append(script)
        dialog = wx.ProgressDialog('Download Progress', 'Downloading datasets . . . . . . . . . . . . . .\n', 
                                   maximum = len(scripts))
        dialog.Show()
        scriptnum = 0
        class update_dialog:
            def write(self, s):                
                txt = s.strip().translate(None, "\b")
                if txt:
                    dialog.Update(scriptnum - 1, msg + "\n" + txt)
        sys.stdout = update_dialog()
        for script in scripts:
            scriptnum += 1
            msg = "Downloading " + script.name
            if len(scripts) > 0:
                msg += " (" + str(scriptnum) + " of " + str(len(scripts)) + ")" 
            msg += " . . ."                               
            try:
                script.download(engine)
            except:
                print "There was an error downloading " + script.name
                raise
        dialog.Update(len(scripts), "Finished!")        
    
    
    class TitledPage(wx.wizard.WizardPageSimple):
        def __init__(self, parent, title, label):
            wx.wizard.WizardPageSimple.__init__(self, parent)
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.SetSizer(self.sizer)
            titleText = wx.StaticText(self, -1, title)
            titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
            self.label = wx.StaticText(self, -1)
            self.sizer.Add(self.label, 0, wx.EXPAND | wx.ALL, 5)
            self.label.Wrap(100)
            if label:
                self.sizer.Add(wx.StaticText(self, -1, label))
    
    
    class ConnectionInfoPage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            #wx.wizard.EVT_WIZARD_PAGE_CHANGING(self, self.GetId(), self.Draw())        
            self.option = dict()
            self.sel = ""
            self.fields = wx.BoxSizer(wx.VERTICAL)
        def Draw(self, evt):
            if len(page[1].dblist.GetStringSelection()) == 0 and evt.Direction:
                evt.Veto()                  
            else:
                if self.sel != page[1].dblist.GetStringSelection():
                    self.sel = page[1].dblist.GetStringSelection()
                    self.engine = Engine()
                    for db in engine_list:
                        if db.name == self.sel:
                            self.engine = db
                    self.fields.Clear(True)     
                    self.fields = wx.BoxSizer(wx.VERTICAL)                
                    self.fieldset = dict()
                    self.option = dict()
                    for opt in self.engine.required_opts:
                        self.fieldset[opt[0]] = wx.BoxSizer(wx.HORIZONTAL)
                        label = wx.StaticText(self, -1, opt[0] + ": ", size=wx.Size(90,35))
                        if opt[0] == "password":
                            self.option[opt[0]] = wx.TextCtrl(self, -1, str(opt[2]), 
                                                              size=wx.Size(200,-1), style=wx.TE_PASSWORD)
                        else:
                            self.option[opt[0]] = wx.TextCtrl(self, -1, str(opt[2]),
                                                              size=wx.Size(200,-1))
                        self.fieldset[opt[0]].AddMany([label, self.option[opt[0]]])
                        self.fieldset[opt[0]].Layout()
                        self.fields.Add(self.fieldset[opt[0]])
                    #self.fields = wx.BoxSizer(wx.VERTICAL)
                    self.fields.Layout()
                    self.sizer.Add(self.fields)
                    self.sizer.Layout()
    
    
    class DatasetPage(TitledPage):
        def __init__(self, parent, title, label):        
            TitledPage.__init__(self, parent, title, label)
            scripts = [script.name for script in dbtk_list]
            self.scriptlist = wx.CheckListBox(self, -1, choices=scripts)
            self.scriptlist.SetCheckedStrings(scripts)
            self.sizer.Add(self.scriptlist)
            self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CheckValues)
        def CheckValues(self, evt):  
            if len(self.scriptlist.GetCheckedStrings()) == 0 and evt.Direction:
                evt.Veto()


    class LastPage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.DisableBackButton)
        def DisableBackButton(self, evt):
            wizard.FindWindowById(wx.ID_BACKWARD).Enable(False)            
                
    
    class DownloadPage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.Download)            
        def Download(self, evt):
            if evt.Direction:
                download_scripts()
            
                                
    class Wizard(wx.wizard.Wizard):
        pass        
    
    
    app = wx.PySimpleApp(False)
    
    wizard = Wizard(None, -1, "Database Toolkit Wizard")
    page = []
    if len(dbtk_list) > 1:
        dataset = "common ecological datasets"
    else:
        dataset = "data from " + dbtk_list[0].name 
    
    page.append(TitledPage(wizard, "Welcome", """Welcome to the Database Toolkit wizard.
     
This wizard will walk you through the process of downloading
and installing """ + dataset + """.
   
This wizard requires that you have one or more of the supported
database systems installed on your machine, and an active
connection to the internet.
    
Supported database systems currently include:\n\n""" + ", ".join([db.name for db in engine_list])))
    
    page.append(TitledPage(wizard, "Select Database", "Please select your database platform:\n"))
    page[1].dblist = wx.ListBox(page[1], -1, choices=[db.name for db in engine_list], style=wx.LB_SINGLE)
    page[1].dblist.SetSelection(0)
    page[1].sizer.Add(page[1].dblist,
                      0, wx.EXPAND | wx.ALL, 5)
    page[1].keepdata = wx.CheckBox(page[1], -1, "Keep raw data files")
    page[1].sizer.Add(wx.StaticText(page[1], -1, "\n"))
    page[1].sizer.Add(page[1].keepdata)    
    
    page.append(ConnectionInfoPage(wizard, "Connection Info", "Please enter the following connection information: \n"))
    page[1].Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, page[2].Draw)
    
    if len(dbtk_list) > 1:
        page.append(DatasetPage(wizard, "Select Datasets", "Check each dataset to be downloaded:\n"))
    
    page.append(DownloadPage(wizard, "Finished", "That's it! Click Next to download and install your data."))
    
    page.append(LastPage(wizard, "Finished", "Your downloads are complete. Click Finish to exit."))
    
    for i in range(len(page) - 1):
        wx.wizard.WizardPageSimple_Chain(page[i], page[i + 1])
        
    wizard.FitToPage(page[0])    
    wizard.RunWizard(page[0])        
    wizard.Destroy()