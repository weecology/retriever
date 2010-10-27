"""Classes representing pages for the DBTK wizard.

"""

import os
import sys
import wx
import wx.html
import wx.wizard
from dbtk.lib.models import Engine
from dbtk.lib.templates import TEMPLATES
from dbtk.lib.tools import get_saved_connection
from dbtk.ui.add_dataset import AddDatasetWizard
from dbtk.ui.controls import *
from dbtk import VERSION


class ChooseDbPage(TitledPage):
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        engine_list = parent.engine_list
        
        dblist = ListBox(self, -1, 
                         choices=[db.name for db in engine_list], 
                         style=wx.LB_SINGLE)
        self.dblist = dblist
        self.dblist.SetSelection(0)
        self.sizer.Add(self.dblist, 0, wx.EXPAND)
        self.AddSpace()
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)    
        self.sizer2.Add(StaticText(self, -1, "Data file directory:", 
                                   size=wx.Size(150,35)))
        self.raw_data_dir = TextCtrl(self, -1, 
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
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.SaveConnection)
    def SaveConnection(self, evt):
        if self.save_connection.Value:
            if os.path.isfile("connections.config"):
                config = open("connections.config", "rb")
                lines = []
                for line in config:
                    if line.split(',')[0] != self.engine.name:
                        lines.append(line.rstrip('\n') + '\n')
                config.close()
                os.remove("connections.config")
                config = open("connections.config", "wb")
                for line in lines:
                    config.write(line)
            else:
                config = open("connections.config", "wb")                    
            connection = self.engine.name
            for key in self.option.keys():
                connection += ','
                connection += key + '::' + self.option[key].Value
            config.write(connection)
            config.close()
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
                self.save_connection = CheckBox(self, -1, "Save connection")
                self.save_connection.SetValue(True)
                self.fields.Add(self.save_connection)
                self.fields.Layout()
                self.sizer.Add(self.fields)
                self.sizer.Layout()


class CategoriesPage(TitledPage):
    """The dataset selection page."""
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)           
        # CheckListBox of scripts
        lists = [list.name for list in parent.lists]
        self.catlist = CheckListBox(self, -1, choices=lists)
        self.catlist.SetCheckedStrings(["All Datasets"])
        self.sizer.Add(self.catlist, 0, wx.EXPAND)
        self.catlist.Bind(wx.EVT_CHECKLISTBOX, self.OnCheck)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.GetScripts)
    def OnCheck(self, evt):
        index = evt.GetSelection()
        clicked = self.catlist.GetString(index)
        status = self.catlist.IsChecked(index)
        if clicked == "All Datasets":
            if status:
                self.catlist.SetCheckedStrings(["All Datasets"])
        else:
            checked = self.catlist.GetCheckedStrings()
            if len(checked) > 1 and "All Datasets" in checked:
                self.catlist.Check(0, False)
    def GetScripts(self, evt):
        if evt.Direction:
            self.Parent.dbtk_list = []
            for checked_list in self.catlist.GetCheckedStrings():
                this_list = [list for list in self.Parent.lists
                             if list.name == checked_list][0]
                for script in this_list.scripts:
                    if not script in self.Parent.dbtk_list:
                        self.Parent.dbtk_list.append(script)
            if len(self.Parent.dbtk_list) == 0:
                evt.Veto()
            self.Parent.DATASET.Draw(None)
        
            
