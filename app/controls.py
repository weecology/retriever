import wx
import wx.lib.wxpTag
from dbtk import VERSION
from dbtk.lib.download import DownloadThread
        
        
class AboutDialog(wx.Dialog):
    text = """
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0" cellpadding="0" border="1">
<tr><td align="center"><h1>
Database Toolkit
</h1><h2>
version """ + VERSION + """
</h2></td></tr></table>
<p>The Database Toolkit is designed to make it easy to download ecological data and set it
up on your own local database system.
</p><p>
For more information, visit <a href="http://www.ecologicaldata.org">http://www.ecologicaldata.org</a>.
</p>
</body>"""
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "About", size=(440, 400))
        
        self.html = HtmlWindow(self)
        self.html.SetPage(self.text)
        
        self.button = wx.Button(self, wx.ID_OK, "OK")
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.html, 1, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(self.sizer)
        self.Layout()


class ScriptList(wx.HtmlListBox):
    def __init__(self, parent, scripts, style=0):
        self.scripts = scripts
        self.script_status = dict()
        wx.HtmlListBox.__init__(self, parent, -1, style=style)
        self.SetItemCount(len(scripts))
        self.Bind(wx.EVT_LISTBOX, self.RefreshMe)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.Download)
    
    def OnGetItem(self, index):
        return self.HtmlScriptSummary(index)

    def OnLinkClicked(self, n, link):
        if link.GetHref()[:10] == "download:/":
            self.SetSelection(int(link.GetHref().lstrip("download:/")))
            self.Download(None)
        else:
            wx.LaunchDefaultBrowser(link.GetHref())
        
    def Redraw(self, scripts):
        self.SetSelection(-1)
        self.scripts = scripts
        self.SetItemCount(len(scripts))
        self.Refresh()
        
    def RefreshMe(self, evt):
        self.RefreshAll()
        
    def Download(self, evt):
        script = self.scripts[self.GetSelection()]
        if self.Parent.Parent.progress_window.Download(script):
            self.SetStatus(script.name, "Waiting...")        
            
    def HtmlScriptSummary(self, index):
        script = self.scripts[index]
        selected = self.GetSelection() == index
        progress_window = self.Parent.Parent.progress_window
        engine = self.Parent.Parent.engine
        desc = "<table><tr><td>"
        link = None
        if script in progress_window.queue or (progress_window.worker and
                                               script == progress_window.worker.script):
            img = "cycle"
        else:
            if script in progress_window.errors:
                link = True
                img = "error"
            elif script in progress_window.downloaded or script.exists(engine):
                img = "downloaded"
            else:
                link = True
                img = "download"
        if img:
            img_tag = "<img src='memory:" + img + ".png' />"
            desc += ("<a href='download:/" + str(index) + "'>%s</a>" % img_tag
                     if link else img_tag)
        desc += "</td><td>"
        desc += ("<b>" + script.name + "</b>"
                 if selected else script.name)
        if script.reference_url():
            desc += "<br /><a href='" + script.reference_url() + "'>" 
            desc += script.reference_url() + "</a><br />"
        if selected:
            if script.addendum:
                desc += "<p><i>"
                desc += script.addendum.replace('\n', "<br />")
                desc += "</i></p>"
        if script.name in self.script_status.keys():
            desc += "<p>" + self.script_status[script.name] + "</p>"
        desc += "</td></tr></table>"
        return desc
        
        
    def SetStatus(self, script, txt):
        self.script_status[script] = "<p>" + txt + "</p>"
        self.RefreshAll()
        
        
class CategoryList(wx.ListBox):
    def __init__(self, parent, id, size=(-1,-1), choices=[], style=0):
        wx.ListBox.__init__(self, parent, id, size=size, 
                            choices=[choice.name for choice in choices], 
                            style=style)
        self.lists = choices
        self.Bind(wx.EVT_LISTBOX, self.Redraw)
    
    def Redraw(self, evt):
        if self.GetSelections():
            selected = self.lists[self.GetSelections()[0]]
            self.Parent.Parent.script_list.Redraw(selected.scripts)
            

