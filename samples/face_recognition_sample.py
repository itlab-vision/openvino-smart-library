import sys, os
import argparse 
import numpy as np
import cv2
sys.path.append("..\src\modules")
import face_recognizer


rec = face_recognizer.PVLRecognizer()
rec.Create("..\\src\\modules\\pvl\\build\\PVL_wrapper.dll")
cap = cv2.VideoCapture(0)
UID = -10000
name = "UNKNOWN"

while(True): 
    _, f = cap.read()
    (ID, (x, y, w, h)) = rec.Recognize(f)
    name = str(ID)
    cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
    cv2.imshow("web", f)
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('r'):
         tmp = rec.Register(f, 1)
    if ch & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()