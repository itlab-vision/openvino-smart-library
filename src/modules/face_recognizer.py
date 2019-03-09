import numpy as np
import ctypes as C
from abc import ABC, abstractmethod

class FaceRecognizer(ABC):
     @staticmethod
     def Create(name):
         if name == "PVL":
            rec = PVLRecognizer()
            return rec
         else:
            raise Exception('Error: wrong recognizer name')
           
     @abstractmethod
     def Register(self, img):
         """Register new reader"""
         
     @abstractmethod
     def Recognize(self, img):
         """Recognize valid user"""
         
class PVLRecognizer(FaceRecognizer):
    def Init(self, path):
        try:
          self.PVL = C.cdll.LoadLibrary(path)
        except OSError:
          print("Can`t load dll")
          return False
        else:
          return True
      
    def XMLPath(self, path):
        p = C.create_string_buffer(bytes(path.encode())) # may be it can be done easier
        self.PVL.GetPath.argtypes = [C.c_char_p]
        self.PVL.GetPath(p)
        
    def Register(self, img, ID):
       return self.PVL.Register(img.shape[0],
                    img.shape[1],
                    img.ctypes.data_as(C.POINTER(C.c_ubyte)), ID)
       
    def Recognize(self, img):
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
    
    def GetUID(self):
        return self.PVL.UnknownID()