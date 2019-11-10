import threading
import Youtube_Preview
from Youtube_Preview import *
import StringIO

API_KEY=open(os.getcwd()+"\\"+"api_key.txt",'r').read()





class LikesThread(threading.Thread):
    #The constructor of the class, gets the main frame as a parameter.
    def __init__(self, frame):
        super(LikesThread,self).__init__()

        #Attributes
        self.frame=frame
       # self.access_token=access_token
    #Function running when you start the process
    def run(self):
        while self.frame.access_token=="WAITING":
            pass
        self.youtube_recent_likes(self.frame.access_token)

        print "process finished likes"

    #The function checks the type of video category and returns it (the music is desired). The function gets the ID of the video and treats accordingly

    def check_categoryid(self,videoid):
        ##music category id is 10
        #url='https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Csnippet&id='+videoid+'&key='+API_KEY
        url='https://www.googleapis.com/youtube/v3/videos?'
        parameters={'part':'snippet,contentDetails','id':videoid,'key':API_KEY}
        url=url+urllib.urlencode(parameters)
        print url

        response=urllib2.urlopen(url)
        response=json.load(response)
        return response['items'][0]['snippet']['categoryId']
    #The function accepts the access token as a parameter and returns the identity of a user's Hliikim list.

    def GetLikesID(self,access_token):
        url='https://www.googleapis.com/youtube/v3/channels?'
        parameters={'part':'contentDetails','mine':'True','access_token':access_token,'key':API_KEY}
        url=url+urllib.urlencode(parameters)

        print url
        response=urllib2.urlopen(url)
        response=json.load(response)
        return response['items'][0]['contentDetails']['relatedPlaylists']['likes']
    #The function accepts the access token, and actually processes the information received from Hliikim of the user. Music videos the function adds to the list Hliikim in the main GUI.
    def youtube_recent_likes(self,access_token):
        ##"UC-lHJZR3Gqxm24_Vd_AJ5Yw"
        ##"UCiYupIhygoYZtwzkoSAgEOA"
        likes_playlist_id=self.GetLikesID(access_token)

        url='https://www.googleapis.com/youtube/v3/playlistItems?'
        parameters={'part':'snippet,contentDetails','playlistId':likes_playlist_id,'access_token':access_token,'key':API_KEY}
        url=url+urllib.urlencode(parameters)
        print url
       ## url='https://www.googleapis.com/youtube/v3/activities?part=contentDetails%2Csnippet&channelId='+channel_id+'&key='+API_KEY'
        response=urllib2.urlopen(url)
        videos=json.load(response)
        print len(videos['items'])
        print(videos['items'])
        i=0
        for video in videos['items']:


            videoid=video['contentDetails']['videoId']
            ##title=title.encode('utf-8').decode('latin_1')
            ##videoid=videoid.encode('utf-8').decode('latin_1')
            if(self.check_categoryid(videoid).encode('utf-8').decode('latin_1')==Youtube_Preview.music_category_id):
                title=video['snippet']['title']
                itemImageUrl=video['snippet']['thumbnails']['default']['url']

                buf = urllib2.urlopen(itemImageUrl).read()
                sbuf = StringIO.StringIO(buf)
                img = wx.ImageFromStream(sbuf).ConvertToBitmap()


                self.frame.Insert_DIC(title,videoid,i)
                self.frame.Insert_List(i,title,img)
                self.frame.Insert_DIC_Index(i,title)
                i=i+1
        try:
            pagetoken=videos['nextPageToken']
        except:
            pagetoken=None
        while pagetoken is not None and len(self.frame.d)<20:
            ##url='https://www.googleapis.com/youtube/v3/activities?pageToken='+pagetoken+'&part=contentDetails%2Csnippet&channelId='+channel_id+'&key='+API_KEY
            url='https://www.googleapis.com/youtube/v3/playlistItems?'
            parameters={'part':'snippet,contentDetails','playlistId':likes_playlist_id,'pageToken':pagetoken,'access_token':access_token,'key':API_KEY}
            url=url+urllib.urlencode(parameters)
            print url
            response=urllib2.urlopen(url)
            videos=json.load(response)
            for video in videos['items']:
                videoid=video['contentDetails']['videoId']
                ##title=title.encode('utf-8').decode('latin_1')
                ##videoid=videoid.encode('utf-8').decode('latin_1')
                if(self.check_categoryid(videoid).encode('utf-8').decode('latin_1')==Youtube_Preview.music_category_id):
                    title=video['snippet']['title']
                    itemImageUrl=video['snippet']['thumbnails']['default']['url']

                    buf = urllib2.urlopen(itemImageUrl).read()
                    sbuf = StringIO.StringIO(buf)
                    img = wx.ImageFromStream(sbuf).ConvertToBitmap()


                    self.frame.Insert_DIC(title,videoid,i)
                    self.frame.Insert_List(i,title,img)
                    self.frame.Insert_DIC_Index(i,title)
                    i=i+1
            try:
                pagetoken=videos['nextPageToken']
            except:
                pagetoken=None

        if len(self.frame.d)==0:
           dlg = wx.MessageDialog(None, 'Plesae go to this url to manage your youtube account and alow the public likes playlist:\nhttps://www.youtube.com/account_privacy', 'Order',
                                     wx.POPUP_WINDOW | wx.ICON_ERROR)
           if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()






