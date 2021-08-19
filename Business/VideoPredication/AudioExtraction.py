import moviepy.editor as mp

def extractAudio(VideoPath):
    my_clip = mp.VideoFileClip(VideoPath)
    my_clip.audio.write_audiofile(r"UPLOAD_FOLDER\Audio.mp3")
    return "UPLOAD_FOLDER\Audio.mp3"




