"""Database Toolkit UI
This module contains the UI elements of the database toolkit platform.

"""

import sys
import wx
import wx.wizard
from dbtk_tools import *

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


    class ChooseDbPage(TitledPage):
        def __init__(self, parent, title, label):
            TitledPage.__init__(self, parent, title, label)
            dblist = wx.ListBox(self, -1, 
                                choices=[db.name for db in engine_list], 
                                style=wx.LB_SINGLE)
            self.dblist = dblist
            self.dblist.SetSelection(0)
            self.sizer.Add(self.dblist,
                              0, wx.EXPAND | wx.ALL, 5)
            self.sizer.Add(wx.StaticText(self, -1, "\n"))
            self.keepdata = wx.CheckBox(self, -1, "Keep raw data files")
            self.keepdata.SetValue(True)    
            self.sizer.Add(self.keepdata)
            self.uselocal = wx.CheckBox(self, -1, 
                                        "Use locally archived files, " +
                                        "if available")
            self.uselocal.SetValue(True)
            self.sizer.Add(self.uselocal)
            self.sizer.Add(wx.StaticText(self, -1, "\n"))
            self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)    
            self.sizer2.Add(wx.StaticText(self, -1, "Data file directory:", 
                                  size=wx.Size(150,35)))
            self.raw_data_dir = wx.TextCtrl(self, -1, 
                                            Engine().RAW_DATA_LOCATION,
                                            size=wx.Size(200,-1))
            self.sizer2.Add(self.raw_data_dir)
            self.dirbtn = wx.Button(self, id=-1, label='Change...',
                                    size=(120, -1))
            self.sizer2.Add(self.dirbtn)
            self.sizer.Add(self.sizer2)                    
            self.dirbtn.Bind(wx.EVT_BUTTON, self.dirbtn_click)
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
        def Draw(self, evt):
            """When the page is drawn, it may need to update its fields if 
            the selected database has changed."""
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
                        label = wx.StaticText(self, -1, opt[0] + ": ", 
                                              size=wx.Size(90,35))
                        if opt[0] == "password":
                            txt = wx.TextCtrl(self, -1, 
                                              str(opt[2]), 
                                              size=wx.Size(200,-1), 
                                              style=wx.TE_PASSWORD)
                        else:
                            txt = wx.TextCtrl(self, -1, str(opt[2]),
                                              size=wx.Size(200,-1))
                        self.option[opt[0]] = txt
                        self.fieldset[opt[0]].AddMany([label, 
                                                       self.option[opt[0]]])
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
            
            public_scripts = [script.name for script in dbtk_list if script.public]
            self.scriptlist.SetCheckedStrings(public_scripts)
            self.sizer.Add(self.scriptlist)
            self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CheckValues)
        def CheckValues(self, evt):  
            """Users can't continue from this page without checking at least
            one dataset."""
            if len(self.scriptlist.GetCheckedStrings()) == 0 and evt.Direction:
                evt.Veto()
            elif evt.Direction:
                checked = self.scriptlist.GetCheckedStrings()
                warn = [script.name for script in dbtk_list 
                        if not script.public and script.name in checked]
                if warn:
                    warning = "Warning: the following datasets are not "
                    warning += "publicly available. You must have the raw "
                    warning += "data files in your data file directory first."
                    warning += "\n\n" + ','.join(warn) + "\n\n"
                    warning += "Do you want to continue?"
                    warndialog = wx.MessageDialog(None, 
                                                  warning, 
                                                  "Warning", 
                                                  style = wx.YES_NO)
                    if warndialog.ShowModal() != wx.ID_YES:
                        evt.Veto()
                         
    
    
    app = wx.PySimpleApp(False)
    
    wizard = wx.wizard.Wizard(None, -1, "Database Toolkit Wizard")
    page = []
    if len(dbtk_list) > 1:
        dataset = "common ecological datasets"
    else:
        dataset = "data from " + dbtk_list[0].name 
    
    page.append(TitledPage(wizard, "Welcome", 
"""Welcome to the Database Toolkit wizard.

This wizard will walk you through the process of downloading
and installing """ + dataset + """.

This wizard requires that you have one or more of the supported
database systems installed. You must also have either an active
connection to the internet, or the raw data files stored locally 
on your computer.

Supported database systems currently include:\n\n""" + 
", ".join([db.name for db in engine_list])))
    
    page.append(ChooseDbPage(wizard, "Select Database", 
                           "Please select your database platform:\n"))
    
    page.append(ConnectPage(wizard, 
                            "Connection Info", 
                            "Please enter your connection information: \n"))
    page[1].Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, page[2].Draw)
    
    if len(dbtk_list) > 1:
        page.append(DatasetPage(wizard, "Select Datasets", 
                                "Check each dataset to be downloaded:\n"))
    
    page.append(TitledPage(wizard, "Finished", 
                           "That's it! Click Finish to download and install " +
                           "your data."))

    
    for i in range(len(page) - 1):
        wx.wizard.WizardPageSimple_Chain(page[i], page[i + 1])
        
    wizard.FitToPage(page[0])    

    if wizard.RunWizard(page[0]):
        # Get a list of scripts to be downloaded
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
                
        # Find the script with the longest name to set size of progress dialog        
        longestname = 0
        for script in scripts:
            if len(script.name) > longestname:
                longestname = len(script.name)
                
        # Create progress dialog 
        dialog = wx.ProgressDialog("Download Progress", 
                                   "Downloading datasets . . ." + 
                                   " " * longestname + "\n", 
                                   maximum = len(scripts), 
                                   style=wx.PD_CAN_ABORT | wx.PD_CAN_SKIP)
        
        dialog.Show()
        scriptnum = 0
        
        # On stdout, the progress dialog updates
        class update_dialog:
            """This function is called whenever the print statement is used,
            and redirects the output to the progress dialog."""
            def write(self, s):                
                txt = s.strip().replace("\b", "")
                if txt:
                    prog = scriptnum - 1
                    if prog < 0:
                        prog = 0
                    (keepgoing, skip) = dialog.Update(prog, 
                                                      msg + "\n" + txt)
                    if not keepgoing:
                        raise UserAborted
                    if skip:
                        raise UserSkipped
                    
        oldstdout = sys.stdout
        sys.stdout = update_dialog()
        
        msg = "Connecting to database:"
        print "Connecting  . . ."     
                
        # Get options from wizard
        engine = page[2].engine
        options = page[2].option
        engine.keep_raw_data = page[1].keepdata.Value
        engine.use_local = page[1].uselocal.Value
        engine.RAW_DATA_LOCATION = page[1].raw_data_dir.Value
        opts = dict()
        for key in options.keys():
            opts[key] = options[key].GetValue()
        engine.opts = opts
        
        # Connect
        try:
            engine.get_cursor()
        except Exception as e:
            wx.MessageBox("There was an error with your database" 
                          + " connection. \n\n" +
                          e.__str__())
            raise
        
        class UserSkipped(Exception):
            pass        
        class UserAborted(Exception):
            pass
        
        # Download scripts
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
                sys.stdout = oldstdout
                dialog.Destroy()                
                wx.MessageBox("Cancelled.")
                final_cleanup(engine)
                sys.exit()
            except Exception as e:
                errors.append("There was an error downloading " + 
                              script.name + ".")
                wx.MessageBox(e.__str__(), "Error")
                
        print "Finishing . . ."
        final_cleanup(engine)
        dialog.Update(len(scripts), "Finished!")
        if errors:
            wx.MessageBox("The following errors occurred: \n" + 
                          '\n'.join(errors))
        else:
            wx.MessageBox("Your downloads were completed successfully.")
                
    wizard.Destroy()