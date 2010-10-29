import wx
import wx.lib.wxpTag
from dbtk import VERSION
from dbtk.app.icon import globe_icon
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
        wx.HtmlListBox.__init__(self, parent, -1, style=style)
        self.scripts = scripts
        self.SetItemCount(len(scripts))
        self.Bind(wx.EVT_LISTBOX, self.RefreshMe)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.Download)
    
    def OnGetItem(self, index):
        return HtmlScriptSummary(self.scripts[index], 
                                 self.GetSelection()==index,
                                 self.Parent.Parent.progress_window)

    def OnLinkClicked(self, n, link):
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
        self.Parent.Parent.progress_window.Download(script)
        
        
def HtmlScriptSummary(script, selected, progress_window):
    desc = "<table><tr><td>"
    if script in progress_window.queue or (progress_window.worker and
                                           script in progress_window.worker.scripts):
        img = "cycle"
    else:
        if script in progress_window.downloaded:
            img = "downloaded"
        else:
            img = "download"
    desc += "<img src='memory:" + img + ".png' />"
    desc += "</td><td>"
    if selected:
        desc += "<b>" + script.name + "</b>" 
    else:
        desc += script.name
    if script.reference_url():
        desc += "<br /><a href='" + script.reference_url() + "'>" 
        desc += script.reference_url() + "</a><br />"
    if selected:
        if script.addendum:
            desc += "<p><i>"
            desc += script.addendum.replace('\n', "<br />")
            desc += "</i></p>"
    '''if selected:
        desc += "</td></tr>"
        desc += """<tr><td><wxp module="wx" class="Button">
    <param name="id" value='""" + str(wx.ID_OK) + """' />
    <param name="label" value="Download" />
</wxp>"""        '''
    desc += "</td></tr></table>"
    return desc
        
        
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


class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, style=0):
        wx.html.HtmlWindow.__init__(self, parent, style=style)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
    def SetHtml(self, html):
        self.SetPage(html)
        #self.SetBackgroundColour(self.Parent.Parent.bgcolor)
            

class ProgressWindow(HtmlWindow):
    dialog = None
    html = ""
    worker = None
    queue = []
    downloaded = set()
    def __init__(self, parent, style=0):
        HtmlWindow.__init__(self, parent, style=style)
        self.timer = wx.Timer(self, -1)
        self.timer.interval = 10
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
    def Download(self, script):
        self.queue.append(script)
        self.downloaded.add(script)
        self.Parent.script_list.RefreshMe(None)
        if not self.timer.IsRunning() and not self.worker and len(self.queue) < 2:
            self.timer.Start(self.timer.interval)
    
    def update(self, evt):
        self.timer.Stop()
        terminate = False
        if self.worker:
            if self.worker.finished() and len(self.worker.output) == 0:
                self.worker = None
                self.Parent.script_list.RefreshMe(None)
                self.timer.Start(self.timer.interval)
            else:
                self.worker.output_lock.acquire()
                while len(self.worker.output) > 0 and not terminate:
                    if self.write(self.worker.output[0]) == False:
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
            self.worker = DownloadThread(self.Parent.engine, [script])
            self.worker.parent = self
            self.worker.start()
            self.timer.Start(10)
    
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
                return False
        else:
            if self.dialog:
                self.dialog.Update(1000, "")
                self.dialog.Destroy()
                self.dialog = None
            if "inserting" in s.lower() and not "<font" in s.lower():
                s = "<font color='green'>" + s + "</font>"
            self.html += "\n<p>" + s + "</p>"
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
