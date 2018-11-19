import sys, os
sys.path.append("..\src\modules") 
import numpy as np
import cv2
import face_detection

cap = cv2.VideoCapture(0)
face_cascade = face_detection.HaarFaceDetector('haarcascade_frontalface_alt.xml')

faces = []

while(True): 
    ret, frame = cap.read()
    rects = face_cascade.Detect(frame)
    frame = face_cascade.Draw(frame, rects)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
