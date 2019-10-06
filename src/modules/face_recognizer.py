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

class DNNFaceDetector():
     def __init__(self, modelPath, configPath, inputWidth, inputHeight, mean, swapRB, scale):
        self.model = modelPath
        self.config = configPath
        self.width = inputWidth
        self.height = inputHeight
        self.mean = mean
        self.swapRB = swapRB
        self.scale = scale
        backendId = cv.dnn.DNN_BACKEND_INFERENCE_ENGINE
        targetId = cv.dnn.DNN_TARGET_CPU
        self.net = cv.dnn.readNet(self.model, self.config)
        self.net.setPreferableBackend(backendId)
        self.net.setPreferableTarget(targetId)

     def detect(self, image):
        ddepth = cv.CV_32F
        resized = cv.resize(image, (self.width, self.height))
        blob = cv.dnn.blobFromImage(image, self.scale, (self.width, self.height),
                  self.mean, self.swapRB, False, ddepth)
        self.net.setInput(blob)
        outputBlobs	= self.net.forward()
        print(outputBlobs)






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