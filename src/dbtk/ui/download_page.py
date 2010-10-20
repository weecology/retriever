"""Wizard page that starts download thread and updates on download progress."""

import wx
from dbtk.ui.controls import *
from dbtk.lib.download import DownloadThread


class DownloadPage(TitledPage):
    def __init__(self, parent, title, label):
        TitledPage.__init__(self, parent, title, label)
        self.summary = HtmlWindow(self)
        self.gauge = wx.Gauge(self, -1, 100, size=(-1,20), style=wx.GA_SMOOTH)
        self.sizer.Add(self.summary, 1, wx.EXPAND)
        self.sizer.Add(self.gauge, 0, wx.EXPAND)
        self.sizer.Layout()
        self.dialog = None
        self.worker = None
        
    def Draw(self, evt):
        self.Parent.FindWindowById(wx.ID_FORWARD).Disable()
        self.SetPrev(None)
        self.html = "<h2>Download Progress</h2>\n"
        self.html += "<p>Beginning downloads . . .</p>"
        self.summary.SetHtml(self.html)
        
        # Get options from wizard
        engine = self.Parent.CONNECTION.engine
        options = self.Parent.CONNECTION.option
        engine.RAW_DATA_LOCATION = self.Parent.CHOOSEDB.raw_data_dir.Value
        opts = dict()
        for key in options.keys():
            opts[key] = options[key].GetValue()
        engine.opts = opts
        
        # Get a list of scripts to be downloaded
        scripts = []
        checked_scripts = self.Parent.DATASET.scriptlist.GetCheckedStrings()
        for script in self.Parent.dbtk_list:
            dl = False
            if len(self.Parent.dbtk_list) > 1:
                if script.name in checked_scripts:
                    dl = True
            else:
                dl = True
            if dl:
                scripts.append(script)
        
        class wxDownloadThread(DownloadThread):        
            def run(self):
                DownloadThread.run(self)
                self.parent.FindWindowById(wx.ID_CANCEL).Disable()
                self.parent.FindWindowById(wx.ID_FORWARD).Enable()                
                
        self.worker = wxDownloadThread(engine, scripts)        
        self.worker.parent = self.Parent
        self.worker.start()

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def update(self, evt):
        self.timer.Stop()
        terminate = False
        if self.worker:
            self.worker.output_lock.acquire()
            while len(self.worker.output) > 0:                    
                if self.write(self.worker.output[0]) == False:
                    terminate = True
                self.worker.output = self.worker.output[1:]
            self.gauge.SetValue(100 * ((self.worker.scriptnum) /
                                       (self.worker.progress_max + 1.0)))
            if not self.worker.finished():
                self.timer.Start(1)
            self.worker.output_lock.release()                
            if terminate:
                self.Parent.Abort(None)
    
    def write(self, s):
        if '\b' in s:
            s = s.replace('\b', '')
            if not self.dialog:
                self.html += "\n<p><font color='green'>" + s.split(':')[0] + "</font></p>"
                self.refresh_html()
                wx.GetApp().Yield()
                self.dialog = wx.ProgressDialog("Download Progress", 
                                                "Downloading datasets . . .\n"
                                                + "  " * len(s), 
                                                maximum=100,
                                                parent=self.Parent,
                                                style=wx.PD_CAN_ABORT 
                                                      | wx.PD_SMOOTH
                                                      | wx.PD_AUTO_HIDE
                                                )
            def progress(s):
                if ' / ' in s:
                    s = s.split(' / ')
                    total = float(s[1])
                    current = float(s[0].split(': ')[1])
                    progress = int((current / total) * 100)
                    if progress < 1:
                        return 1
                    else:
                        return progress
                else:
                    return None
                    
            current_progress = progress(s)
            if current_progress:
                (keepgoing, skip) = self.dialog.Update(current_progress, s)
            else:
                (keepgoing, skip) = self.dialog.Pulse(s)
                
            if not keepgoing:
                self.dialog.Update(100, "")
                self.dialog = None
                return False
        else:
            if self.dialog:
                self.dialog.Update(100, "")
                self.dialog = None
            if "inserting" in s.lower() and not "<font" in s.lower():
                s = "<font color='green'>" + s + "</font>"
            self.html += "\n<p>" + s + "</p>"
            self.refresh_html()

        wx.GetApp().Yield()
        return True
    
    def refresh_html(self):
        self.summary.SetHtml(self.html)
        self.summary.Scroll(-1, self.summary.GetScrollRange(wx.VERTICAL))