class ProgressWindow(wx.html.HtmlWindow):
    def __init__(self, parent, style=0):
        wx.html.HtmlWindow.__init__(self, parent, style=style)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
        self.dialog = None
        self.html = ""
        self.worker = None
        self.queue = []
        self.downloaded = set()
        self.errors = set()
        self.help_text = """<h2>Welcome to the Database Toolkit!</h2>
<p>Choose from data categories on the left, and double click a dataset on the right
to begin your download.</p>"""
        self.timer = wx.Timer(self, -1)
        self.timer.interval = 10
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
    def SetHtml(self, html):
        self.html = html
        self.SetPage(self.help_text + self.html)
        
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
                self.refresh_html()

        wx.GetApp().Yield()
        return True
    
    def refresh_html(self):
        self.SetHtml(self.html)
        self.Scroll(-1, self.GetScrollRange(wx.VERTICAL))


class StaticText(wx.StaticText):
    def __init__(self, parent, id, label, size=wx.Size(-1,-1)):
        wx.StaticText.__init__(self, parent, id, label, size=size)
        #self.SetForegroundColour(wx.BLACK)
        
        
class TextCtrl(wx.TextCtrl):
    def __init__(self, parent, id, txt="", size=(-1,-1), style=0):
        wx.TextCtrl.__init__(self, parent, id, txt, size=size, style=style)
        #self.SetForegroundColour(wx.BLACK)
        #self.SetBackgroundColour(wx.WHITE)
        
 
class CheckBox(wx.CheckBox):
    def __init__(self, parent, id, label):
        wx.CheckBox.__init__(self, parent, id, label)
        #self.SetForegroundColour(wx.BLACK)
        #self.SetBackgroundColour(parent.Parent.bgcolor)


class ListBox(wx.ListBox):
    def __init__(self, parent, id, size=(-1,-1), choices=[], style=0):
        wx.ListBox.__init__(self, parent, id, size=size, choices=choices, style=style)
        #self.SetForegroundColour(wx.BLACK)
        #self.SetBackgroundColour(wx.WHITE)
        
        
class CheckListBox(wx.CheckListBox):
    def __init__(self, parent, id, size=(-1,-1), choices=[], style=0):
        wx.CheckListBox.__init__(self, parent, id, size=size, choices=choices, style=style)
        #self.SetForegroundColour(wx.BLACK)
        #self.SetBackgroundColour(wx.WHITE)
        
        
class HtmlCheckListBox(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=None, choices=None):
        wx.html.HtmlWindow.__init__(self, parent, size=size)

        self._check_box = """
<tr><td>
<wxp module="wx" class="CheckBox">
    <param name="id" value="%d" />
    <param name="label" value="" />
</wxp>
</td><td>
%s
</td></tr>"""

        self.checkboxes = dict()

        if choices:
            items = set()
            for choice in choices:
                i = wx.NewId()
                self.checkboxes[choice] = i
                items.append(self._check_box % (i, choice))
            self._html += (items)
            self.SetPage()
    
    def Clear(self):
        self._html = ""
        self.SetPage()
        
    def Append(self, txt):
        i = wx.NewId()
        self.checkboxes[txt] = i
        #if self._html:
            #self._html += "<hr />"
        self._html += (self._check_box % (i, txt))
        self.SetPage()
        
        self.Bind(wx.EVT_CHECKLISTBOX, self.Parent.OnCheck)
    
    def SetPage(self):
        wx.html.HtmlWindow.SetPage(self, "<table>" + self._html + "</table>")
        
    def GetCheckedStrings(self):
        return [key for key in self.checkboxes.keys()
                if self.FindWindowById(self.checkboxes[key]).GetValue()]
        
    def SetCheckedStrings(self, strings):
        for key in self.checkboxes.keys():
            self.FindWindowById(self.checkboxes[key]).SetValue(key in strings)
            
    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        

class TitledPage(wx.wizard.WizardPageSimple):
    """A standard wizard page with a title and label."""
    def __init__(self, parent, title, label):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        #self.SetBackgroundColour(parent.bgcolor)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        if title:
            titleText = wx.StaticText(self, -1, title)
            titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            #titleText.SetForegroundColour(wx.BLACK)
            self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        if label:
            self.AddSpace()
            label = wx.StaticText(self, -1, label)
            #label.SetForegroundColour(wx.BLACK)
            self.sizer.Add(label)
            self.AddSpace()
    def AddSpace(self, n=1):
        self.sizer.Add(wx.StaticText(self, -1, "\n" * n))
