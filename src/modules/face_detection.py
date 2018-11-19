import numpy as np
import cv2
from abc import ABCMeta, abstractmethod, abstractproperty

class FaceDetector():
     __metaclass__=ABCMeta
     
     @staticmethod
     def CreateDetector(name):
        try:
           assert(name == 'cascade')
           if name == 'cascade':
               cascade = HaarFaceDetector()
               return cascade
        except AssertionError:
            print("Wrong name")
       
     @abstractmethod
     def __init__(self,name):
        """Constructor"""
        
     @abstractmethod
     def Detect(self, frame, objects, scores):
        """Detect face on frame"""
        
     def Draw(self, frame, rects):
         for (x,y,w,h) in rects:
             cv2.rectangle(frame, (x,y), (x+w,y+h),(255,0,0), 2)
         return frame

class HaarFaceDetector(FaceDetector):
    hdetector = cv2.CascadeClassifier()
    
    def __init__(self, name):
           self.model_file_path = name
           self.hdetector.load(name)
            
    def Detect(self, frame):
        if self.hdetector.empty():
            return -1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects  = self.hdetector.detectMultiScale(frame, 
                                                scaleFactor = 1.2,
                                                minNeighbors = 3,
                                                minSize=(30, 30))
        return rects
