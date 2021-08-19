import cv2
import re
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoFileClip
from Business.VideoPredication import VideoFramePredictor
from Business.VideoPredication.Video_Results import Video_Results

videoFileName='D:/Faculty/Graduation Project/VideoEmotionClassifier_V1/VideoEmotionClassifier/Face Test.mp4'

#_____________________________________________________
def Video_analisis(videoFileName):
    
    output=VideoFramePredictor.videoFramesPrediction(videoFileName)         
    cap = cv2.VideoCapture(videoFileName)
    word=''
    confidance=''
    img_array = []
    conf=''
    ori=''   
    # Capture frames in the video 
    print('Writing on video frames...............')
    while(True):
        ret, frame = cap.read()
        if ret:
            currenttimestamp=cap.get(cv2.CAP_PROP_POS_MSEC)/1000   
            matchedObj=[item for item in output if item.timeStamp/1000==currenttimestamp]   
            if len(matchedObj) >0 :
                    word="status: "+matchedObj[0].status
                    confidance=matchedObj[0].confidance
                    conf= "confidence: "+ str(round(confidance*100, 2))+"%"                             
                
            font = cv2.FONT_HERSHEY_TRIPLEX
            ori = cv2.rectangle(frame,(450,120), (20,20), (0,0,0), 4)
            cv2.putText(ori,  word,(60, 60), font, 1,(251, 186, 8), 1,cv2.LINE_4)
            cv2.putText(ori, conf, (60, 100 ),font, 1,(8, 186,251), 1,cv2.LINE_4)
            height, width, layers = frame.shape
            size = (width,height)               
            img_array.append(ori)           
        else:
            break
    # release the cap object
    cap.release()
    # close all windows
    cv2.destroyAllWindows()
        #cv2.imshow('video', ori)
      
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #         break
   
    print('Saving video.................')   
    out = cv2.VideoWriter('Application/demo.mp4',cv2.VideoWriter_fourcc(*'H264'),30, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release() 
    
    duration,duration_dict=video_calculations(videoFileName,output)
    video_Results=Video_Results('demo.mp4',duration,duration_dict,output)  
    variation_intime(output)
    return video_Results

#---------------------------------------------------   

def video_calculations(videoFileName,output):
    
    clip = VideoFileClip(videoFileName)
    duration= clip.duration
    duration_dict={}   
    previous=duration   
    for item in output[::-1]:
            if not item.status in duration_dict:
                duration_dict[item.status]=previous- (item.timeStamp/1000)
                previous=item.timeStamp/1000
            else:
                duration_dict[item.status]=duration_dict[item.status]+( previous- (item.timeStamp/1000))
                previous=item.timeStamp/1000
    return duration,duration_dict
#----------------------------------------------------------------------------------------- 


#-----------------------------------------------------------------------------------------
def variation_intime(output):
     # duration,duration_dict=video_calculations(videoFileName,output)
     classes={ 'disgust': 0,'angry': 1, 'fear': 2, 'sad': 3,'neutral': 4,'happy': 5, 'surprise': 6}        
     X=[]
     Y=[]
     for item in output:
       x=item.timeStamp/1000
       y=classes[item.status]
       print(y)
       X.append(x)
       Y.append(y)
  
     fig, ax = plt.subplots()
     fig.canvas.draw()
     ymin, ymax = plt.ylim()
     plt.ylim(0, 6)
     labels = [item.get_text() for item in ax.get_yticklabels()]
     labels[0] = 'Disgust'
     labels[1] = 'Angry'
     labels[2] = 'Fear'
     labels[3] = 'Sad'
     labels[4] = 'Neutral'
     labels[5] = 'Happy'
     labels[6] = 'Surprise'
     ax.set_yticklabels(labels)
     ax.plot(X, Y,color='green',  linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=8)    
    
     plt.savefig('Application/EmotionsWithTime.png')
     
     
     
    #  anger,sad,neutral,fear,disgust,happy,surprise=0,0,0,0,0,0,0
    #  if 'angry' in duration_dict:
    #     anger= round(((duration_dict['angry']/duration)*100),2)
    #  if 'sad' in duration_dict:
    #     sad= round(((duration_dict['sad']/duration)*100),2)
    #  if 'neutral' in duration_dict:
    #     neutral= round(((duration_dict['neutral']/duration)*100),2)
    #  if 'fear' in duration_dict:
    #     fear= round(((duration_dict['fear']/duration)*100),2)
    #  if 'disgust' in duration_dict:
    #     disgust= round(((duration_dict['disgust']/duration)*100),2)
    #  if 'happy' in duration_dict:
    #     happy= round(((duration_dict['happy']/duration)*100),2)
    #  if 'surprise' in duration_dict:
    #     surprise= round(((duration_dict['surprise']/duration)*100),2)
 	
  
    #  # defining labels
    #  status = ['Angry', 'Sad', 'Happy', 'Surprise','Neutral','Fear','Disgust']
      
    #  # portion covered by each label
    #  slices =[anger,sad,happy,surprise,neutral,fear,disgust]
      
    # # color for each label
    #  colors = ['#ff3333', '#3333ff', '#33ff33','#ffff33', '#ff9999', '#ff8000','#9933ff']
      
    #  from matplotlib import pyplot as plt
    #  plt.figure(figsize=(20,12))
    # # plotting the pie chart
    #  plt.pie(slices, labels = status, colors=colors, 
    #     startangle=90, shadow = True, explode = (0, 0, 0, 0,0,0,0),
    #     radius = 1.2, autopct = '%1.1f%%')   
    #  # plotting legend
    #  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      
    # # showing the plot
    #  #plt.show()
    #  plt.savefig('Application/EmotionsDurations.png')
     
         
    

