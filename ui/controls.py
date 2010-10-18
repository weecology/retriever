import wx


class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent):
        wx.html.HtmlWindow.__init__(self, parent, size=(-1,300))
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
    def SetHtml(self, html):
        self.SetPage(html)
        self.SetBackgroundColour(self.Parent.Parent.bgcolor)
        

class StaticText(wx.StaticText):
    def __init__(self, parent, id, label, size=wx.Size(-1,-1)):
        wx.StaticText.__init__(self, parent, id, label, size=size)
        self.SetForegroundColour(wx.BLACK)
        
        
class TextCtrl(wx.TextCtrl):
    def __init__(self, parent, id, txt="", size=(-1,-1), style=None):
        wx.TextCtrl.__init__(self, parent, id, txt, size=size, style=0)
        self.SetForegroundColour(wx.BLACK)
        self.SetBackgroundColour(wx.WHITE)
        
 
class CheckBox(wx.CheckBox):
    def __init__(self, parent, id, label):
        wx.CheckBox.__init__(self, parent, id, label)
        self.SetForegroundColour(wx.BLACK)
        self.SetBackgroundColour(parent.Parent.bgcolor)


class ListBox(wx.ListBox):
    def __init__(self, parent, id, size=(-1,-1), choices=[], style=0):
        wx.ListBox.__init__(self, parent, id, size=size, choices=choices, style=style)
        self.SetForegroundColour(wx.BLACK)
        self.SetBackgroundColour(wx.WHITE)
        
        
class CheckListBox(wx.CheckListBox):
    def __init__(self, parent, id, size=(-1,-1), choices=[]):
        wx.CheckListBox.__init__(self, parent, id, size=size, choices=choices)
        self.SetForegroundColour(wx.BLACK)
        self.SetBackgroundColour(wx.WHITE)
        

class TitledPage(wx.wizard.WizardPageSimple):
    """A standard wizard page with a title and label."""
    def __init__(self, parent, title, label):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.SetBackgroundColour(parent.bgcolor)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        if title:
            titleText = wx.StaticText(self, -1, title)
            titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            titleText.SetForegroundColour(wx.BLACK)
            self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        if label:
            self.AddSpace()
            label = wx.StaticText(self, -1, label)
            label.SetForegroundColour(wx.BLACK)
            self.sizer.Add(label)
            self.AddSpace()
    def AddSpace(self, n=1):
        self.sizer.Add(wx.StaticText(self, -1, "\n" * n))
