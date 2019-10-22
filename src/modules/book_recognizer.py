import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
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


class QRBookRecognizer(BookRecognizer):
    def create(self, detName):
        pass

    @staticmethod
    def recognize(frame):
        # Find barcodes and QR codes
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decodedObjects = pyzbar.decode(gray)

        # Print results
        ans = ""
        for obj in decodedObjects:
            if obj.type == 'QRCODE':
                ans = obj.data.decode('utf-8')

        # Return decode information
        return ans

    @staticmethod
    def display(frame):
        # Find objects
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decodedObjects = pyzbar.decode(gray)

        # Loop over all decoded objects
        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # Number of points in the convex hull
            n = len(hull)

            # Draw the convext hull
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        return frame
