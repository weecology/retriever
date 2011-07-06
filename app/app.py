"""Contains implementations of wx.App and wx.Frame for the GUI."""

import wx
from retriever.app.connect_wizard import ConnectWizard
from retriever.app.controls import *
from retriever.app.download_manager import DownloadManager
from retriever.app.images import icon, cycle, download, downloaded, error
from retriever.lib.tools import get_default_connection, get_saved_connection, choose_engine
from retriever.lib.lists import Category
from retriever import ENGINE_LIST, SCRIPT_LIST

ENGINE_LIST = ENGINE_LIST()

class App(wx.App):
    def __init__(self, lists):
        wx.App.__init__(self, redirect=False)
        
        mfs = wx.MemoryFSHandler()
        wx.FileSystem_AddHandler(mfs)
        mfs.AddFile("globe.png", icon.GetImage(), wx.BITMAP_TYPE_PNG)
        mfs.AddFile("cycle.png", cycle.GetImage(), wx.BITMAP_TYPE_PNG)
        mfs.AddFile("download.png", download.GetImage(), wx.BITMAP_TYPE_PNG)
        mfs.AddFile("downloaded.png", downloaded.GetImage(), wx.BITMAP_TYPE_PNG)
        mfs.AddFile("error.png", error.GetImage(), wx.BITMAP_TYPE_PNG)
        
        default_connection = get_default_connection()
        if default_connection:
            parameters = get_saved_connection(default_connection)
            parameters["engine"] = default_connection
            engine = choose_engine(parameters)
        else:
            wizard = ConnectWizard(lists, ENGINE_LIST)

            success = wizard.RunWizard(wizard.pages[0])
        
            if not success:
                wizard.Destroy()
                return
        
            engine = wizard.CONNECTION.engine
            options = wizard.CONNECTION.option
            opts = dict()
            for key in options.keys():
                opts[key] = options[key].GetValue()
            engine.opts = opts
            wizard.Destroy()
        
        try:
            engine.get_connection()
        except:
            pass
        
        self.frame = Frame(None, -1, "EcoData Retriever", lists, engine)
        self.frame.Show()
        
        
class Frame(wx.Frame):
    def __init__(self, parent, ID, title, lists, engine):
        wx.Frame.__init__(self, parent, ID, title,
                          size=(800, 550))
        
        self.download_manager = DownloadManager(self)
        
        self.dialog = None
        self.lists = lists
        self.engine = engine
        self.SetIcon(icon.GetIcon())
        
        self.CreateStatusBar()        
        
        big_font = self.GetFont()
        big_font.SetPointSize(int(big_font.GetPointSize() * 1.2))
        
        # Menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_ABOUT, "&About",
                    "More information about this program")
        connection_id = wx.NewId()
        file_menu.Append(connection_id, "&Connection",
                    "Set up your database connection")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
        
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_FIND, "&Find")
        
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File");
        menu_bar.Append(edit_menu, "E&dit");
        self.SetMenuBar(menu_bar)
        
        self.Bind(wx.EVT_CLOSE, self.Quit)
        self.Bind(wx.EVT_MENU, self.About, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.Connection, id=connection_id)
        self.Bind(wx.EVT_MENU, self.Quit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.Find, id=wx.ID_FIND)
        
        # Layout
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self, -1)
        
        self.cat_list = CategoryList(self.splitter, -1, choice_tree=self.lists,
                                     style=wx.TR_HAS_BUTTONS)
        self.cat_list.SetFont(big_font)
                
        self.script_list = ScriptList(self.splitter, 
                                      style=wx.RAISED_BORDER | wx.LB_SINGLE,
                                      scripts=[script for script in lists.scripts])

        self.cat_list.SelectRoot()
        
        
        self.splitter.SetMinimumPaneSize(300)
        self.splitter.SplitVertically(self.cat_list, self.script_list, 300)
        
        self.vsizer.Add(self.splitter, 3, wx.EXPAND | wx.ALL, 2)
        
        self.SetSizer(self.vsizer)
        self.vsizer.Layout()
        
    def About(self, evt):
        dlg = AboutDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    
    def Connection(self, evt):
        if self.download_manager.worker or self.download_manager.queue:
            dlg = wx.MessageDialog(self, 
                                   "You can't change the connection while datasets are downloading.",
                                   style=wx.OK)
            dlg.ShowModal()
        else:
            wizard = ConnectWizard(self.lists, ENGINE_LIST, self.engine.name)

            success = wizard.RunWizard(wizard.pages[1])
        
            if not success:
                wizard.Destroy()
                return
        
            engine = wizard.CONNECTION.engine
            options = wizard.CONNECTION.option
            opts = dict()
            for key in options.keys():
                opts[key] = options[key].GetValue()
            engine.opts = opts
            wizard.Destroy()
            self.engine = engine
            try:
                self.engine.get_connection()
            except:
                pass
                
            self.download_manager.downloaded = set()
            self.download_manager.errors = set()
            self.script_list.script_status = dict()
            self.script_list.RefreshMe(None)
            
    def Quit(self, evt):
        if self.download_manager.worker:
            dlg = wx.MessageDialog(self, 
                                   'Your download is still in progress. Are you sure you want to quit?', 
                                   'Quit',
                                   wx.YES | wx.NO)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self.download_manager.worker = None
            else:
                if self.download_manager.dialog:
                    self.download_manager.dialog.Resume()
                self.download_manager.timer.Start(self.download_manager.timer.interval)
                return
                
        if self.download_manager.dialog:
            self.download_manager.dialog.Destroy()
        
        self.Destroy()
        
        
    def Find(self, evt):
        dlg = wx.TextEntryDialog(self, 
                                 'Enter the keyword(s) to search for', 
                                 'Find',
                                 '')
        dlg.ShowModal()
        result = dlg.GetValue().strip()
        
        if result:
            search_terms = [term.strip() for term in result.split(' ') 
                                         if term.strip()]
            scripts = []
            for script in SCRIPT_LIST():
                if script.matches_terms(search_terms):
                    scripts.append(script)
                    
            if len(scripts) > 0:
                results = Category("Search results: " + ', '.join(search_terms),
                                   scripts)
                self.cat_list.AddChild(results, select=True)
            else:
                wx.MessageBox("Your search returned no results.",
                              "No results")
            
        dlg.Destroy()
