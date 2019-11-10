import wx
import wx.html2
import Youtube_Preview
from apiclient import discovery
from oauth2client import client
# -*- coding: utf-8 -*-

import threading


flow = client.flow_from_clientsecrets('client_secrets.json',
                   scope='https://www.googleapis.com/auth/youtube',
                   redirect_uri='urn:ietf:wg:oauth:2.0:oob')
auth_uri = flow.step1_get_authorize_url()

#auth_uri="https://accounts.google.com/b/0/IssuedAuthSubTokens"
#auth_uri="https://accounts.google.com/Logout"


f=open('account.txt','rb')

class MyBrowser(wx.Dialog):
  def __init__(self,frame, *args, **kwds):
    wx.Dialog.__init__(self,frame, *args, **kwds)
    sizer = wx.BoxSizer(wx.VERTICAL)
    print "D"
    self.code=""
    self.frame=frame
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
##Action is subdivision of Mybrowser which is activated when jumping event changed the title of the web page. When the page is actually passed to the page where the code is confirming the action closes the browser for the sake of security. Action gets the event as a parameter and treats it accordingly.
  def OnWebViewTitleChanged(self, evt):
    # The full document has loaded
    print "OnWebViewTitleChanged"
    print evt.GetString()
    self.code=evt.GetString()
    if self.code[:13]=="Success code=":
       auth_code = self.code[13:]
       credentials = flow.step2_exchange(auth_code)
       self.frame.access_token=credentials.access_token
       print "Successfuly Connected"
       self.frame.connect_button.SetBitmap(self.frame.img2)
       self.frame.connect_button.Refresh()
       self.Destroy()
       finish=True
       LikesThread=Youtube_Preview.youtube_data_api.LikesThread(self.frame)
       playNext=Youtube_Preview.Play_Next.PlayNextThread(self.frame)
       LikesThread.start()
       playNext.start()


class LoginThread(threading.Thread):
    #The constructor of the class. Get the main frame of the program and building the browser will display the login

    def __init__(self, frame):
        super(LoginThread,self).__init__()
        self.dialog=MyBrowser(frame,-1)
        print auth_uri
        self.dialog.browser.LoadURL(auth_uri)
      ##  self.dialog.Show()
        self.dialog.Show()
        #Attributes
        self.frame=frame



"""

app=wx.App()
dialog = MyBrowser(None, -1)
print "ok dude it fine"
print auth_uri
dialog.browser.LoadURL(auth_uri)
dialog.Show()
app.MainLoop()
"""