class DatasetPage(TitledPage):
    """The dataset selection page."""
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        # Check that at least one dataset is selected before proceeding
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.CheckValues) 
        # All checkbox
        self.checkallbox = CheckBox(self, -1, "All")
        self.sizer.Add(self.checkallbox)
        self.checkallbox.Bind(wx.EVT_CHECKBOX, self.CheckAll)
        # CheckListBox of scripts
        self.scriptlist = CheckListBox(self, -1, size=(-1,200))
        self.sizer.Add(self.scriptlist, 0, wx.EXPAND)
        self.scriptlist.Bind(wx.EVT_CHECKLISTBOX, self.OnCheck)
        # Add dataset button
        self.addbtn = wx.Button(self, -1, "Add...")
        self.sizer.Add(self.addbtn)
        self.addbtn.Bind(wx.EVT_BUTTON, self.AddDataset)
    def Draw(self, evt):
        dbtk_list = self.Parent.dbtk_list
        self.scriptlist.Clear()
        for script in [str(script) for script in dbtk_list]:
            self.scriptlist.Append(script)
        public_scripts = [str(script) for script in dbtk_list if script.public]
        self.scriptlist.SetCheckedStrings(public_scripts)
        self.OnCheck(None)
    def OnCheck(self, evt):
        checked = self.scriptlist.GetCheckedStrings()
        self.checkallbox.SetValue(len(checked) == len(self.Parent.dbtk_list))
    def AddDataset(self, evt):
        # Run Add Dataset wizard
        add_dataset = AddDatasetWizard(self.Parent, -1, 'Add Dataset')            
        if add_dataset.RunWizard(add_dataset.pages[0]):                
            dataset_url = add_dataset.url.GetValue()
            dbname = add_dataset.dbname.GetValue()
            tablename = add_dataset.tablename.GetValue()
            if not tablename:
                tablename = dbname
            fullname = dbname
            if tablename:
                fullname += "." + tablename              
            if dbname and dataset_url:
                if not (fullname in self.scriptlist.GetItems()):
                    # Add dataset to list
                    temp = add_dataset.templates.GetStringSelection()
                    for template in TEMPLATES:
                        if template[0] == temp:
                            new_dataset = template[1]
                    
                    new_dataset.name = fullname
                    new_dataset.shortname = dbname
                    new_dataset.tablename = tablename
                    new_dataset.url = dataset_url
                    
                    
                    self.Parent.dbtk_list.append(new_dataset)
                    self.scriptlist.Append(fullname)
                    
                    # Append dataset to scripts.config file
                    if os.path.isfile("scripts.config"):
                        mode = 'ab'
                        initial = "\n"                            
                    else:
                        mode = 'wb'
                        initial = ""
                    config = open("scripts.config", mode)                        
                    config.write(initial + temp + "," + dbname + "," + tablename + "," + dataset_url)
                else:
                    wx.MessageBox("You already have a dataset named " + dataset_name + ".")
                # Automatically check the new dataset
                self.scriptlist.SetCheckedStrings(self.scriptlist.GetCheckedStrings() + (fullname,))
        add_dataset.Destroy()
    def CheckAll(self, evt):
        if self.checkallbox.GetValue():
            self.scriptlist.SetCheckedStrings([str(script) for script in self.Parent.dbtk_list])
        else:
            self.scriptlist.SetCheckedStrings([])
    def CheckValues(self, evt):  
        """Users can't continue from this page without checking at least
        one dataset."""
        if len(self.scriptlist.GetCheckedStrings()) == 0 and evt.Direction:
            evt.Veto()
        elif evt.Direction:
            checked = self.scriptlist.GetCheckedStrings()
            warn = [script.name for script in self.Parent.dbtk_list 
                    if not script.public and str(script) in checked]
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
            self.Parent.FINISH.Draw(None)


class FinishPage(TitledPage):
    """The dataset selection page."""
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        self.summary = HtmlWindow(self)
        self.sizer.Add(self.summary, 1, wx.EXPAND)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.StartDownloads)
    def StartDownloads(self, evt):
        if evt.Direction:
            self.Parent.DOWNLOAD.Draw(None) 
    def Draw(self, evt):
        checked_scripts = self.Parent.DATASET.scriptlist.GetCheckedStrings()
        html = "<h2>Finished</h2><p>That's it! Click Next to download your data.</p>"
        html += "<p>Download summary:</p><ul>"
        for script in self.Parent.dbtk_list:
            if str(script) in checked_scripts:
                html += "<li>" + script.name
                if script.reference_url():
                    html += ' (<a href="' + script.reference_url() + '">About</a>)'
                if script.addendum:
                    html += "<p><i>"
                    html += script.addendum.replace("\n", "<br />")
                    html += "</i></p>"
                html += "</li>"
        html += "</ul>"
        self.summary.SetHtml(html)
