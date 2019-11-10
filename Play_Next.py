import threading

class PlayNextThread(threading.Thread):
    #The constructor of the class. Get the main frame of the software.

    def __init__(self,frame):
        super(PlayNextThread,self).__init__()

        #Attrubutes
        self.frame=frame
    #Function running when you start the process. The function actually runs the background and when finished video calling function is basically the main frame you move to the next video.
    def run(self):

        print "New Thread Started"
        print self.frame.playNext
        while True:
            print "im still here"
            while self.frame.playNext=="No":
                    pass
            print "Should i play the next track?"+self.frame.playNext
            #It means we should play the next track
            self.frame.Play_Next()


