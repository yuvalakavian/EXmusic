__author__ = 'YuvalMetal'

from Browser import MyBrowser
from random import shuffle
import wx
import wx.media
import os
import urllib2
import urllib
import json
import threading
import tags
import youtube_data_api
import Play_Next
import Login_Flow
import Disconnect
import CEF
import player_skeleton2
from player_skeleton2 import *
from hachoir_metadata import metadata
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from os import walk
import urllib2
from bs4 import BeautifulSoup



API_KEY=open(os.getcwd()+"\\"+"api_key.txt",'r').read()
html="""
<!DOCTYPE html>
<html>
  <body>
    <!-- 1. The <iframe> (and video player) will replace this <div> tag. -->
    <div id="player" border=0></div>

    <script>
      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '610',
          width: '100%',
          videoId:'"""

html2="""',
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
            'onError':onPlayerError
          }
        });
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.playVideo();
        document.title="started"
      }
      function onPlayerError(event){
      if(event.data==150){
      document.title="ended"
      }
	  if(event.data==101){
	    document.title="ended"
	  }
	  }

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
      var done = false;
      function onPlayerStateChange(event) {
    //   if (event.data == YT.PlayerState.PLAYING && !done) {
      //    setTimeout(stopVideo, 6000);
        //  done = true;
        //}
		if (event.data==YT.PlayerState.ENDED){

		document.title="ended"
		}
      }
      function stopVideo() {
        player.stopVideo();
      }
    </script>
  </body>
</html>
     """





music_category_id="10"

class MyApp(wx.App):
    timer = None
    timerID = 1
    mainFrame = None
    def OnInit(self):
        if not CEF.USE_EVT_IDLE:
            print("[wxpython.py] Using TIMER to run CEF message loop")
            self.CreateTimer()

        self.frame = MyFrame(None, title="Youtube Preview")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    def CreateTimer(self):
        # See "Making a render loop":
        # http://wiki.wxwidgets.org/Making_a_render_loop
        # Another approach is to use EVT_IDLE in MainFrame,
        # see which one fits you better.
        self.timer = wx.Timer(self, self.timerID)
        self.timer.Start(10) # 10ms
        wx.EVT_TIMER(self, self.timerID, self.OnTimer)

    def OnTimer(self, event):
        CEF.cefpython.MessageLoopWork()

    def OnExit(self):
        # When app.MainLoop() returns, MessageLoopWork() should
        # not be called anymore.
        print("[wxpython.py] MyApp.OnExit")
        if not CEF.USE_EVT_IDLE:
            self.timer.Stop()


