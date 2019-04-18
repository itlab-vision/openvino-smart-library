import cv2
from abc import ABC, abstractmethod

class BookRecognizer(ABC):
    @abstractmethod
    def create(self, detName):
        """Create recognizer"""
        
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