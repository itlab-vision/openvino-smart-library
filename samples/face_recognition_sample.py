import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer

args = dict(name = 'DNN', model = "face-reidentification-retail-0095.bin", 
            config = "face-reidentification-retail-0095.xml", 
            width = 128, height = 128, threshold = 0.5)
rec = face_recognizer.FaceRecognizer.create(args)

cap = cv.VideoCapture(0)
while(True): 
    _, f = cap.read()
    cv.imshow("window", f)
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('r'):
      out = rec.register(f, 1)
      print(out)
    if ch & 0xFF == ord('q'):
        break
cap.release()