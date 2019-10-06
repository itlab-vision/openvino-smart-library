import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer


det = face_recognizer.DNNFaceDetector("face-detection-retail-0004.bin",
                                           "face-detection-retail-0004.xml", 300, 300, 
                                           (127.5, 127.5, 127.5), False, 0.007843)
cap = cv.VideoCapture(0)
while(True): 
    _, f = cap.read()
    det.detect(f)
    cv.imshow("window", f)
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('q'):
        break
cap.release()