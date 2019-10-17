import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer

args = dict(name = 'DNNfd', model = "face-detection-retail-0004.bin" , 
                            config = "face-detection-retail-0004.xml",  
                            width = 672, height = 384, threshold = 0.9)
det = face_recognizer.FaceDetector.create(args)

cap = cv.VideoCapture(0)
while(True): 
    _, f = cap.read()
    faces = det.detect(f)
    for face in faces:
        cv.rectangle(f, face[0], face[1], color=(0, 255, 0))
    cv.imshow("window", f) #cv.transpose(f))
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('q'):
        break
cap.release()