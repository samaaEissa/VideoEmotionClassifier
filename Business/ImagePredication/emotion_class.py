class Emotion:
    #Constructor
    def __init__(self,img,status):
        self._img=img,
        self._status=status      
        
   #get img
    @property
    def img(self):         
         return self._img
    #-----------------------------------------------
    @img.setter 
    def img(self, img):
         self._img = img 
     #-----------------------------------------------   
 
    #get status
    @property
    def status(self):         
         return self._status
    #-----------------------------------------------
    @status.setter 
    def status(self, status):
         self._status = status 
     #----------------------------------------------- 
        
  
   
    
    

