#-------------------------------------------
#import libraries
import cv2 as cv
import numpy as np
import base64
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from Business.ImagePredication import imagePredictor
from Business.ImagePredication import FaceDetection
from Business.VideoPredication import VideoFramesExtractor
from Business.VideoPredication.VideoFrame import VideoFrame
from Business.VideoPredication.EmotionVideoFrame import EmotionVideoFrame_B
#-------------------------------------------
#ImagesEmojiDcitionary={'angry': '😠', 'disgust': '😖', 'fear': '😱', 'happy': '😁', 'neutral': '🙂', 'sad': '😩', 'surprise': '😲'}  
classes={'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surpris': 6}        
# load json and create model
json_file = open('Business/ImagePredication/Files/model_64.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#loaded_model._make_predict_function() 
# load weights into new model
loaded_model.load_weights("Business/ImagePredication/Files/model_64.h5")
# dimensions of our images
img_width, img_height = 48 ,48

#-------------------------------------------
def preProcessImage(imageFileName,croppedbox):
    x1=croppedbox[0]
    y1=croppedbox[1]
    x2=croppedbox[2]
    y2=croppedbox[3]     
    img = cv.imread(imageFileName)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    crop_img = gray[y1:y2, x1:x2]    
    width=48 
    height=48
    dim = (width, height)
    resizedimg= cv.resize(crop_img, dim, interpolation = cv.INTER_AREA)   
    return resizedimg
#-----------------------------------------------
# prediction function
def predicting_image(face_image):   
        #loaded_model.summary()        
        # load the image                 
        # load image as as grayscale
        #img = load_img(face_image,target_size=(img_width, img_height), color_mode = "grayscale")
        # convert image to a numpy array
        img_array = img_to_array(face_image)
        new_image_data =img_array.reshape((1, img_width, img_height, 1)).astype(np.float32)  
        emotion_classes = loaded_model.predict(new_image_data)
        #print("emotion_classes",emotion_classes[0])
        a = np.array(emotion_classes)
        idx = np.argmax(a)
        emotion=''
        print('idx',idx)
        for value, key in classes.items():           
            if key == idx:
                print(value)
                emotion=value
                break       
        return emotion,idx
 #-----------------------------------------------     
def framePrediction (videoFrame):
        directory='UPLOAD_FOLDER'       
        img = directory + '/' +'frame' + str(videoFrame.index) + '.jpg'
        cv.imwrite(img, videoFrame.frame)
        imgContent=''     
        with open(img, "rb") as image_file:            
            imgContent = base64.b64encode(image_file.read())
            imgContent = imgContent.decode('utf-8')          
        emotion=None     
        boxes,image=FaceDetection.DetectFaces(img)        
        if len(boxes)==0 :
            return None
            #emotion=EmotionVideoFrame(imgContent,"No Face detected")            
        else:            
            processedimg=imagePredictor.preProcessImage(img,boxes[0])            
            emotion_status,confidance=imagePredictor.predicting_image(processedimg)  
            #emoji=ImagesEmojiDcitionary[emotion_status]
            #emotion_status=emotion_status +" " + emoji
            emotion=EmotionVideoFrame_B(emotion_status,confidance,videoFrame.timeStamp)
        return emotion     
 #-----------------------------------------------  
def videoFramesPrediction(videofilepath):
   lstemotionVideoFrames=[]
   print("extract video frames")
   lstVideoFrames=VideoFramesExtractor.getVideoFrames(videofilepath)
   for videoframe in lstVideoFrames:
       emotionVideoFrame=framePrediction(videoframe) 
       if emotionVideoFrame==None: continue
       lstemotionVideoFrames.append(emotionVideoFrame)
   return lstemotionVideoFrames       
 #-----------------------------------------------    

    
      
   
    
    
    
    
    
    
    
    
    
    
    
    
    