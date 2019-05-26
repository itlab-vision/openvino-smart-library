import sys, os
import argparse 
#import numpy as np
import cv2
sys.path.append("..\\src\\modules")
import face_recognizer

def build_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recognizer', type = str, default = "PVL",
                        dest = 'recognize', help = 'type of recognizer')
    parser.add_argument('-d', '--dll', type = str, default = "PVL_wrapper.dll",
                        dest = 'dll', help = 'dll')
    parser.add_argument('-i', '--im_dir', type = str,
                        dest = 'image', help = 'image')
    parser.add_argument('-v', '--video', type = str,
                        dest = 'video', help = 'video')
    parser.add_argument('-w', '--wbcam', type = int, default = 0, 
                        dest = 'webcam', help = 'webcam')
    parser.add_argument('-m', '--model', type = str, default = "defaultdb.xml" ,
                        dest = 'model', help = 'data base with faces')
    args = parser.parse_args()
    return args

def showText(f, x, y, h, w, name):
     cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
     cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (219, 132, 58), 2)
     cv2.putText(f, "Press Q to exit" , (10,40), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
     cv2.putText(f, "Press R to register." , (10,20), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
def show(src, uID):
    cap = cv2.VideoCapture(src)
    fCount =  cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    currCount = 0
    name = "UNKNOWN"
    hold = 1
    while(True): 
        _, f = cap.read()
        currCount += 1
        if fCount != -1.0 and  fCount == currCount - 1:
          currCount = 0 #Or whatever as long as it is the same as next line
          cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
        (ID, (x, y, w, h)) = rec.Recognize(f)
        name = str(ID)
        showText(f,x,y,h,w,name)
        cv2.imshow(src, f)
        ch = cv2.waitKey(hold)
        if ch & 0xFF == ord('r') and ID != uID:
             tmp = rec.Register(f, rec.GetNewID())
        if ch & 0xFF == ord('q'):
          break
    cap.release()
    
recArgs = dict(name = frName, dll = dllPath , db= dbPath)
args = build_argparse()

if (args.recognizer != None):
  recArgs["name"] = args.recognizer
  if (args.dll != None):
    recArgs["dll"] = args.dll
  if (args.model != None):
    recArgs["db"] = args.model
  rec = face_recognizer.FaceRecognizer.create(recArgs)
  uID = rec.GetUID()
  if (args.w != None):
      
  elif (args.video != None):
      
  elif (args.image != None):
      
    
    
cv2.destroyAllWindows()
