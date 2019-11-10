import wx
import wx.lib.iewin as iewin
class MyBrowser(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    ##super(MyBrowser,self).__init__(self,parent)
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.browser =  iewin.IEHtmlWindow(self)
    sizer.Add(self.browser, 1, wx.ALL|wx.EXPAND)
    self.SetSizer(sizer)
    x=wx.EXPAND
    self.SetSize(parent.Size)
    #sizer.Fit(parent)

   # self.SetSize((400,200))
  def load(self,uri):
      self.browser.Navigate(uri)
""""
if __name__ == '__main__':
  app = wx.App()
  dialog = MyBrowser(None, -1)
  dialog.browser.Navigate("https://www.youtube.com/embed/CpAcxbtXUgQ")
  dialog.Show()
  app.MainLoop()
  """
