import numpy as np
import cv2 as cv
import ctypes as C

from abc import ABC, abstractmethod

class FaceRecognizer(ABC):
     @staticmethod
     def create(args): #Args - dict("name", "dll", "db")
         if args["name"] == 'PVL':
            return PVLRecognizer(args["dll"], args["db"])
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
            return DNNDetector(args["model"], args["config"], args["width"], args["height"],args["threshold"])
         else:
            raise Exception('Error: wrong detector name')

     @abstractmethod
     def detect(self, img,  threshold):
         """Detect faces on image"""

class FaceLandmarks(ABC):
    @staticmethod
    def create(args): #Args - dict("name", "dll", "db")
         if args["name"] == 'DNNLandmarks':
            return DNNLandmarks(args["model"], args["config"], args["width"], args["height"])
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
        # print(out)
        landmarks = []
        for i in range(5):
            # print(i)
            landmarks.append((out[2*i],out[2*i+1]))
        return landmarks

    def align(self, img, desiredLandmarkPoints):
        landmarks = self.findLandmarks(img)
        warp = getAffineTransform(landmarks, desiredLandmarkPoints)
        warp_dst = warpAffine( src, warp_dst, warp_mat, warp_dst.size() );

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

# class DNNRecognizer(FaceRecognizer):
#     def __init__(self, dllPath, dbPath):


#     def register(self, img, ID):
#         return True

#     def recognize(self, img):
#         return True

class PVLRecognizer(FaceRecognizer):
    def __init__(self, dllPath, dbPath):
        try:
          self.PVL = C.cdll.LoadLibrary(dllPath)
          p = C.create_string_buffer(bytes(dbPath.encode()))
          self.PVL.SetDB.argtypes = [C.c_char_p]
          self.PVL.SetDB(p)
        except OSError:
           raise Exception('Can`t load dll')

    def register(self, img, ID):
        res = self.PVL.Register(img.shape[0],
                    img.shape[1],
                    img.ctypes.data_as(C.POINTER(C.c_ubyte)), ID)
        if(ID != res):
           raise Exception('An error occured while register')
        return True

    def recognize(self, img):
         x =  C.c_int(0)
         xptr = C.pointer(x)
         y = C.c_int(0)
         yptr = C.pointer(y)
         w = C.c_int(0)
         wptr = C.pointer(w)
         h = C.c_int(0)
         hptr = C.pointer(h)
         ID = self.PVL.Recognize(img.shape[0],
                            img.shape[1],
                            img.ctypes.data_as(C.POINTER(C.c_ubyte)),
                            xptr, yptr, wptr, hptr)
         return (ID, (x.value, y.value, w.value, h.value))

    def getUID(self):
        return self.PVL.UnknownID()

    def getNewID(self):
        return self.PVL.GetNewID()