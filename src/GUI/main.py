import sys, os
import cv2
from PyQt5 import QtWidgets
import LoginWin  #design
import AdminWin  #design
sys.path.insert(0, '../modules')
import face_recognizer
import book_recognizer

class LoginWindow(QtWidgets.QMainWindow, LoginWin.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.pushButton_2.clicked.connect(self.SignIn)  # execute func on button click
        self.dialog = AdminWindow()
        
    def SignIn(self):
        rec = face_recognizer.PVLRecognizer() #передавать через параметры
        rec.Create("..\\modules\\pvl\\build\\Release\\PVL_wrapper.dll") # передавать через параметры
        cap = cv2.VideoCapture(0)
        UID = -10000
        name = "UNKNOWN"
        while(True): 
            _, f = cap.read()
            (ID, (x, y, w, h)) = rec.Recognize(f)
            if (ID != UID):
              name = str(ID)
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
            cv2.imshow("web", f)
            ch = cv2.waitKey(1)
            if ID != -10000:
                break
        ch = cv2.waitKey(1000)
        cap.release()
        cv2.destroyAllWindows()
        print(ID)
        self.close()
        self.dialog.show()

class AdminWindow(QtWidgets.QMainWindow, AdminWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.pushButton_1.clicked.connect(self.GetBook)
        self.pushButton_2.clicked.connect(self.AddBook) 
        self.pushButton_3.clicked.connect(self.GetInfoReaders) 
        self.pushButton_4.clicked.connect(self.GetInfoBooks) 
        self.pushButton_5.clicked.connect(self.GetInfoBB) # get information about borrowed books
    
    def GetBook(self):
        rec = book_recognizer.Recognizer()
        rec.Create("SURF")
#        #---Функция БД, присваивающая templ список с изображениями обложек-----------
        templ = [ os.path.join("covers/", b) for b in os.listdir("covers/")
                 if os.path.isfile(os.path.join("covers/", b)) ]
        #-----------------------------------------------------------------------------
        #---Получить видеопоток с камеры----------------------------------------------
        cap = cv2.VideoCapture(0)
        #-----------------------------------------------------------------------------
        i = 0
        l = len(templ)
        res_arr = []
        for i in range(l):
            res_arr.append(0)
        while(True): 
            _, frame = cap.read()
            cv2.imshow("web", frame)
            ch = cv2.waitKey(1)   
            recognize_result = rec.Recognize(frame, templ, 0.87)
            print(res_arr, "\n")
            for i in range(l):
                res_arr[i] = res_arr[i] + recognize_result[i]
            if max(res_arr) > 8000:
                break
        print(res_arr, "\n")
        cap.release()
        cv2.destroyAllWindows()
        idres = res_arr.index(max(res_arr))
        print("Book id = ", idres)

        
    def AddBook(self):
        print("AddBook")
    
    def GetInfoReaders(self):
        print("GetInfoReaders")
        
    def GetInfoBooks(self):
        print("GetInfoBooks")
    
    def GetInfoBB(self):
        print("GetInfoBB")
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = LoginWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 