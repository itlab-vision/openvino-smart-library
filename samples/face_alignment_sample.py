
import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer

refLandmarks = np.float32([[0.31556875000000000, 0.4615741071428571],  # left eye
                           [0.68262291666666670, 0.4615741071428571],  # right eye
                           [0.50026249999999990, 0.6405053571428571],  # tip of nose
                           [0.34947187500000004, 0.8246919642857142],  # left lip corner, right lip corner
                           [0.65343645833333330, 0.8246919642857142]])  # right lip corner

args = dict(name = 'DNNLandmarks', model = "landmarks-regression-retail-0009.bin",
            config = "landmarks-regression-retail-0009.xml", width = 48, height = 48)
fl = face_recognizer.FaceLandmarks.create(args)
args = dict(name = 'DNNfd', model = "face-detection-retail-0004.bin",
            config = "face-detection-retail-0004.xml", 
            width = 672, height = 384, threshold = 0.9)
det = face_recognizer.FaceDetector.create(args)

cap = cv.VideoCapture(0)
landmarks = []
while(True): 
    _, img = cap.read()
    faces = det.detect(img)
    alignFace = np.zeros(img.shape, np.uint8)
    for face in faces:
        roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
        landmarks = fl.findLandmarks(roi)
        alignFace = fl.align(roi, landmarks, refLandmarks)
    cv.imshow("window1", alignFace)
    cv.imshow("window2", img)
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('q'):
        break
cap.release()