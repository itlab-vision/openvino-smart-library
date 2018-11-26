# pydoc argparse
import sys, os
import argparse 
import numpy as np
import cv2
sys.path.append("..\src\modules")
import face_detection


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type = str, dest = 'model_path', action = 'store', help = 'HAAR or LBP')
parser.add_argument('-i', '--image', type = str, dest = 'image_path', action = 'store', help = 'Path to image')
parser.add_argument('-v', '--video', action='store_true', dest = 'isWebCam', help = 'Webcam')
args = parser.parse_args()

face_cascade = face_detection.FaceDetector.CreateDetector('cascade')

if (args.model_path != None):
   detectName = args.model_path
   if not face_cascade.Init(detectName):
      raise ValueError

if (args.image_path != None):
    img = cv2.imread(args.image_path)
    rects = face_cascade.Detect(img)
    img = face_cascade.Draw(img, rects)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    if(args.isWebCam == True):
       cap = cv2.VideoCapture(0)
       while(True): 
            ret, frame = cap.read()
            rects = face_cascade.Detect(frame)
            frame = face_cascade.Draw(frame, rects)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
       cap.release()
       cv2.destroyAllWindows()
