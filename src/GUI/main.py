import sys, os
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import LoginWin  #design
import SignupWin #design
import AdminWin  #design
import AdminWin  #design
import ReaderWin #design
import BookWin #design
sys.path.insert(0, '../modules')
import face_recognizer
import book_recognizer
sys.path.insert(0, "../infrastructure")
from CSVDatabase import *
from Data_types.User import *
from Data_types.Book import *

ID = 0

class LoginWindow(QtWidgets.QMainWindow, LoginWin.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.SignUp)
        self.pushButton_2.clicked.connect(self.SignIn)  # execute func on button click
        
        self.admWin = AdminWindow()
        self.readerWin = ReaderWindow()
        self.signupWin = SignupWindow()
    """Пофиксить работу БД при входе"""    
    def SignIn(self):
        rec = face_recognizer.FaceRecognizer.Create("PVL")
        rec.Init("..\\modules\\pvl\\build\\Release\\PVL_wrapper.dll") # передавать через параметры
        rec.XMLPath("..\\infrastructure\\database\\facesdb.xml")
        cap = cv2.VideoCapture(0)
        UID = rec.GetUID()
        name = "UNKNOWN"
        ch = 0
        CSV = CSVDatabase()
        while(True): 
            _, f = cap.read()
            (ID, (x, y, w, h)) = rec.Recognize(f)
            print(ID)
            if (ID != UID):
              name = (CSV.GetUser(ID))[0].first_name
              print(name)
            else:
               cv2.putText(f, "You are not a member." , (135, 460),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 1)  
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(f, name , (x,y-2), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
            cv2.imshow("web", f)
            if ID != UID or ch & 0xFF == ord('q') or ch & 0xFF == ord('Q'):
                break
            ch = cv2.waitKey(1) 
        h = cv2.waitKey(1000)
        cap.release()
        cv2.destroyAllWindows()
        if (ID != UID):
            CSV = CSVDatabase()
            role = (CSV.GetUser(ID))[1]
            self.close()
            if (int(role.role_id) == 1):
                self.readerWin.show()
            else:
                self.admWin.show()
        
    def SignUp(self):
        self.close()
        self.signupWin.show()

class SignupWindow(QtWidgets.QMainWindow, SignupWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())   
        self.pushButton.clicked.connect(self.SignUp)
        self.pushButton.setEnabled(False)
        
        self.lineEdit.textChanged.connect(self.EnableBtn)
        self.lineEdit_2.textChanged.connect(self.EnableBtn)
        self.lineEdit_3.textChanged.connect(self.EnableBtn)
        self.lineEdit_4.textChanged.connect(self.EnableBtn)
        
    """Проверить реализацию записи пользователя в БД"""
    def SignUp(self):
        CSV = CSVDatabase()
        fName = self.lineEdit.text() # first name 
        lName = self.lineEdit_2.text() # last name
        mName = self.lineEdit_3.text() # middle name
        phone = self.lineEdit_4.text() 
        #insert user in DB
        newID = NumOfLines("../infrastructure/Database/Users/Users.csv")
        print("new ID = ", newID)
        print("User:")
        user._print()
        print("Result:")
        print(CSV.AddUser(user))
#        print(NumOfLines("../infrastructure/Database/Users/Users.csv"))
        #---------------------
        rec = face_recognizer.FaceRecognizer.Create("PVL")
        rec.Init("../modules/pvl/build/Release/PVL_wrapper.dll") # передавать через параметры
        rec.XMLPath("../infrastructure/database/facesdb.xml")
        cap = cv2.VideoCapture(0)
        UID = rec.GetUID()
        name = "UNKNOWN"
        while(True): 
            _, f = cap.read()
            (ID, (x, y, w, h)) = rec.Recognize(f)
            if (ID != UID):
              name = str(ID) #Можно выводить имя пользователя
              cv2.putText(f, "You are already a member. Press Q to exit" , (10,460), 
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
            else:
              cv2.putText(f, "Press R to register" , (10,460), 
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(f, name , (x - 10  ,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
            cv2.imshow("web", f)
            ch = cv2.waitKey(1)
            if (ch & 0xFF == ord('r') or ch & 0xFF == ord('R')) and ID == UID:
                checkID = rec.Register(f,  newID) #Необходимо генерировать новый ID
                break
            if ch & 0xFF == ord('q') or ch & 0xFF == ord('Q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.close()
        self.loginWin = LoginWindow()
        self.loginWin.show()
       
    
    def EnableBtn(self):
        if(len(self.lineEdit.text()) > 0 and  len(self.lineEdit_2.text()) > 0 and
            len(self.lineEdit_3.text()) > 0 and  len(self.lineEdit_4.text()) > 0 ):
             self.pushButton.setEnabled(True)
        else:
             self.pushButton.setEnabled(False)
        
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
        self.bookWin = BookWindow()
        self.bookWin.show()
        print("AddBook")
    
    def GetInfoReaders(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
         #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Phone", "First name",
                                                     "Last name", "Middle name"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        
        CSV = CSVDatabase()
        User = CSV.GetAllUsers()
        for i in enumerate(User):
            print(i[0])
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(User[i[0]].user_id))
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(User[i[0]].phone))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(User[i[0]].first_name))
            self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(User[i[0]].last_name))
            self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(User[i[0]].middle_name))
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
        
        CSV = CSVDatabase()
        Book = CSV.GetAllBooks()
        for i in enumerate(Book):
            c = ", " # строка для разделения авторов
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(Book[i[0]].book_id))
            authorsStr = "" # строка для размещения в ней ФИО авторов
            for j in enumerate(Book[i[0]].authors):
                if (j[0] == len(Book[i[0]].authors) - 1):
                    c = ''
                authorsStr += (Book[i[0]].authors[j[0]].first_name + ' ' +
                            Book[i[0]].authors[j[0]].last_name + ' ' +
                            Book[i[0]].authors[j[0]].middle_name + c)
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(authorsStr))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(Book[i[0]].title))
            self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(Book[i[0]].publisher))
            self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(Book[i[0]].year))
            self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(Book[i[0]].file_path))
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
        self.tableWidget.setHorizontalHeaderLabels(["User ID", "Book ID", "First name", "Last name",
                                                     "Middle name", "Phone", "Title", "Borrow date",
                                                     "Return date"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        
        CSV = CSVDatabase()
        BBook = CSV.GetBorrowedBooks()
        Book = BBook[0]
        DateB = BBook[1]
        DateR = BBook[2]
        User = BBook[3]
        for i in enumerate(DateB):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(User[i[0]].user_id))
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(Book[i[0]].book_id))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(User[i[0]].first_name))
            self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(User[i[0]].last_name))
            self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(User[i[0]].middle_name))
            self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(User[i[0]].phone))
            self.tableWidget.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(Book[i[0]].title))
            self.tableWidget.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(DateB[i[0]]))
            self.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem(DateR[i[0]]))
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
       
