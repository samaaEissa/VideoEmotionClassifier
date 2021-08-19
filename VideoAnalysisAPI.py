#-------------------------------------------
#import libraries
import os
from Business.VideoPredication import VideoFramePredictor
from Business.ImagePredication import imagePredictor
#-------------------------------------------
#API liberaries
from flask import Flask,request
from flask_cors import CORS
import jsonpickle
app = Flask(__name__)
CORS(app)
#-------------------------------------------
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#-----------------------------------------------
@app.route('/getEmotionFromVideo_facialExpression', methods=["POST"])
def getEmotionFromVideo():    
    videoFile = request.files['file']
    print("saving video file")
    videoFile.save(videoFile.filename)    
    print("predict video emotions")   
    output=VideoFramePredictor.videoFramesPrediction(videoFile.filename)    
    json_string=jsonpickle.encode(output,unpicklable=False)   
    response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json' )
    #delete temp files
    files = os.listdir('UPLOAD_FOLDER')
    for file in files:
        file=UPLOAD_FOLDER+'/' +file
        os.remove(file)
    return response

#-----------------------------------------------
#-----------------------------------------------
#routing API function        
@app.route('/getEmotionFromImage', methods=["POST"])
def getEmotionFromImage():
    Results=[]   
    
    files =request.files.getlist("image")
    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))   
    images = os.listdir('UPLOAD_FOLDER')
    for img in images:
        img=UPLOAD_FOLDER+'/' + img        
        emotion=imagePredictor.singleImagePreddiction(img)
        Results.append(emotion)
       
    json_string=jsonpickle.encode(Results,unpicklable=False) 
    #delete temp files
    for file in images:
        file=UPLOAD_FOLDER+'/' +file
        os.remove(file)
    response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json' )
    return response

#-----------------------------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=False, threaded=False)
    
