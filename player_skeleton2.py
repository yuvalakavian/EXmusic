#----------------------------------------------------------------------
# player_skeleton2.py
#
# Created: 04/15/2010
#
# Author: Mike Driscoll - mike@pythonlibrary.org
#----------------------------------------------------------------------

import os
import wx
import wx.media
import wx.lib.buttons as buttons

from mutagen import File
import threading
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

########################################################################
class MediaPanel(wx.Panel):
    """"""
    #The constructor of the class. Get the panel of local music and the main frame parameters.
    #----------------------------------------------------------------------
    def __init__(self, parent,frameparent):
        """Constructor"""
        #wx.Panel.__init__(self, parent=parent,frameparent=frameparent)
        super(MediaPanel, self).__init__(parent)
        self.frame = frameparent
        self.currentVolume = 50
        self.createMenu()
        self.layoutControls()
        
        sp = wx.StandardPaths.Get()
        self.currentFolder = sp.GetDocumentsDir()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
    #----------------------------------------------------------------------
    def layoutControls(self):
        """
        Create and layout the widgets
        """
        
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self,szBackend=wx.media.MEDIABACKEND_WMP10) #wx.SIMPLE_BORDER
        except NotImplementedError:
            self.Destroy()
            raise
                
        # create playback slider
        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        self.Bind(wx.EVT_SLIDER, self.onSeek, self.playbackSlider)
        
        self.volumeCtrl = wx.Slider(self, style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.volumeCtrl.SetRange(0, 100)
        self.volumeCtrl.SetValue(self.currentVolume)
        self.volumeCtrl.Bind(wx.EVT_SLIDER, self.onSetVolume)
                
        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioSizer = self.buildAudioBar()
                
        # layout widgets
        mainSizer.Add(self.playbackSlider, 1, wx.ALL|wx.EXPAND, 5)
        hSizer.Add(audioSizer, 0, wx.ALL|wx.CENTER, 5)
        hSizer.Add(self.volumeCtrl, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
        
        self.SetSizer(mainSizer)
        self.Layout()
    #Action builds the player buttons
    #----------------------------------------------------------------------
    def buildAudioBar(self):
        """
        Builds the audio bar controls
        """
        audioBarSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.buildBtn({'bitmap':'player_prev.png', 'handler':self.onPrev,
                       'name':'prev'},
                      audioBarSizer)
        
        # create play/pause toggle button
        img = wx.Bitmap(os.path.join(bitmapDir, "player_play.png"))
        self.playPauseBtn = buttons.GenBitmapToggleButton(self, bitmap=img, name="play")
        self.playPauseBtn.Enable(False)

        img = wx.Bitmap(os.path.join(bitmapDir, "player_pause.png"))
        self.playPauseBtn.SetBitmapSelected(img)
        self.playPauseBtn.SetInitialSize()
        
        self.playPauseBtn.Bind(wx.EVT_BUTTON, self.onPlay)

        self.Bind(wx.media.EVT_MEDIA_LOADED, self.song_is_loaded)
        self.Bind(wx.media.EVT_MEDIA_FINISHED, self.onSongFinished)
        audioBarSizer.Add(self.playPauseBtn, 0, wx.LEFT, 3)
        
        btnData = [{'bitmap':'player_stop.png',
                    'handler':self.onStop, 'name':'stop'},
                    {'bitmap':'player_next.png',
                     'handler':self.onNext, 'name':'next'}]
        for btn in btnData:
            self.buildBtn(btn, audioBarSizer)
            
        return audioBarSizer
                    
    #----------------------------------------------------------------------
    def buildBtn(self, btnDict, sizer):
        """"""
        bmp = btnDict['bitmap']
        handler = btnDict['handler']
                
        img = wx.Bitmap(os.path.join(bitmapDir, bmp))
        btn = buttons.GenBitmapButton(self, bitmap=img, name=btnDict['name'])
        btn.SetInitialSize()
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.LEFT, 3)
    #Action creates the software's menu
    #----------------------------------------------------------------------
    def createMenu(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        panelMenu=wx.Menu()
        open_file_menu_item = fileMenu.Append(wx.NewId(), "&Open", "Open a File")
        change_panel=panelMenu.Append(wx.NewId(),"&Youtube Panel","Change To Youtube")
        change_panel2=panelMenu.Append(wx.NewId(),"&Music Panel","Change To Music")
        menubar.Append(fileMenu, '&File')
        menubar.Append(panelMenu,'&Panel')
        self.frame.SetMenuBar(menubar)
        self.frame.Bind(wx.EVT_MENU, self.onBrowse, open_file_menu_item)
        self.frame.Bind(wx.EVT_MENU, self.onChangeToYoutube, change_panel)
        self.frame.Bind(wx.EVT_MENU, self.onChangeToMusic, change_panel2)
        self.frame.Bind(wx.media.EVT_MEDIA_LOADED, self.song_is_loaded)

    #The function loads the song from the address that received as a parameter. The function receives as a parameter the location of the song and treats it accordingly.
    #----------------------------------------------------------------------
    def loadMusic(self, musicFile):
        """"""
        if not self.mediaPlayer.Load(musicFile):
            wx.MessageBox("Unable to load %s: Unsupported format?" % musicFile,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            print musicFile

            print "Exporting artwork!!"
            this="\\"
            that="\\\\"
            musicFile.replace(this,that)
            print( musicFile)
            musicFile=str(musicFile)
            file = File(musicFile) # mutagen can automatically detect format and type of tags
            print dirName
            try:
                artwork = file.tags['APIC:'].data # access APIC frame and grab the image
                filepath=dirName+'\check.jpg'
                with open(filepath, 'wb') as img:
                    img.write(artwork) # write artwork to new image


            except:
                print "no album art"
                filepath="noalbumart.jpg"

            self.frame.OnMusicPlay(filepath)

            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            self.playPauseBtn.Enable(True)
    #The function is called when an event occurs which the song is loaded successfully. The function starts the song. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def song_is_loaded(self,e):
        """this function gets called when the EVT_MEDIA_LOADED is created
        , then  it plays the song that gets loaded.
        """
        self.playPauseBtn.SetToggle(True)
        self.mediaPlayer.Play()
        self.mediaPlayer.SetInitialSize()
        self.GetSizer().Layout()
        self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
        print 'evt loaded'
    #The function is called when an event occurs which the song is over. The function starts the next song on the album. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onSongFinished(self,event):
        print "WORKS"
        self.frame.Play_Next_Song()
    #The function is called when the event deaf clicking on the folder selection button. The function for the user opens the dialogue window in which he will choose the folder and then she will call a function that sorts the albums main frame.
    #----------------------------------------------------------------------
    def onBrowse(self, event):
        """
        Opens file dialog to browse for music
        """
        wildcard = "MP3 (*.mp3)|*.mp3|"     \
                   "WAV (*.wav)|*.wav"
        dlg = wx.DirDialog(
            self, message="Choose a folder",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.currentFolder = os.path.dirname(path)

            cAlbums=threading.Thread(target=self.frame.Create_Albums, args=(path,))
            cAlbums.start()
        dlg.Destroy()
    #The function is activated when the user chose to pass the Panel YouTube. The function replaces the panel to the panel you want. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onChangeToYoutube(self,event):
        self.frame.music_player_panel.Hide()
        self.frame.panel.Show()
    #The function is activated when the user choose to switch to a panel of music. The function replaces the panel to the panel you want. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onChangeToMusic(self,event):
        self.frame.panel.Hide()
        self.frame.music_player_panel.Show()
        self.frame.music_player_panel.SetSizer
    #The function is activated when the user presses a button indicating transition to the next song, and transfers Tune in to the next song. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onNext(self, event):
        self.frame.Play_Next_Song()
    #The function is activated when the user click on a button that indicates stopping song, and the song pauses. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onPause(self):
        """
        Pauses the music
        """
        self.mediaPlayer.Pause()
    #The function is activated when the user click on a button that indicates playing a song, and starts the song. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onPlay(self, event):
        """
        Plays the music
        """
        if not event.GetIsDown():
          self.onPause()
          return
        
        if not self.mediaPlayer.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            
        event.Skip()
    #The function is activated when the user click on a button that indicates beyond previous song, and transfers the Tune In to the previous song. The function receives as a parameter to the event, and treats him accordingly.
    #----------------------------------------------------------------------
    def onPrev(self, event):
        self.frame.Play_Prev_Song()
    #The function adjusts the part of the song is heard by the part moved the carriage. The function receives as a parameter in the event that moved at the carriage and treats it accordingly.
    #----------------------------------------------------------------------
    def onSeek(self, event):
        """
        Seeks the media file according to the amount the slider has
        been adjusted.
        """
        offset = self.playbackSlider.GetValue()
        self.mediaPlayer.Seek(offset)
    #The function determines the volume of the player depending on the level selected. The function receives the event marks the modified level and handles it accordingly.
    #----------------------------------------------------------------------
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        self.currentVolume = self.volumeCtrl.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        self.mediaPlayer.SetVolume(self.currentVolume)
    #The function stops the music and initializes the play button. The function receives as a parameter to the event means that the stop button is pressed and treats it accordingly.
    #----------------------------------------------------------------------
    def onStop(self, event):
        """
        Stops the music and resets the play button
        """
        self.mediaPlayer.Stop()
        self.playPauseBtn.SetToggle(False)
        
    #----------------------------------------------------------------------
    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        offset = self.mediaPlayer.Tell()
        self.playbackSlider.SetValue(offset)

########################################################################
class MediaFrame(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Python Music Player")
        panel = MediaPanel(self)
        
#----------------------------------------------------------------------
# Run the program
"""
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()
"""
