import wx
import wx.html2
import Youtube_Preview
from Youtube_Preview import *
from apiclient import discovery
from oauth2client import client
import codecs
import threading


flow = client.flow_from_clientsecrets('client_secrets.json',
                   scope='https://www.googleapis.com/auth/youtube',
                   redirect_uri='urn:ietf:wg:oauth:2.0:oob')
auth_uri = flow.step1_get_authorize_url()

#auth_uri="https://accounts.google.com/b/0/IssuedAuthSubTokens"
auth_uri="https://accounts.google.com/Logout"
revokeUrl="https://accounts.google.com/o/oauth2/revoke?token="


class MyBrowser(wx.Dialog):
  def __init__(self,frame,*args, **kwds):
    wx.Dialog.__init__(self,frame,*args, **kwds)
    sizer = wx.BoxSizer(wx.VERTICAL)
    print "D"
    self.browser = wx.html2.WebView.New(self)
    sizer.Add(self.browser, 1, wx.EXPAND, 10)
    ##self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.browser)
    self.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.browser)
    ##self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.onWebViewNavigating, self.browser)

    self.SetSizer(sizer)
    self.SetSize((1024, 720))

  def onWebViewNavigating(self, evt):
    print "onWebViewNavigating"
    print evt.GetURL()



 ## def OnWebViewLoaded(self, evt):
   ## self.browser.RunScript('alert("OnWebViewLoaded");')
   ## print "OnWebViewLoaded"
 #Action is subdivision of Mybrowser which is activated when jumping event changed the title of the web page. When the page is actually moved to the graduating disengagement action closes the browser for the sake of security. Action gets the event as a parameter and treats it accordingly.

  def OnWebViewTitleChanged(self, evt):
    # The full document has loaded
    print "OnWebViewTitleChanged"
    print evt.GetString()
    print evt.GetString().split()[0]

    print evt.GetString().split()
    if len(evt.GetString().split())>2:
        if evt.GetString().split()[3]==unicode('Google'):
            #self.dialog.browser.LoadURL(revokeUrl)
            self.Destroy()




class DisconnectThread(threading.Thread):
    #The constructor of the class. Get the main frame of the program and building the browser will display the disengagement
    def __init__(self, frame):
        super(DisconnectThread,self).__init__()
        self.dialog=MyBrowser(frame,-1)
        print auth_uri
      ##  self.dialog.Show()
        self.dialog.Show()
        #Attributes
        self.frame=frame
    def run(self):
        self.dialog.browser.LoadURL(revokeUrl+self.frame.access_token)
        self.dialog.browser.LoadURL(auth_uri)
        self.frame.access_token="WAITING"
        self.frame.control2.DeleteAllItems()
        self.frame.control2_il.RemoveAll()





"""

app=wx.App()
dialog = MyBrowser(None, -1)
print "ok dude it fine"
print auth_uri
dialog.browser.LoadURL(auth_uri)
dialog.Show()
app.MainLoop()
"""
