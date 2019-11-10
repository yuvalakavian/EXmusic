import threading
import StringIO
from Youtube_Preview import *
API_KEY=open(os.getcwd()+"\\"+"api_key.txt",'r').read()
class TagsThread(threading.Thread):
    #The constructor of the class. Get the main frame of the software and the tags to search for entries on YouTube.

    def __init__(self, frame,tags):
        super(TagsThread,self).__init__()

        #Attributes
        self.frame=frame
        self.tags=tags
        self.index=0

        BMP_SIZE = 24
        self.tsize = (BMP_SIZE, BMP_SIZE)
        self.il = wx.ImageList(BMP_SIZE, BMP_SIZE)

        self.bmpdict={}
        # mapping wxImageList indices to keys in test_list_data
        self.imglistdict={}



    #Function running when you start the process. The function calls for each artist search function that creates the relevancy to the search results
    def run(self):
        for tag in self.tags:
            self.create_playlist(tag)
        print "process finished"

    def Create_Q(self,tag):
        tag=tag.split()
        print tag
        q=tag[0]
        for word in xrange(1,len(tag)):
            q=q+"+"+tag[word]
        print q
        return q
    #The search function receives the desired and for creating the list of search results additions to the list of results in the GUI program.
    def create_playlist(self,tag):
        url='https://www.googleapis.com/youtube/v3/search?'
        parameters={'part':'snippet','maxResults':'10','q':tag,'type':'video','videoSyndicated':'true','videoCategoryId':'10','key':API_KEY}
        url=url+urllib.urlencode(parameters)
        print url



        response=urllib2.urlopen(url)

        videos=json.load(response)
        print len(videos['items'])
        for video in videos['items']:
                title=video['snippet']['title']
                videoid=video['id']['videoId']
                itemImageUrl=video['snippet']['thumbnails']['default']['url']
                print itemImageUrl

                buf = urllib2.urlopen(itemImageUrl).read()
                sbuf = StringIO.StringIO(buf)
                img = wx.ImageFromStream(sbuf).ConvertToBitmap()
                #img.SetSize((50,50))



                self.bmpdict[self.index+1]=img
                self.imglistdict[self.index+1]=self.il.Add(img)


                ##title=title.encode('utf-8').decode('latin_1')
                ##videoid=videoid.encode('utf-8').decode('latin_1')

                self.frame.Insert_Tags_DIC(title,videoid)
                self.frame.Insert_Tags(self.index,title,img)
                self.index=self.index+1

      #  self.frame.Insert_IMG_LIST(self.il,self.imglistdict)




