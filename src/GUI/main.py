import sys, os
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
import LoginWin  #design
import SignupWin
import AdminWin  #design
sys.path.insert(0, '../modules')
import face_recognizer
import book_recognizer

class LoginWindow(QtWidgets.QMainWindow, LoginWin.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.SignUp)
        self.pushButton_2.clicked.connect(self.SignIn)  # execute func on button click
        self.admwin = AdminWindow()
#        self.readerwin = ReaderWindow()
        self.signupwin = SignupWindow()
        
    def SignIn(self):
#        rec = face_recognizer.PVLRecognizer() #передавать через параметры
#        rec.Create("..\\modules\\pvl\\build\\Release\\PVL_wrapper.dll") # передавать через параметры
#        cap = cv2.VideoCapture(0)
#        UID = -10000
#        name = "UNKNOWN"
#        while(True): 
#            _, f = cap.read()
#            (ID, (x, y, w, h)) = rec.Recognize(f)
#            if (ID != UID):
#              name = str(ID)
#            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
#            cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
#            cv2.imshow("web", f)
#            ch = cv2.waitKey(1)
#            if ID != -10000:
#                break
#        ch = cv2.waitKey(1000)
#        cap.release()
#        cv2.destroyAllWindows()
#        print(ID)
        self.close()
        self.admwin.show()
    def SignUp(self):
        self.close()
        self.signupwin.show()

class SignupWindow(QtWidgets.QMainWindow, SignupWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())   
        
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
        templ = [ os.path.join("../infrastructure/Database/Books/Covers/", b) 
                for b in os.listdir("../infrastructure/Database/Books/Covers/")
                 if os.path.isfile(os.path.join("../infrastructure/Database/Books/Covers/", b)) ]
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
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
         #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Last name", "First name", 
                                                     "Middle name", "Phone", "Role"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("Вихрев"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("Иван"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("Борисович"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("+00000000000"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("Administrator"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        #self.tableWidget.resizeColumnsToContents()
        print("GetInfoReaders")
        
    def GetInfoBooks(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
         #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                     "Publisher", "Publication date", "Cover"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("---"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        print("GetInfoBooks")
    
    def GetInfoBB(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(9)
        #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Last name", "First name", 
                                                     "Middle name", "Phone", "Author", "Title", "Borrow date",
                                                     "Return date"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem("---"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        print("GetInfoBBooks")
       
    

def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = LoginWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 