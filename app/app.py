"""Contains implementations of wx.App and wx.Frame for the GUI."""

import wx
from retriever.app.connect_wizard import ConnectWizard
from retriever.app.controls import *
from retriever.app.download_manager import DownloadManager
from retriever.app.images import globe_icon, cycle, download, downloaded, error
from retriever.lib.tools import get_default_connection, get_saved_connection, choose_engine
from retriever import ENGINE_LIST

ENGINE_LIST = ENGINE_LIST()

class App(wx.App):
    def __init__(self, lists):
        wx.App.__init__(self, redirect=False)
        
        mfs = wx.MemoryFSHandler()
        wx.FileSystem_AddHandler(mfs)
        mfs.AddFile("globe.png", globe_icon.GetImage(), wx.BITMAP_TYPE_PNG)
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
        self.SetIcon(globe_icon.GetIcon())
        
        self.CreateStatusBar()        
        
        big_font = self.GetFont()
        big_font.SetPointSize(int(big_font.GetPointSize() * 1.2))
        
        # Menu
        self.menu = wx.Menu()
        self.menu.Append(wx.ID_ABOUT, "&About",
                    "More information about this program")
        connection_id = wx.NewId()
        self.menu.Append(connection_id, "&Connection",
                    "Set up your database connection")
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu, "&File");
        self.SetMenuBar(self.menu_bar)
        
        self.Bind(wx.EVT_CLOSE, self.Quit)
        self.Bind(wx.EVT_MENU, self.About, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.Connection, id=connection_id)
        self.Bind(wx.EVT_MENU, self.Quit, id=wx.ID_EXIT)
        
        # Layout
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter = wx.SplitterWindow(self, -1)
        
        self.cat_list = CategoryList(self.splitter, -1, style=wx.RAISED_BORDER | wx.LB_SINGLE,
                                     choices=self.lists)
        self.cat_list.SetSelection(0)
        self.cat_list.SetFont(big_font)
                
        self.script_list = ScriptList(self.splitter, 
                                      style=wx.RAISED_BORDER | wx.LB_SINGLE,
                                      scripts=[script for script in lists[0].scripts])
        
        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SplitVertically(self.cat_list, self.script_list, 200)
        
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
