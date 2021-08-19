class EmotionVideoFrame:
    #Constructor
    def __init__(self,img,status,confidance,timeStamp=None):
        self._img=img,
        self._status=status,
        self._confidance=confidance,
        self._timeStamp=timeStamp        
    #get img
    @property
    def img(self):         
         return self._img
    #-----------------------------------------------
    #get status
    @property
    def status(self):         
         return self._status  
    #-----------------------------------------------     
    @property
    def confidance(self):         
         return self._confidance
    #-----------------------------------------------   
    @property
    def timeStamp(self):         
         return self._timeStamp
    #-----------------------------------------------   
         
    

#____________________________________________________________________________________________

class EmotionVideoFrame_B:
    #Constructor
    def __init__(self,status,confidance,timeStamp=None):
        
        self.status=status
        self.confidance=confidance
        self.timeStamp=timeStamp        
    
   
         