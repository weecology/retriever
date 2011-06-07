"""Custom implementations of wxPython controls for use in the Retriever."""

import wx
import wx.lib.wxpTag
from retriever import VERSION, BUILD

        
class AboutDialog(wx.Dialog):
    text = """
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0" cellpadding="0" border="1">
<tr><td align="center"><h1>
EcoData Retriever
</h1><h2>
version """ + VERSION + " (" + BUILD + ")" + """
</h2></td></tr></table>
<p>The EcoData Retriever is designed to make it easy to download ecological data and set it
up on your own local database system.
</p><p>
To get started, double click on a dataset to download the data files and import the data into
your database.
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
        if self.Parent.Parent.download_manager.Download(script):
            self.SetStatus(script.name, "Waiting...")        
            
    def HtmlScriptSummary(self, index):
        script = self.scripts[index]
        selected = self.GetSelection() == index
        download_manager = self.Parent.Parent.download_manager
        engine = self.Parent.Parent.engine
        desc = "<table><tr><td>"
        link = None
        if script in download_manager.queue or (download_manager.worker and
                                               script == download_manager.worker.script):
            img = "cycle"
        else:
            if script in download_manager.errors:
                link = True
                img = "error"
            elif script in download_manager.downloaded or script.exists(engine):
                img = "downloaded"
            else:
                link = True
                img = "download"
        if img:
            img_tag = "<img src='memory:" + img + ".png' />"
            desc += ("<a href='download:/" + str(index) + "'>%s</a>" % img_tag
                     if link else img_tag)
        desc += "</td><td>"
        desc += "<b>" + script.name + "</b>"
        if script.description:
            desc += "<p>" + script.description + "</p>"
        if script.reference_url():
            desc += "<p><a href='" + script.reference_url() + "'>" 
            desc += script.reference_url() + "</a></p>"
        if selected:
            if script.addendum:
                desc += "<p><i>"
                desc += script.addendum.replace('\n', "<br />")
                desc += "</i></p>"
        if script.name in self.script_status.keys():
            desc += "<p>" + self.script_status[script.name] + "</p>"
        desc += "</td></tr></table><hr />"
        return desc
        
        
    def SetStatus(self, script, txt):
        self.script_status[script] = "<p>" + txt + "</p>"
        self.RefreshMe(None)
        
        
class CategoryList(wx.TreeCtrl):
    def __init__(self, parent, id, choice_tree, size=(-1,-1), style=0):
        wx.TreeCtrl.__init__(self, parent, id, size=size, style=style)        
        self.lists = choice_tree
        self.root = self.AddRoot(choice_tree.name)
        for choice in choice_tree.children:
            self.AddChild(choice)
            
        self.Expand(self.root)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.Redraw)
        
        
    def AddChild(self, choice, parent=None):
        new_node = self.AppendItem(self.root if parent == None else parent,
                                   choice.name)
        self.SetItemPyData(new_node, choice)
        for child in choice.children:
            self.AddChild(child, new_node)
        
    def SelectRoot(self):
        self.SelectItem(self.root)
    
    
    def Redraw(self, evt):
        if evt.GetItem() == self.root:
            selected = self.lists
        else:
            selected = self.GetItemPyData(evt.GetItem())

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
