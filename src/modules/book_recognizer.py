import cv2
from abc import ABC, abstractmethod

class BookRecognizer(ABC):
    @abstractmethod
    def Create(self, det_name):
        """Create recognizer"""
        
    @abstractmethod
    def Recognize(self, frame, tpls, coeff):
        """Recognize book"""
        

class Recognizer(BookRecognizer):
    
    def Create(self, det_name):
        detectors = {"ORB":1, "SIFT":2, "SURF":3}
        
        try:
            detectors[det_name]
            
        except(KeyError):
            print("Wrong detector name")
            
        else:
            if (det_name == "ORB"):
                self.det = cv2.ORB_create() 
            elif (det_name == "SIFT"):
                self.det = cv2.xfeatures2d.SIFT_create()
            elif (det_name == "SURF"):
                self.det = cv2.xfeatures2d.SURF_create()

            
    def Recognize(self, frame, tpls, coeff):
        arr = []
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp_frame, des_frame = self.det.detectAndCompute(frame_gray, None)

        for t in tpls:
            tpl = cv2.imread(t)
            matcher = cv2.BFMatcher()
            tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
            
            kp_tpl, des_tpl = self.det.detectAndCompute(tpl_gray, None)
        
            matches = matcher.knnMatch(des_tpl, des_frame, k = 2)
            good = []
            
            for m,n in matches:
                if m.distance < n.distance * coeff: 
                    good.append(m)
                    
            arr.append(len(good))
        
        return arr