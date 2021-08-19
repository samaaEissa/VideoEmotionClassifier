import os
from Business.VideoPredication import opencvWriteOnVideo
from DataAccess import DBconnection
#from Business.VideoPredication.Video_Results import Video_Results
#-------------------------------------------
#API liberaries
from flask import Flask,request,send_from_directory
from flask_cors import CORS
import jsonpickle
app = Flask(__name__)
CORS(app)
#-------------------------------------------
UPLOAD_FOLDER = 'UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#-----------------------------------------------
@app.route('/getAnalysedVideo', methods=["POST"])
def getEmotionFromVideo():    
    videoFile = request.files['file']
    print("saving video file")
    videoFile.save(videoFile.filename)    
    print("predict video emotions")   
    video_Results=opencvWriteOnVideo.Video_analisis(videoFile.filename)
    video_Results.FilePath= video_Results.FilePath
    json_string=jsonpickle.encode(video_Results,unpicklable=False)   
    response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json' )
    #delete temp files
    files = os.listdir('UPLOAD_FOLDER')
    for file in files:
        if '.mp4' in file : continue
        file=UPLOAD_FOLDER+'/' +file
        os.remove(file)
    return response

#-----------------------------------------------

@app.route('/Register', methods=["POST"])
def Register():   
    json_data =request.json
    name=json_data['name']
    email=json_data['email']
    password=json_data['password']
    DBconnection.Registeration(name,password,email)    
    response = app.response_class(
        response="OK",
        status=200,
        mimetype='application/json' )   
    return response

#-----------------------------------------------    
@app.route('/Login', methods=["POST"])
def login():    
    json_data =request.json
    email=json_data['email']
    password=json_data['password']
    DBconnection.login(email,password)    
    response = app.response_class(
        response="OK",
        status=200,
        mimetype='application/json' )   
    return response

#-----------------------------------------------    

# @app.route("/UPLOAD_FOLDER/<path:path>")
# def get_file(path):
#     """Download a file."""
#     return send_from_directory('', path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=False, threaded=False)