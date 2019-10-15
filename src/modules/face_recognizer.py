import numpy as np
import cv2 as cv
import ctypes as C

from abc import ABC, abstractmethod

class FaceRecognizer(ABC):
     @staticmethod
     def create(args): #Args - dict("name", "dll", "db")
        if args["name"] == 'DNN':
            return DNNRecognizer(args["model"], args["config"], 
                                 args["width"], args["height"], 
                                 args["threshold"])
        else:
            raise Exception('Error: wrong recognizer name')

     @abstractmethod
     def register(self, img, ID):
         """Register new reader"""

     @abstractmethod
     def recognize(self, img):
         """Recognize valid user"""

class FaceDetector(ABC):
     @staticmethod
     def create(args):
         if args["name"] == 'DNNfd':
            return DNNDetector(args["model"], args["config"], 
                               args["width"], args["height"], 
                               args["threshold"])
         else:
            raise Exception('Error: wrong detector name')

     @abstractmethod
     def detect(self, img,  threshold):
         """Detect faces on image"""

class FaceLandmarks(ABC):
    @staticmethod
    def create(args): #Args - dict("name", "dll", "db")
         if args["name"] == 'DNNLandmarks':
            return DNNLandmarks(args["model"], args["config"], 
                                args["width"], args["height"])
         else:
            raise Exception('Error: wrong detector name')

    @abstractmethod
    def align(self, img, l):
         """Detect faces on image"""

class DNNLandmarks(ABC):
    def __init__(self, modelPath, configPath, width, height):
        self.model = modelPath
        self.config = configPath
        self.width = width
        self.height = height
        backendId = cv.dnn.DNN_BACKEND_INFERENCE_ENGINE
        targetId = cv.dnn.DNN_TARGET_CPU
        self.net = cv.dnn.readNet(self.model, self.config)
        self.net.setPreferableBackend(backendId)
        self.net.setPreferableTarget(targetId)

    def findLandmarks(self, img):
        blob = cv.dnn.blobFromImage(img,  size=(self.width, self.height))
        self.net.setInput(blob)
        out = self.net.forward()
        out = out.flatten()
        landmarks = np.empty((5, 2), dtype=np.float32)
        for i in range(5):
            landmarks[i] = [out[2*i],out[2*i+1] ]

        return landmarks

    def align(self, img, landmarks, refLandmarks):
        aligned_face= np.copy(img)
        refLandmarksCopy =  np.copy(refLandmarks)
        for  point, refPoint in zip(landmarks, refLandmarksCopy):
           point[1] = int(point[1]*img.shape[0])
           point[0] = int(point[0]*img.shape[1])
           refPoint[1] = int(refPoint[1]*img.shape[0])
           refPoint[0] = int(refPoint[0]*img.shape[1])

        print(landmarks)
        print(landmarks[0:3,:])
        print(landmarks[0:5:2,:])

        l = np.empty((3, 2), dtype=np.float32)
        rl= np.empty((3, 2), dtype=np.float32)
        l[0] = landmarks[1]
        l[1] = landmarks[2]
        l[2] = landmarks[4]
        rl[0] = refLandmarksCopy[1]
        rl[1] = refLandmarksCopy[2]
        rl[2] = refLandmarksCopy[4]
        M = cv.getAffineTransform(l, rl)  # landmarks[0:5:2,:], refLandmarksCopy[0:3,:])
        aligned_face = cv.warpAffine(aligned_face, M, (aligned_face.shape[1], aligned_face.shape[0]))
        return aligned_face
       
class DNNDetector(FaceDetector):
    def __init__(self, modelPath, configPath, width, height, threshold):
        self.model = modelPath
        self.config = configPath
        self.width = width
        self.height = height
        self.threshold = threshold
        backendId = cv.dnn.DNN_BACKEND_INFERENCE_ENGINE
        targetId = cv.dnn.DNN_TARGET_CPU
        self.net = cv.dnn.readNet(self.model, self.config)
        self.net.setPreferableBackend(backendId)
        self.net.setPreferableTarget(targetId)

    def detect(self, img):
        blob = cv.dnn.blobFromImage(img,  size=(self.width, self.height))
        self.net.setInput(blob)
        out	= self.net.forward()
        faces = []
        for detection in out.reshape(-1, 7):
            confidence = float(detection[2])
            if confidence >  self.threshold:
                xmin = int(detection[3] *  img.shape[1])
                ymin = int(detection[4] *  img.shape[0])
                xmax = int(detection[5] *  img.shape[1])
                ymax = int(detection[6] *  img.shape[0])
                faces.append(((xmin, ymin), (xmax, ymax)))
        return faces

class DNNRecognizer(FaceRecognizer):
    def __init__(self, modelPath, configPath, width, height, threshold):
        args = dict(name = 'DNNLandmarks', model = "landmarks-regression-retail-0009.bin",
                    config = "landmarks-regression-retail-0009.xml",
                    width = 48, height = 48)
        self.fl = FaceLandmarks.create(args)
        args = dict(name = 'DNNfd', model = "face-detection-retail-0004.bin",
                    config = "face-detection-retail-0004.xml",
                    width = 672, height = 384, threshold = 0.9)
        self.det = FaceDetector.create(args)
        self.model = modelPath
        self.config = configPath
        self.width = width
        self.height = height
        self.threshold = threshold
        backendId = cv.dnn.DNN_BACKEND_INFERENCE_ENGINE
        targetId = cv.dnn.DNN_TARGET_CPU
        self.net = cv.dnn.readNet(self.model, self.config)
        self.net.setPreferableBackend(backendId)
        self.net.setPreferableTarget(targetId)


    def register(self, img, ID):
        faces = self.det.detect(img)
        for face in faces:
            roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
            landmarks = self.fl.findLandmarks(roi)
            pts1 = np.float32([ [landmarks[0][0], landmarks[0][1]], [landmarks[1][0], landmarks[1][1]] ,[landmarks[2][0], landmarks[2][1]] ])
            pts2 = np.float32([[0.31556875000000000, 0.4615741071428571], [0.68262291666666670, 0.4615741071428571], [0.50026249999999990, 0.6405053571428571]])
            alignFace = self.fl.align(roi, pts1, pts2)
        blob = cv.dnn.blobFromImage(alignFace,  size=(self.width, self.height))
        self.net.setInput(blob)
        out	= self.net.forward()
        out = out.flatten()
        return out

    def recognize(self, img):
        #TODO
        return True

