import wx

class TitledPage(wx.wizard.WizardPageSimple):
    """A standard wizard page with a title and label."""
    def __init__(self, parent, title, label):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        if title:
            titleText = wx.StaticText(self, -1, title)
            titleText.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
            self.sizer.Add(titleText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        if label:
            self.AddSpace()
            self.sizer.Add(wx.StaticText(self, -1, label))
            self.AddSpace()
    def AddSpace(self, n=1):
        for i in range(n):
            self.sizer.Add(wx.StaticText(self, -1, "\n"))
