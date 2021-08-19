import cv2
#-------------------------------------------
haar_cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#-------------------------------------------

def DetectFaces(imag):    
    boxes = []
    #Loading the image to be tested
    test_image = cv2.imread(imag)
    #Converting to grayscale
    test_image_gray = cv2.cvtColor(test_image,cv2.COLOR_BGR2GRAY)
    #detect faces
    faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
    for (x,y,w,h) in faces_rects:
        cv2.rectangle(test_image, (x, y), (x+w, y+h), (0, 0, 0), 1)
        boxes.append([x, y, x+w, y+h])
    return boxes,test_image