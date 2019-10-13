
import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer


# args = dict(name = '', model = '' , config= '', witdth = 0, height = 0, threshold = 0.5)
args = dict(name = 'DNNLandmarks', model = "landmarks-regression-retail-0009.bin" , config = "landmarks-regression-retail-0009.xml", width = 48, height = 48)
fl = face_recognizer.FaceLandmarks.create(args)

args = dict(name = 'DNNfd', model = "face-detection-retail-0004.bin" , config = "face-detection-retail-0004.xml", width = 672, height = 384, threshold = 0.9)
det = face_recognizer.FaceDetector.create(args)

cap = cv.VideoCapture(0)
landmarks = []
while(True): 
    _, img = cap.read()
    faces = det.detect(img)
    for face in faces:
        # print(face[0][0])
        roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
        landmarks = fl.findLandmarks(roi)
        #print(landmarks)
        for point in landmarks[0:1]:
            y = int(point[1]*roi.shape[0])
            x = int(point[0]*roi.shape[1])
            cv.circle(roi, (x,y) , 15, (0,0,255), -1)

    cv.imshow("window", img)
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('q'):
        break
cap.release()