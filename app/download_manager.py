import wx
from retriever.lib.download import DownloadThread


class DownloadManager:
    def __init__(self, parent):
        self.dialog = None
        self.worker = None
        self.queue = []
        self.downloaded = set()
        self.errors = set()
        self.Parent = parent
        self.timer = wx.Timer(parent, -1)
        self.timer.interval = 10
        parent.Bind(wx.EVT_TIMER, self.update, self.timer)
        
    def Download(self, script):
        if not script in self.queue and not (self.worker and self.worker.script == script):
            self.queue.append(script)
            self.downloaded.add(script)
            if script in self.errors:
                self.errors.remove(script)
            self.Parent.script_list.RefreshMe(None)
            if not self.timer.IsRunning() and not self.worker and len(self.queue) < 2:
                self.timer.Start(self.timer.interval)
            return True
        return False
    
    def update(self, evt):
        self.timer.Stop()
        terminate = False
        if self.worker:
            script = self.worker.script
            if self.worker.finished() and len(self.worker.output) == 0:
                self.Parent.SetStatusText("")
                self.worker = None
                self.Parent.script_list.RefreshMe(None)
                self.timer.Start(self.timer.interval)
            else:
                self.worker.output_lock.acquire()
                while len(self.worker.output) > 0 and not terminate:
                    if "Error:" in self.worker.output[0] and script in self.downloaded:
                        self.downloaded.remove(script)
                        self.errors.add(script)
                    if self.write(self.worker) == False:
                        terminate = True
                    self.worker.output = self.worker.output[1:]
                #self.gauge.SetValue(100 * ((self.worker.scriptnum) /
                #                           (self.worker.progress_max + 1.0)))
                self.worker.output_lock.release()
                if terminate:
                    self.Parent.Quit(None)
                else:
                    self.timer.Start(self.timer.interval)
        elif self.queue:
            script = self.queue[0]
            self.queue = self.queue[1:]
            self.worker = DownloadThread(self.Parent.engine, script)
            self.worker.parent = self
            self.worker.start()
            self.timer.Start(10)
    
    def write(self, worker):
        s = worker.output[0]
        
        if '\b' in s:
            s = s.replace('\b', '')
            if not self.dialog:
                wx.GetApp().Yield()
                self.dialog = wx.ProgressDialog("Download Progress", 
                                                "Downloading datasets . . .\n"
                                                + "  " * len(s), 
                                                maximum=1000,
                                                parent=None,
                                                style=wx.PD_SMOOTH
                                                      | wx.DIALOG_NO_PARENT
                                                      | wx.PD_CAN_ABORT
                                                      | wx.PD_AUTO_HIDE
                                                      | wx.PD_REMAINING_TIME
                                                )
            def progress(s):
                if ' / ' in s:
                    s = s.split(' / ')
                    total = float(s[1])
                    current = float(s[0].split(': ')[1])
                    progress = int((current / total) * 1000)
                    return (progress if progress > 1 else 1)
                else:
                    return None
                    
            current_progress = progress(s)
            if current_progress:
                (keepgoing, skip) = self.dialog.Update(current_progress, s)
            else:
                (keepgoing, skip) = self.dialog.Pulse(s)
                
            if not keepgoing:
                return False
        else:
            if self.dialog:
                self.dialog.Update(1000, "")
                self.dialog.Destroy()
                self.dialog = None
            
            if '...' in s:
                self.Parent.SetStatusText(s)
            else:
                self.Parent.script_list.SetStatus(worker.script.name, s)

        wx.GetApp().Yield()
        return True
