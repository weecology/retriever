"""Database Toolkit UI
This module contains the UI elements of the database toolkit platform.
"""

import sys
import wx
import wx.wizard
from dbtk_models import *

def launch_wizard(dbtk_list, engine_list):
    print "Launching Database Toolkit wizard . . ."        
    
    
    class TitledPage(wx.wizard.WizardPageSimple):
        """A standard wizard page with a title and label."""
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
        """The connection info page."""
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            #wx.wizard.EVT_WIZARD_PAGE_CHANGING(self, self.GetId(), self.Draw())        
            self.option = dict()
            self.sel = ""
            self.fields = wx.BoxSizer(wx.VERTICAL)
        def Draw(self, evt):
            """When the page is drawn, it may need to update its fields if the selected 
            database has changed."""
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
        """The dataset selection page."""
        def __init__(self, parent, title, label):        
            TitledPage.__init__(self, parent, title, label)
            scripts = [script.name for script in dbtk_list]
            self.scriptlist = wx.CheckListBox(self, -1, choices=scripts)
            self.scriptlist.SetCheckedStrings(scripts)
            self.sizer.Add(self.scriptlist)
            self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CheckValues)
        def CheckValues(self, evt):  
            """Users can't continue from this page without checking at least one dataset."""
            if len(self.scriptlist.GetCheckedStrings()) == 0 and evt.Direction:
                evt.Veto()                
    
    
    app = wx.PySimpleApp(False)
    
    wizard = wx.wizard.Wizard(None, -1, "Database Toolkit Wizard")
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
    page[1].sizer.Add(wx.StaticText(page[1], -1, "\n"))
    page[1].keepdata = wx.CheckBox(page[1], -1, "Keep raw data files")
    page[1].keepdata.SetValue(True)    
    page[1].sizer.Add(page[1].keepdata)
    page[1].uselocal = wx.CheckBox(page[1], -1, "Use locally archived files, if available")
    page[1].uselocal.SetValue(True)
    page[1].sizer.Add(page[1].uselocal)
        
    
    page.append(ConnectionInfoPage(wizard, "Connection Info", "Please enter the following connection information: \n"))
    page[1].Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, page[2].Draw)
    
    if len(dbtk_list) > 1:
        page.append(DatasetPage(wizard, "Select Datasets", "Check each dataset to be downloaded:\n"))
    
    page.append(TitledPage(wizard, "Finished", "That's it! Click Next to download and install your data."))

    
    for i in range(len(page) - 1):
        wx.wizard.WizardPageSimple_Chain(page[i], page[i + 1])
        
    wizard.FitToPage(page[0])    

    if wizard.RunWizard(page[0]):
        engine = page[2].engine
        options = page[2].option
        engine.keep_raw_data = page[1].keepdata.Value
        engine.use_local = page[1].uselocal
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
                                   maximum = len(scripts), style=wx.PD_CAN_ABORT | wx.PD_CAN_SKIP)
        dialog.Show()
        scriptnum = 0
        
        class UserSkipped(Exception):
            pass        
        class UserAborted(Exception):
            pass
        
        class update_dialog:
            """This function is called whenever the print statement is used, and redirects the output
            to the progress dialog."""
            def write(self, s):                
                txt = s.strip().translate(None, "\b")
                if txt:
                    (keepgoing, skip) = dialog.Update(scriptnum - 1, msg + "\n" + txt)
                    if not keepgoing:
                        raise UserAborted
                    if skip:
                        raise UserSkipped
                    
        sys.stdout = update_dialog()
        errors = []
        for script in scripts:
            scriptnum += 1
            msg = "Downloading " + script.name
            if len(scripts) > 0:
                msg += " (" + str(scriptnum) + " of " + str(len(scripts)) + ")" 
            msg += " . . ."                               
            try:
                script.download(engine)
            except UserSkipped:
                errors.append("Skipped " + script.name + ".")
            except UserAborted:
                dialog.Destroy()
                wx.MessageBox("Aborted.")
            except:
                errors.append("There was an error downloading " + script.name + ".")
                
        print "Finishing . . ."
        final_cleanup()
        dialog.Update(len(scripts), "Finished!")
        if errors:
            wx.MessageBox("The following errors occurred: \n" + '\n'.join(errors))
        else:
            wx.MessageBox("Your downloads were completed successfully.")
                
    wizard.Destroy()