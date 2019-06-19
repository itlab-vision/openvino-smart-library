import sys, os
import argparse 
#import numpy as np
import cv2
sys.path.append("..\\src\\modules")
import face_recognizer

class fpsMeasure:
     fpsInterval = 0
     fpsSum = 0
     fps = 0
def build_argparse():
    parser = argparse.ArgumentParser(description='face recognizer sample')
    parser.add_argument('-r', '--recognizer', type = str, default = 'PVL',
                        dest = 'recognizer', help = 'type of recognizer')
    parser.add_argument('-d', '--dll', type = str, default = 'PVL_wrapper.dll',
                        dest = 'dll', help = 'dll')
    parser.add_argument('-i', '--image', type = str,
                        dest = 'image', help = 'image')
    parser.add_argument('-v', '--video', type = str,
                        dest = 'video', help = 'video')
    parser.add_argument('-w', '--webcam', type = int, default = 0, 
                        dest = 'webcam', help = 'webcam')
    parser.add_argument('-m', '--model', type = str, default = 'defaultdb.xml' ,
                        dest = 'model', help = 'data base with faces')
    args = parser.parse_args()
    return args

def showText(f, x, y, h, w, name, elapsed = 0):
     cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
     cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (219, 132, 58), 2)
     cv2.putText(f, "Press Q to exit" , (10,40), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
     cv2.putText(f, "Press R to register." , (10,20), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)

     FPS_MEASURE_INTERVAL = 30
    #  fpsMeasure.fpsInterval = 0
    #  fpsMeasure.fpsSum = 0
    #  fpsMeasure.fps = 0
     fpsMeasure.fpsSum += elapsed
     fpsMeasure.fpsInterval = fpsMeasure.fpsInterval + 1
     print(fpsMeasure.fpsInterval)
     if (fpsMeasure.fpsInterval == FPS_MEASURE_INTERVAL):
          fpsMeasure.fps = 1.0 / fpsMeasure.fpsSum * FPS_MEASURE_INTERVAL
          fpsMeasure.fpsInterval = 0
          fpsMeasure.fpsSum = 0
     
     string = "fps:" + "{0:.3f}".format(fpsMeasure.fps)
     cv2.putText(f, string,(10,60), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
      
def show(src, uID,):
    cap = cv2.VideoCapture(src)
    fCount =  cap.get(cv2.CAP_PROP_FRAME_COUNT)
    currCount = 0
    name = "UNKNOWN"
    hold = 1
    startTick = cv2.getTickCount()
    while(True): 
        _, f = cap.read()
        (ID, (x, y, w, h)) = rec.recognize(f)
        currCount += 1
        if fCount != -1.0 and  fCount == currCount:
          currCount = 0 
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        name = str(ID)
        if ID == uID:
          name = "UNKNOWN"
        elapsed = float(cv2.getTickCount() - startTick) / cv2.getTickFrequency()
        startTick = cv2.getTickCount()
        showText(f,x,y,h,w,name, elapsed)
        cv2.imshow(str(src), f)
        ch = cv2.waitKey(hold)
        if ch & 0xFF == ord('r') and ID == uID:
             tmp = rec.register(f, rec.getNewID())
        if ch & 0xFF == ord('q'):
          break
    cap.release()
    
recArgs = dict(name = '', dll = '' , db= '')
args = build_argparse()

if (args.recognizer != None):
  recArgs['name'] = args.recognizer
  if (args.dll != None):
    recArgs['dll'] = args.dll
  if (args.model != None):
    recArgs['db'] = args.model
  rec = face_recognizer.FaceRecognizer.create(recArgs)
  uID = rec.getUID()
  
  if (args.image != None):
      img = cv2.imread(args.image)
      height, width, layers = img.shape
      size = (width,height)
      vName = 'tmp.avi'
      out = cv2.VideoWriter(vName,cv2.VideoWriter_fourcc(*'XVID'), 1.0, size)
      for i in range(2):
         out.write(img)
      out.release()
      show(vName, uID)
      os.remove('tmp.avi')
      
  elif (args.video != None):
      show(args.video,uID)
      
  elif (args.webcam != None):
      show(args.webcam ,uID)
    
    
cv2.destroyAllWindows()
