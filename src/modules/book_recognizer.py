import numpy as np
import cv2
from abc import ABC, abstractmethod

class BookRecognizer(ABC):
    @abstractmethod
    def Create(self, det_name):
        """Create recognizer"""
        
    @abstractmethod
    def Recognize(self, frame, tpls, coeff, min_count):
        """Recognize book"""
        
    @abstractmethod
    def Draw(self, frame, tpl, res):
        """Draw frame"""
        
class Recognizer(BookRecognizer):
    
    def Create(self, det_name):
         if (det_name == "ORB"):
             self.det = cv2.ORB_create() 
         elif (det_name == "SIFT"):
             self.det = cv2.xfeatures2d.SIFT_create()
         elif (det_name == "SURF"):
             self.det = cv2.xfeatures2d.SURF_create()
         else:
             print("Wrong detector name")
            
    def Recognize(self, frame, tpls, coeff, min_count):
        max_num_kp = 0
        for t in tpls:
            tpl = cv2.imread(t)
            matcher = cv2.BFMatcher()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
            kp_frame, des_frame = self.det.detectAndCompute(frame_gray, None)
            kp_tpl, des_tpl = self.det.detectAndCompute(tpl_gray, None)
            matches = matcher.knnMatch(des_tpl, des_frame, k = 2)
            good = []
            for m,n in matches:
                if m.distance < n.distance * coeff: 
                    good.append(m)
                    res = [good, kp_frame, kp_tpl]      
            print(len(res[0]),"совпадения",t)
            if len(res[0]) > max_num_kp:
                max_num_kp = len(res[0])
                good_res = res
                good_id = t
                good_tpl = tpl
                
        if max_num_kp > min_count:
            return [good_id, good_tpl, good_res]
   
        else:
            return [-1, 0, 0]
    
    def Draw(self, frame, tpl, res):
        good = res[0]
        kp_frame = res[1]
        kp_tpl = res[2]
        src_pts = np.float32([ kp_tpl[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp_frame[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, _ = cv2.findHomography( src_pts, dst_pts, cv2.RANSAC , 5.0 ) # матрица преобразования координат точек
        h, w, _ = tpl.shape # размеры шаблона
        pts = np.asarray( [ [0,0], [0,h - 1], [w - 1,h - 1], [w - 1,0] ],
                         dtype=np.float32).reshape(-1,1,2)
        dst = cv2.perspectiveTransform( pts, M )
        dst = [np.int32(np.abs(dst))]
        img_res = cv2.polylines(frame, dst, True, (0,255,255), 2, cv2.LINE_AA )
        return img_res
