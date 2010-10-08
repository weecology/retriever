"""Wizard page that starts download thread and updates on download progress."""

import wx
from threading import Thread, Lock
from dbtk.ui.pages import TitledPage, HtmlWindow
from dbtk.ui.download import download_scripts


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
        self.summary.SetPage(self.html)
        
        class DownloadThread(Thread):
            def __init__(self, parent):
                Thread.__init__(self)
                self.parent = parent
                self.scriptnum = 0
                self.progress_max = 1
                self.daemon = True
                self.output_lock = Lock()
                self.output = []
            def run(self):
                download_scripts(self, self.parent)
                self.scriptnum = self.progress_max + 1
                self.parent.FindWindowById(wx.ID_CANCEL).Disable()
                self.parent.FindWindowById(wx.ID_FORWARD).Enable()
                
        self.worker = DownloadThread(self.Parent)
        self.worker.start()

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def update(self, evt):
        self.timer.Stop()
        if self.worker:
            self.worker.output_lock.acquire()
            while len(self.worker.output) > 0:                    
                self.write(self.worker.output[0])
                self.worker.output = self.worker.output[1:]
            self.gauge.SetValue(100 * ((self.worker.scriptnum) /
                                       (self.worker.progress_max + 1.0)))
            if self.worker.scriptnum < self.worker.progress_max + 1:
                self.timer.Start(1)
            self.worker.output_lock.release()                
    
    def write(self, s):
        if '\b' in s:
            s = s.replace('\b', '')
            if not self.dialog:
                self.html += "<font color='green'>" + s.split(':')[0] + "</font>"
                self.refresh_html()
                wx.GetApp().Yield()
                self.dialog = wx.ProgressDialog("Download Progress", 
                                                "Downloading datasets . . .\n"
                                                + "  " * len(s), 
                                                maximum=2,
                                                parent=self.Parent,
                                                style=wx.PD_CAN_ABORT 
                                                      | wx.PD_SMOOTH
                                                      | wx.PD_AUTO_HIDE
                                                )
            (keepgoing, skip) = self.dialog.Pulse(s)
            if not keepgoing:
                self.dialog.Update(2, "")
                self.dialog = None
                self.Parent.Abort(None)
        else:
            if self.dialog:
                self.dialog.Update(2, "")
                self.dialog = None
            if "inserting" in s.lower() and not "<font" in s.lower():
                s = "<font color='green'>" + s + "</font>"
            self.html += "\n<p>" + s + "</p>"
            self.refresh_html()

        wx.GetApp().Yield()
    
    def refresh_html(self):
        self.summary.SetPage(self.html)
        self.summary.Scroll(-1, self.summary.GetScrollRange(wx.VERTICAL))
