import unittest
import sys
import cv2
import numpy as np
sys.path.append("..\src\modules")
import face_detection

class CommonTestCase(unittest.TestCase):
    
    def test(self):
        img = cv2.imread("..\samples\lena.png")
        face_cascade = face_detection.FaceDetector.CreateDetector('cascade')
        face_cascade.Init("C:\Intel\computer_vision_sdk_2018.3.343\opencv\etc\haarcascades\haarcascade_frontalface_alt.xml")
        rects = face_cascade.Detect(img)
        self.assertLessEqual(abs(rects.item(0)-213), 10) # x
        self.assertLessEqual(abs(rects.item(1)-205), 10) # y
        self.assertLessEqual(abs(rects.item(2)-175), 10) # w
        self.assertLessEqual(abs(rects.item(3)-175), 10) # h
        
        
if __name__ == '__main__':
    unittest.main()