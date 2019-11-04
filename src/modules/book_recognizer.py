import cv2
import sys
import time
import numpy as np
from abc import ABC, abstractmethod


class BookRecognizer(ABC):
    @staticmethod
    def create(version, detName=1):
        if version == 2:
            return QRBookRecognizer()
        
    @abstractmethod
    def recognize(self, frame, tpls, coeff):
        """Recognize book"""
        

class Recognizer(BookRecognizer):
    
    def create(self, detName):
        detectors = {"ORB":1, "SIFT":2, "SURF":3}
        
        try:
            detectors[detName]
            
        except(KeyError):
            print("Wrong detector name")
            
        else:
            if (detName == "ORB"):
                self.det = cv2.ORB_create() 
            elif (detName == "SIFT"):
                self.det = cv2.xfeatures2d.SIFT_create()
            elif (detName == "SURF"):
                self.det = cv2.xfeatures2d.SURF_create()

            
    def recognize(self, frame, desTpls, coeff):
        arr = []
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, desFrame = self.det.detectAndCompute(frameGray, None)

        for t in desTpls:
            matcher = cv2.BFMatcher()
            matches = matcher.knnMatch(t, desFrame, k = 2)
            good = []
            
            for m,n in matches:
                if m.distance < n.distance * coeff: 
                    good.append(m)
                    
            arr.append(len(good))
        
        return arr


class QRBookRecognizer(BookRecognizer):
    # Constructor
    def __init__(self):
        self.qrDecoder = cv2.QRCodeDetector()
        self.box = 0

    def recognize(self, input_image, tpls=0, coeff=0) -> str:
        # Detect and decode the qrcode
        data, bbox, rectifiedImage = self.qrDecoder.detectAndDecode(input_image)
        if len(data) > 0:
            self.box = bbox
            return data
        else:
            return ""