class ReaderWindow(QtWidgets.QMainWindow, ReaderWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.GetBook)
        #tabel 1 with borrowed books
        self.tableWidget.setColumnCount(6)
        #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Рассмотреть возможность вывода обложки книги в таблицу
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date"])
        self.tableWidget.resizeColumnsToContents()
        #tabel 2 with previously taken books
        self.tableWidget_2.setColumnCount(7)
        #disable editing
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date", "Return date"])
        self.tableWidget_2.resizeColumnsToContents()    
    
    def GetBook(self):
        print("hello")

class BookWindow(QtWidgets.QMainWindow, BookWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.pushButton_add.clicked.connect(self.Add)
        self.pushButton_add.setEnabled(False)
        self.pushButton.clicked.connect(self.OpenFile)
        self.pushButton.setEnabled(False)
        self.lineEdit_name.textChanged.connect(self.EnableBtn1)
        self.lineEdit_title.textChanged.connect(self.EnableBtn2)
        self.lineEdit_author.textChanged.connect(self.EnableBtn2)
        self.lineEdit_publisher.textChanged.connect(self.EnableBtn2)
        self.lineEdit_date.textChanged.connect(self.EnableBtn2)
    """сделать запись в БД"""    
    def Add(self):
        title = self.lineEdit_title.text()
        author = self.lineEdit_author.text()
        publisher = self.lineEdit_publisher.text()
        date = self.lineEdit_date.text()
        coverName = self.lineEdit_name.text()
        self.Cover.save("../infrastructure/Database/Books/Covers/" + coverName + ".png")
        print(title, " ", author, " ", publisher, " ", date)
        print("add")
        self.close()
        
    """Добавить путь до обложки в БД
       В функции добавления новой обложки необходимо реализовать именование обложек
        в соответствии с БД, проверять имя на уникальность и т.д"""
    def OpenFile(self):
        fileName = QFileDialog.getOpenFileName(self.label_pix, 
                                                     'Open File',"",
                                                     "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        """Pixmap - показываем миниатюру картинки на экране загрузки 
           self.Cover - сохраняем полную картинку, чтобы потом ее записать в нужную папку"""
        pixmap = QPixmap(fileName[0])
        self.Cover = pixmap 
        pixmap = pixmap.scaled(self.label_pix.width(), self.label_pix.height(), QtCore.Qt.KeepAspectRatio)
        self.label_pix.setPixmap(pixmap)
        print("open")
        
    def EnableBtn1(self):
        if len(self.lineEdit_name.text()) > 0:
             self.pushButton.setEnabled(True)
        else:
             self.pushButton.setEnabled(False)
             
    def EnableBtn2(self):
        if(len(self.lineEdit_title.text()) > 0 and  len(self.lineEdit_author.text()) > 0 and
            len(self.lineEdit_publisher.text()) > 0 and  len(self.lineEdit_date.text()) > 0 ):
             self.pushButton_add.setEnabled(True)
        else:
             self.pushButton_add.setEnabled(False)   
def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = LoginWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 