import cv2
import numpy as np
from skimage import measure
from Business.VideoPredication.VideoFrame import VideoFrame
simlarityThreshold=0.85
#-------------------------------------------
def extractVideoFrames(videofilepath):
    listVideoFrames=[]
    cam = cv2.VideoCapture(videofilepath)
    # Used as counter variable
    currentframe = 0
    while(True):
        # reading from frame
        ret,frame = cam.read()
        if ret:
            if(currentframe % 25==0):
                videoFrame=VideoFrame(currentframe,frame)
                videoFrame.timeStamp=cam.get(cv2.CAP_PROP_POS_MSEC)                
                listVideoFrames.append(videoFrame)
            currentframe += 1
        else:
            break
    print('TotalFramesCount=',currentframe)
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return listVideoFrames   
#-------------------------------------------
def calculatestructural_similarity_BetweentwoImages(image1,image2):  
    grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    resized_image1 = cv2.resize(grayimage1, (32, 32))
    resized_image2 = cv2.resize(grayimage2, (32, 32))
    resized_image1 = np.array(resized_image1)
    resized_image2 = np.array(resized_image2)
    # Count root mean square between both images (RMS)
    similarity=measure.compare_ssim(resized_image1, resized_image2)   
    return similarity    
#-------------------------------------------
def removeConsecutiveDuplicateFrames(listVideoFrames):
    listUniqueVideoFrames=[]
    previous_value = listVideoFrames[0]    
    for elem in listVideoFrames:
        ssimvalue=calculatestructural_similarity_BetweentwoImages(elem.frame,
                                                    previous_value.frame)
        if ssimvalue<simlarityThreshold:
            listUniqueVideoFrames.append(elem)
            previous_value = elem
    return listUniqueVideoFrames 

#-------------------------------------------
def getVideoFrames(videofilepath):
    listVideoFrames=extractVideoFrames(videofilepath)
    print('TotalFramesCount60ps=',len(listVideoFrames))
    listRemainingVideoFrames=removeConsecutiveDuplicateFrames(listVideoFrames)
    print('TotalFramesAfterRemoveConsecutiveDuplicate=',len(listRemainingVideoFrames))    
    return listRemainingVideoFrames
#-------------------------------------------