class MyFrame(CEF.MainFrame):
    ##The constructor of the class, who takes the father, the id, title, location, size, style and name. It should be noted that everyone boot from the start and the project is not sent to any action by the user parameters.

    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=(850,400),
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="MyFrame"):
        super(MyFrame, self).__init__(parent, title, pos, size, style, name)
        # Attributes
        self.d_index={}
        self.index=""
        self.d={}
        self.tags_d={}
        self.tags_arr=[]
        self.access_token="WAITING"
        self.dAlbums={}
        self.dCurrentAlbum={}
        self.d_Current_Album_Index={}
        self.Current_Album_Index=""
        self.dArtists={}






        file_path=os.getcwd()+"\\connect.PNG"
        print file_path
        img=wx.Image('connect.PNG',wx.BITMAP_TYPE_ANY)
        img=img.Scale(150,35)
        img=img.ConvertToBitmap()

        img2=wx.Image('disconnect.PNG',wx.BITMAP_TYPE_ANY)
        img2=img2.Scale(150,35)
        img2=img2.ConvertToBitmap()

        self.img=img
        self.img2=img2

        icon=wx.Image('EXmusicico.PNG',wx.BITMAP_TYPE_ANY)
        icon=icon.Scale(100,60)
        icon=icon.ConvertToBitmap()


        self.connect_button=wx.BitmapButton(self.panel,-1,img,size=(150,35),pos=(650,0))
        self.icon=wx.BitmapButton(self.panel,-1,icon,size=(100,60),pos=(0,0))

        self.btn1 = wx.Button(self.panel, id=1, label="SEARCH", pos =(435,65))
      #later  self.shuffle=wx.Button(self.panel,id=9,label="SHUFFLE",pos=(170,100))

       # self.static2 = wx.StaticText(self.panel,id=3, label="Videos List: ", pos=(0, 100))
     #   self.static3 = wx.StaticText(self.panel,id=4, label="Preview:", pos=(400, 100))
      #  self.static_tags= wx.StaticText(self.panel,id=3, label="Tags: ", pos=(40, 70))

        self.tags=wx.TextCtrl(self.panel,id=7,size=(400,25),style=wx.ALIGN_LEFT,pos=((0,65)))

        self.control2 = wx.ListCtrl(self.panel,id=6,size=(150,600),style=wx.LC_REPORT)

        self.control2.InsertColumn(1, "LIKED VIDEOS",width=wx.EXPAND)
        self.control2_il=wx.ImageList(120, 90)
        self.control2.SetImageList(self.control2_il,wx.IMAGE_LIST_SMALL)
        self.control2.Arrange()




        self.tags_list=wx.ListCtrl(self.panel,id=8,size=(150,600),style=wx.LC_REPORT
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        #self.tags_list.InsertColumn(0,"")
        self.tags_list.InsertColumn(0, "TAGS",width=wx.EXPAND)
        self.tags_il=wx.ImageList(120, 90)
        self.tags_list.SetImageList(self.tags_il,wx.IMAGE_LIST_SMALL)
        self.tags_list.Arrange()

        self.youtube_lyrics_ctrl=wx.TextCtrl(self.panel,size=(250,600),style=wx.LC_REPORT)
        self.youtube_lyrics_ctrl.SetValue("hello world")
        self.youtube_lyrics_ctrl.Hide()


        self.music_player_panel=wx.Panel(self,size=(1920,1080))
        self.music_player_panel.SetBackgroundColour(wx.WHITE)
        self.music_player_panel.Hide()

        img = wx.EmptyImage(400,400)
        self.image=wx.StaticBitmap(self.music_player_panel,id=8,size=(400,400))
        self.image.SetBitmap(wx.BitmapFromImage(img))
        #self.image.Hide()
        self.test_panel=wx.Panel(self.music_player_panel,size=(500,300))
        self.musicplayer=player_skeleton2.MediaPanel(self.test_panel,self)

        self.music_List=wx.ListCtrl(self.music_player_panel,id=10,size=(300,600),style=wx.LC_REPORT
                                #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        self.music_List.InsertColumn(0, "",width=wx.EXPAND)
        self.music_il=wx.ImageList(90, 90)
        self.music_List.SetImageList(self.music_il,wx.IMAGE_LIST_SMALL)

        self.song_list=wx.ListCtrl(self.music_player_panel,id=11,size=(300,600),style=wx.LC_REPORT
                                   #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        self.song_list.InsertColumn(0, "",width=wx.EXPAND)
        self.lyrics_ctrl=wx.TextCtrl(self.music_player_panel,size=(400,600),style=wx.LC_REPORT)
        self.lyrics_ctrl.SetValue("hello world")
        self.lyrics_ctrl.Hide()




        #self.song_il=wx.ImageList(90, 90)
        #self.song_list.SetImageList(self.music_il,wx.IMAGE_LIST_SMALL)








        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.btn1)
        self.Bind(wx.EVT_BUTTON,self.OnConnect,self.connect_button)
       # self.Bind(wx.EVT_BUTTON,self.OnShuffle,self.shuffle)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.control2)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.tags_list)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.music_List)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.song_list)
       # self.Bind(wx.media.EVT_MEDIA_LOADED, self.song_is_loaded)
        #self.Bind(wx.media.EVT_MEDIA_LOADED, self.song_is_loaded,self.musicplayer)






        panelSizer=wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(self.panel,1,wx.EXPAND)
        panelSizer.Add(self.music_player_panel,1,wx.EXPAND)
        self.SetSizer(panelSizer)



        topSizer=wx.BoxSizer(wx.VERTICAL)
        lineSizer=wx.BoxSizer(wx.HORIZONTAL)
        titleSizer=wx.BoxSizer(wx.HORIZONTAL)
        searchSizer=wx.BoxSizer(wx.HORIZONTAL)
        previewSizer=wx.BoxSizer(wx.HORIZONTAL)


        titleSizer.Add(self.icon,1,wx.HORIZONTAL|wx.ALIGN_LEFT)
        titleSizer.Add(wx.StaticText(self.panel),100,wx.HORIZONTAL|wx.ALIGN_CENTER)
        titleSizer.Add(self.connect_button,1,wx.HORIZONTAL|wx.ALIGN_RIGHT)

        searchSizer.Add(self.tags,7,wx.HORIZONTAL|wx.ALIGN_LEFT)
        searchSizer.Add(wx.StaticText(self.panel),1,wx.HORIZONTAL|wx.ALIGN_LEFT)
        searchSizer.Add(self.btn1,1,wx.HORIZONTAL|wx.ALIGN_LEFT)
        searchSizer.Add(wx.StaticText(self.panel),30,wx.HORIZONTAL|wx.ALIGN_RIGHT)

        previewSizer.Add(self.control2,3,wx.HORIZONTAL|wx.ALIGN_LEFT)
        previewSizer.Add(wx.StaticText(self.panel),0,wx.HORIZONTAL)
        previewSizer.Add(self.tags_list,3,wx.HORIZONTAL|wx.ALIGN_LEFT)
        previewSizer.Add(wx.StaticText(self.panel),0,wx.HORIZONTAL|wx.ALIGN_RIGHT)
        previewSizer.Add(self.mainPanel,10,wx.HORIZONTAL|wx.ALIGN_RIGHT)
        previewSizer.Add(self.youtube_lyrics_ctrl,3,wx.ALIGN_RIGHT)






        topSizer.Add(titleSizer,0,wx.ALL|wx.EXPAND)
        topSizer.Add(searchSizer,0,wx.ALL|wx.EXPAND)
        topSizer.Add(previewSizer,0,wx.ALL|wx.EXPAND)
        #topSizer.Add(self.youtube_lyrics_ctrl,0,wx.ALIGN_RIGHT)


        self.panel.SetSizer(topSizer)

        topSizer2=wx.BoxSizer(wx.HORIZONTAL)
        ImageSizer=wx.BoxSizer(wx.HORIZONTAL)
        mpSizer=wx.BoxSizer(wx.VERTICAL)

        mpSizer.Add(self.image,2,wx.ALIGN_LEFT|wx.ALIGN_TOP)
        mpSizer.Add(self.test_panel,2,wx.ALIGN_TOP|wx.ALIGN_LEFT)

        ImageSizer.Add(mpSizer,1,wx.HORIZONTAL|wx.ALIGN_LEFT)
        ImageSizer.Add(self.music_List,0,wx.ALIGN_TOP|wx.ALIGN_LEFT)
        ImageSizer.Add(self.song_list,0,wx.ALIGN_TOP|wx.ALIGN_LEFT)
        ImageSizer.Add(self.lyrics_ctrl,0,wx.ALIGN_TOP|wx.ALIGN_LEFT)




        topSizer2.Add(ImageSizer,0,wx.ALL|wx.EXPAND)
       # topSizer2.Add(mpSizer,0,wx.ALL|wx.EXPAND)

        self.music_player_panel.SetSizer(topSizer2)

        self.music_player_panel.Refresh()
        self.music_player_panel.Layout()
        self.musicplayer.SetInitialSize()

        try:
            jsonFile= open("Jsonfile.json",'r')
            print "ok"
            self.dAlbums=json.load(jsonFile)
            loadAlbums=threading.Thread(target=self.Create_Albums_List,args=(self.dAlbums,))
            loadAlbums.start()
        except:
            print "No Local Json File Created Yet!!!!!!!!!!!!!1"








    """

    def song_is_loaded(self,e):
            this function gets called when the EVT_MEDIA_LOADED is created
            , then  it plays the song that gets loaded.

            self.musicplayer.mediaPlayer.Play()
            print 'evt loaded'
    """
    """
    def OnShuffle(self,event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        print "Button Clicked:"
        print "ID=%d" % event_id
        print "object=%s" % event_obj.GetLabel()
        self.tags_list.DeleteAllItems()
        shuffle(self.tags_arr)
        print self.tags_arr
        for i in xrange(len(self.tags_arr)):
            self.tags_list.InsertStringItem(i,self.tags_arr[i])
    """
    ##This actually perform the search on what the user typed. Action receives the event and in accordance care of him.
    def OnButtonClick(self, event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        print "Button Clicked:"
        print "ID=%d" % event_id
        print "object=%s" % event_obj.GetLabel()

        self.tags_list.DeleteAllItems()
        self.tags_d={}
        self.tags_arr=[]
        self.tags_il.RemoveAll()


        tags_list=self.tags.GetValue()
        tags_list=tags_list.split(",")
        print tags_list
        # Non-Blocking mode
        task2=tags.TagsThread(self,tags_list)

        task2.start()
    ##This action actually make the connect / disconnect YouTube account. Action receives the event and in accordance care of him.

    def OnConnect(self,event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        print "Button Clicked:"
        print "ID=%d" % event_id

        if self.connect_button.Bitmap==self.img2:
            self.OnDisconnect()
            self.connect_button.SetBitmap(self.img)


        else:
           # self.connect_button.Destroy()

            self.control2.DeleteAllItems()
            self.d={}


            # Non-Blocking mode

            login_task=Login_Flow.LoginThread(self)
           # task1=youtube_data_api.LikesThread(self)
           # playNext=Play_Next.PlayNextThread(self)

            login_task.start()
            login_task.join()

            #task1.start()
            #playNext.start()




#Dragged action of OnConnect that actually operate the disengagement process.
    def OnDisconnect(self):
        disconnect_task=Disconnect.DisconnectThread(self)
        disconnect_task.start()

#This occurs when the user selects a video from the list Hliikim or search results. In addition, when the user selects a new album or a new song be heard. All different choice has different treatment accordingly. The function receives the event and according attends
    def OnSelect(self,event):
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        print "Video Is Previewed:"
        print "ID=%d" % event_id



        print self.d
        print self.tags_d
        if event_id==6:
            videoName=event.GetText()
            videoid=self.d[videoName][0]
            self.index=self.d[videoName][1]
            self.LoadIt(videoid)
            loadLyrics=threading.Thread(target=self.LoadLyrics,args=(videoName,"Youtube Panel",))
            loadLyrics.start()
            self.youtube_lyrics_ctrl.SetValue("Searching For Lyrics..")
            self.youtube_lyrics_ctrl.Show()
            self.SetSize((1920,1080))

        if event_id==8:
            print "D"
            videoName=event.GetText()
            self.browser.Navigate("https://www.youtube.com/embed/"+self.tags_d[videoName]+"?autoplay=true")
            loadLyrics=threading.Thread(target=self.LoadLyrics,args=(videoName,"Youtube Panel",))
            loadLyrics.start()
            self.youtube_lyrics_ctrl.SetValue("Searching For Lyrics..")
            self.youtube_lyrics_ctrl.Show()
            self.SetSize((1920,1080))

        if event_id==10:
            self.song_list.DeleteAllItems()
            self.dCurrentAlbum={}
            self.LoadAlbum(event)
            self.lyrics_ctrl.Hide()

        if event_id==11:
           self.LoadSongViaEvent(event)
           self.lyrics_ctrl.SetValue("Searching For Lyrics..")
           self.lyrics_ctrl.Show()
           self.SetSize((1450,600))

    #Operation loads the next song by event and by autoplay that background. The intention is where the song will play at the event and received by the playlist of the album. The function receives the event and in accordance care of him. The intention is to send it to LoadSong which action triggers the local song.
    def LoadSongViaEvent(self,event):
        try:
            self.song_list.SetItemBackgroundColour(self.Current_Album_Index,wx.WHITE)
        except:
            print "first song selected"
        songName=event.GetText()
        self.Current_Album_Index=self.dCurrentAlbum[songName][1]
        print self.Current_Album_Index
        self.song_list.SetItemBackgroundColour(self.Current_Album_Index,"#778899")
        self.song_list.Select(self.Current_Album_Index,on=0)
        self.LoadSong(songName)
    #Action which claims the song, getting the song to be applied.
    def LoadSong(self,songName):
        songDir=self.dCurrentAlbum[songName][0]
        print songDir
        self.musicplayer.loadMusic(songDir)
        songArtist=self.GetSongArtist(songDir)
        name=songArtist+" "+songName
        #self.LoadLyrics(name,"Music Panel")
        loadLyrics=threading.Thread(target=self.LoadLyrics,args=(name,"Music Panel",))
        loadLyrics.start()

        """
        btnInfo = self.musicplayer.playPauseBtn
        evt = wx.PyCommandEvent(wx.EVT_BUTTON,btnInfo)
        wx.PostEvent(btnInfo, evt)

        """

   ##Function claims for any song or video in accordance with its address and displays them on the screen. The function gets the name of the song and it lyrics that will be at the panel. (YouTube or local songs)

    def LoadLyrics(self,name,panel):
        try:
            print ((name))
            str = name
            #str = unicode(str, errors='replace')
            print "ok"
            name = str.encode('utf8')


            #audiofile = eyed3.load((name))
            print('Test')
            #name= name.replace('.mp3','')
            print('Applying to '+name)
            name = name +' lyrics'
            name  = name.replace(' ','+')

            url = 'http://www.google.com/search?q='+name

            req = urllib2.Request(url, headers={'User-Agent' : "foobar"})

            response = urllib2.urlopen(req)
            str = response.read()
            str = unicode(str, errors='replace')

            #print(str.encode('utf8'))

            result = str.encode('utf8')

            link_start=result.find('http://www.metrolyrics.com')
            link_end=result.find('html',link_start+1)
            #print(result[link_start:link_start+57])


            link = result[link_start:link_end+4]

            lyrics_html = urllib2.urlopen(link).read()
            soup = BeautifulSoup(lyrics_html)
            raw_lyrics= (soup.findAll('p', attrs={'class' : 'verse'}))
            paras=[]
            test1=unicode.join(u'\n',map(unicode,raw_lyrics))

            test1= (test1.replace('<p class="verse">','\n'))
            test1= (test1.replace('<br/>',' '))
            test1 = test1.replace('</p>',' ')
            print (test1)
            print test1.split()
            if test1.split()==[]:
               if panel=="Music Panel":
                 self.lyrics_ctrl.SetValue("No Lyrics Found")
               elif panel=="Youtube Panel":
                 print "YOUTUBE LYRICS"
                 self.youtube_lyrics_ctrl.SetValue("No Lyrics Found")
            elif panel=="Music Panel":
               self.lyrics_ctrl.SetValue(test1+"\r\n Powered By MetroLyrics")
            elif panel=="Youtube Panel":
               print "YOUTUBE LYRICS"
               self.youtube_lyrics_ctrl.SetValue(test1+"\r\n Powered By MetroLyrics")
            # audiofile.tag.lyrics.set(u''+test1 )
            #audiofile.tag.save()
            #print('lyrics Added! ')
        except:
            print ('An error occured for '+name)
            if panel=="Music Panel":
              self.lyrics_ctrl.SetValue("No Lyrics Found")
            elif panel=="Youtube Panel":
              print "YOUTUBE LYRICS"
              self.youtube_lyrics_ctrl.SetValue("No Lyrics Found")


  #The function returns the name of the artist by extracting metadata from the song received as a parameter. The function gets the name of the song and treats it accordingly.

    def GetSongArtist(self,songDir):
        parser = createParser(songDir)
        print parser

        meta=""

        # See what keys you can extract
        for k,v in metadata.extractMetadata(parser)._Metadata__data.iteritems():

            if v.values:
                print v.key, v.values[0].value
                if v.key=="author":
                    return v.values[0].value


   #The function loads the selected album named event is created by selecting the album. The function receives the event and handles it accordingly.

    def LoadAlbum(self,event):
        key=event.GetText()
        print key
        arr=self.dAlbums[key]
        #img=self.Get_Album_Img(self.dAlbums,key)
        i=0
        for song in arr:
         #   index=self.song_il.Add(img)
          #  print self.song_il.GetImageCount
            songName=self.GetSongName(song)
            self.dCurrentAlbum[songName]=[song,i]
            self.song_list.InsertStringItem(i,songName,i)
            self.d_Current_Album_Index[i]=songName
            print self.d_Current_Album_Index
            i=i+1
#The function returns the song name by retrieving metadata from the song received as a parameter. The function gets the name of the song and treats it accordingly.

    def GetSongName(self,songDir):
        parser = createParser(songDir)
        print parser

        meta=""

        # See what keys you can extract
        for k,v in metadata.extractMetadata(parser)._Metadata__data.iteritems():

            if v.values:
                print v.key, v.values[0].value
                if v.key=="title":
                    return v.values[0].value
#The function loads the requested video. The function gets the ID of the video and treats it accordingly

    def LoadIt(self,videoid):
            self.Create_Html(videoid)
         #   self.browser.Navigate("https://www.youtube.com/embed/"+self.d[event.GetText()][0]+"?autoplay=true")
            self.browser.Navigate(os.getcwd()+"\\"+"test.html")
#Function basically a chain of HTML code with the resulting video ID parameter and writes the output to an HTML file to be run later and displayed on the screen. The function gets the ID of the video and treats it accordingly.

    def Create_Html(self,videoid):
        newHtml=html+videoid+html2
        if os.path.exists(os.getcwd()+"\\"+"test.html"):
           os.remove(os.getcwd()+"\\"+"test.html")
        f=open("test.html",'w')
        f.write(newHtml)
#Operates the following video in the likes playlist

    def Play_Next(self):
        print self.index
        print self.d_index[self.index]
        videoid=self.d[self.d_index[self.index+1]][0]
        print( videoid)
        self.control2.Select(self.index,on=0)
        self.index=self.index+1
        self.control2.Select(self.index)
        self.LoadIt(videoid)
        print "Status: ",CEF.MainFrame.playNext
        CEF.MainFrame.playNext="No"
        print "Status: ",self.playNext
#The function starts the next song in the album selected from local songs

    def Play_Next_Song(self):
        try:
            nextSongName=self.d_Current_Album_Index[self.Current_Album_Index+1]
            self.song_list.Select(self.Current_Album_Index,on=0)
            self.song_list.SetItemBackgroundColour(self.Current_Album_Index,wx.WHITE)
            self.Current_Album_Index=self.Current_Album_Index+1
            self.song_list.SetItemBackgroundColour(self.Current_Album_Index,"#778899")
            self.song_list.Select(self.Current_Album_Index,on=0)
            print nextSongName
            self.LoadSong(nextSongName)
        except:
            print "Last song in album"

#The function starts the previous song in the album selected from local songs

    def Play_Prev_Song(self):
        try:
            prevSongName=self.d_Current_Album_Index[self.Current_Album_Index-1]
            self.song_list.Select(self.Current_Album_Index,on=0)
            self.song_list.SetItemBackgroundColour(self.Current_Album_Index,wx.WHITE)
            self.Current_Album_Index=self.Current_Album_Index-1
            self.song_list.SetItemBackgroundColour(self.Current_Album_Index,"#778899")
            self.song_list.Select(self.Current_Album_Index,on=0)
            print prevSongName
            self.LoadSong(prevSongName)
        except:
            print "First song in album"

#The function displays the image on when you play the song. The function receives as parameter the link to the location the image to be there and treats it accordingly.
    def OnMusicPlay(self,filepath):
        print filepath
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        img=img.Scale(400,400)
        self.image.SetBitmap(wx.BitmapFromImage(img))
        #self.mainPanel.Hide()
        #self.control2.Hide()
        #self.tags_list.Hide()
        self.image.Show()
#The function receives the folder location where the songs are local and sorts them in albums according to their metadata, and maintains all json file so that the next entrance screening will be ready. The function gets the path as a parameter and treats it accordingly

    def Create_Albums(self,path):
        print path
        print "Sucess!!"
        mypath=path
        self.music_List.DeleteAllItems()
        self.music_il.RemoveAll()
        dAlbums={}
        dArtists={}
        f = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            for i in filenames:
                f.append(dirpath+"\\"+i)
                filename=dirpath+"\\"+i
                #filename, realname = unicodeFilename(filename), filename
                if filename[-3:]=="mp3":
                    parser = createParser(filename)
                    print parser

                    meta=""

                    # See what keys you can extract
                    for k,v in metadata.extractMetadata(parser)._Metadata__data.iteritems():

                        if v.values:
                            print v.key, v.values[0].value
                            if v.key=="album":
                                if not (dAlbums.has_key(v.values[0].value)):
                                    dAlbums[v.values[0].value]=[]
                                dAlbums[v.values[0].value].append(filename)
                                #meta=meta+str(v.key)+":"+str(v.values[0].value)+"\n"
                            """
                            if v.key=="author":
                                if not (dArtists.has_key(v.values[0].value)):
                                    dArtists[v.values[0].value]=[]
                                dArtists[v.values[0].value].append(filename)
                            """


        print dAlbums
        #print dArtists
        self.dAlbums=dAlbums
        #self.dArtists=dArtists
        jsonarray1 = json.dumps(dAlbums)
        #jsonarray2 = json.dumps(dArtists)

        f=open("Jsonfile.json",'wb')
        f.write(jsonarray1)
        #f.write(jsonarray2)
        self.Create_Albums_List(dAlbums)
        self.music_player_panel.Refresh()
        self.music_player_panel.Layout()


#The function returns the desired album art. The function receives as a parameter the dictionary albums and a key which is actually a song from the album, so that the image be repaid is actually a picture of one of the songs.
    def Get_Album_Img(self,dAlbums,dkey):
        print dAlbums[dkey]
        musicFile=dAlbums[dkey][0]
        print musicFile
        musicFile=str(musicFile)
        file = File(musicFile) # mutagen can automatically detect format and type of tags
        try:
                artwork = file.tags['APIC:'].data # access APIC frame and grab the image
               # return artwork
                filepath=os.getcwd()+'\check.jpg'
                with open(filepath, 'wb') as img:
                    img.write(artwork) # write artwork to new image
                print "this is the filepath",filepath
                image = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                image=image.Scale(90,90)
                image=image.ConvertToBitmap()
                return image
               # self.frame.OnMusicPlay(filepath)
        except:
                print "no album art"
                filepath='noalbumart.jpg'
                image = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                image=image.Scale(90,90)
                image=image.ConvertToBitmap()
                return image
#The function creates a list of albums in the GUI software. The function gets the dictionary albums parameter and treats it accordingly.
    def Create_Albums_List(self,dAlbums):
        i=0
        for key in dAlbums:
            print key
            img=self.Get_Album_Img(dAlbums,key)
            index=self.music_il.Add(img)
            print self.music_il.GetImageCount
            self.music_List.InsertImageStringItem(i,key,i)
            i=i+1










#The function adds the values list Hliikim include the name of the video and the video image. The function receives the index, the name and the video image as a parameter and treats them in accordance with

    def Insert_List(self,i,title,img):
        index=self.control2_il.Add(img)
        print self.control2_il.GetImageCount
        print i,index
        wx.CallAfter(self.control2.InsertImageStringItem, i, title,i)
#The function adds entries to the dictionary that contains information about each video in the list Hliikim. The function receives as a parameter the name of the video, its identity, and its index.
    def Insert_DIC(self,title,videoid,i):
        self.d[title]=[videoid,i]
#The function adds the values of the indexes dictionary Hliikim list. The function receives the index and the name of the video and treats them accordingly.

    def Insert_DIC_Index(self,i,title):
        self.d_index[i]=title
#The function adds the values in the list of search results that include the name of the video and the video image. The function receives the index, the name and the video image as a parameter and treats them in accordance with

    def Insert_Tags(self, i, title,img):
        index=self.tags_il.Add(img)
        print self.tags_il.GetImageCount
        print i,index
        #wx.CallAfter(self.tags_list.InsertImageItem,0,i)
        wx.CallAfter(self.tags_list.InsertImageStringItem, i, title, i)
#The function adds entries to the dictionary that contains information about each video in the list of search results. The function receives as a parameter the name of the video, and his identity and treats them accordingly.

    def Insert_Tags_DIC(self,title, videoid):
        self.tags_d[title]=videoid

   ## def Insert_Tags_List(self,title):
     ##   self.tags_arr.append(title)




        """
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = "Artist"
        self.tags_list.InsertColumnInfo(0, info)

        info.m_text = "Title"
        self.tags_list.InsertColumnInfo(1, info)


        # ListCtrl data generation
        items = self.tags_d.items()
        print "THIS IS NOT"
        print items
        for key, data in items:
            imglist_idx = imglistdict[key]
            index = self.tags_list.InsertImageStringItem(key, data[0], imglist_idx)
            self.tags_list.SetStringItem(index, 1, data[1])
            self.tags_list.SetItemData(index, key)
        """











if __name__ == "__main__":
    CEF.init_CEF()



    app = MyApp(False)
    app.MainLoop()


    # Let wx.App destructor do the cleanup before calling
    # cefpython.Shutdown(). This is to ensure reliable CEF shutdown.
    del app

    CEF.cefpython.Shutdown()
