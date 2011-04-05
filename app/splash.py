import wx
from wx.lib.agw.advancedsplash import AdvancedSplash
from retriever.app.splash_img import splash_img

class Splash(AdvancedSplash):
    def __init__(self, parent=None):
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN
        AdvancedSplash.__init__(self, parent, size=wx.DefaultSize, 
                                bitmap=splash_img.GetBitmap(), 
                                style=splashStyle)
        wx.GetApp().Yield()
