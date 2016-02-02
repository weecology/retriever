import wx
from wx.lib.agw.advancedsplash import AdvancedSplash
from retriever.app.images import logo


class Splash(AdvancedSplash):

    def __init__(self, parent=None):
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.FRAME_SHAPED
        AdvancedSplash.__init__(self, parent, size=wx.DefaultSize,
                                bitmap=logo.GetBitmap(),
                                style=splashStyle)
        wx.GetApp().Yield()
