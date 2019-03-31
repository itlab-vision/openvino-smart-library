import sys, os
import numpy as np
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox 
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import (Qt, QCoreApplication, QThread, QPoint, pyqtSignal, pyqtSlot)

from datetime import datetime, date, time
sys.path.insert(0, 'GUI')

import StartWin #design
import AdminWin  #design
import ReaderWin #design
import BookWin #design

sys.path.insert(0, 'modules')
import face_recognizer
import book_recognizer
sys.path.insert(0, "infrastructure")
from CSVDatabase import *
from Data_types.User import *
from Data_types.Book import *

#Global user ID
#ID = 0
#Face Recgonizer dependencies
FRName = "PVL"
dllPath = "modules/pvl/build/Release/PVL_wrapper.dll"
dbPath = "infrastructure/database/facesdb.xml"
#Book Recognizer dependencies
BRName = "ORB"

#Data base files
usersTable = "infrastructure/Database/Users/Users.csv"

#Поток для отрисовки видео с вебкамеры
class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    returnID = pyqtSignal(int)
    returnUID = pyqtSignal(int)
    
    def run(self): # Как передать агументы? Возвратить?
        rec = face_recognizer.FaceRecognizer.create(FRName)
        rec.init(dllPath) # передавать через параметры
        rec.XMLPath(dbPath)
        cap = cv2.VideoCapture(0)
        UID = rec.getUID()
        self.returnUID.emit(UID)
        self.check = False
        name = "UNKNOWN"
        CSV = CSVDatabase()
        while True:
            ret, f = cap.read()
            (ID, (x, y, w, h)) = rec.recognize(f)
            if (ID != UID):
              name = (CSV.GetUser(ID))[0].first_name #Можно выводить имя пользователя
              cv2.putText(f, "You are already a member." , (10,460), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
            else:
              name = "UNKNOWN"
              cv2.putText(f, "You are not a member" , (10,460), 
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 208, 86), 1)
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(f, name , (x - 10  ,y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
            if(self.check == True and ID == UID):
               rec.register(f,  self.newID)
               self.check =  False
            rgbImage = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                         QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convertToQtFormat)
            resizeImage = pixmap.scaled(472, 354, Qt.KeepAspectRatio)
            self.changePixmap.emit(resizeImage)
            self.returnID.emit(ID)
            
#получить newID из основного потока
    def passNewID(self, newID):
        self.newID = newID
        self.check = True #флаг того, что newID получен и можно регистрировать
        
#функция для остановки потока 
    def stop(self):
        self.terminate()
#Окно входа в приложение
class StartWindow(QtWidgets.QMainWindow, StartWin.Ui_MainWindow):
     def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
#        
        self.check = True
        
#Начинаем отрисовку видео с веб камеры в новом потоке        
        self.image = QPixmap()
        self.thread = Thread(self)
        self.thread.changePixmap.connect(self.setPixmap) 
        self.thread.returnID.connect(self.getID)
        self.thread.returnUID.connect(self.getUID)
        self.thread.start()
        
        self.btnBack.setIcon(QIcon("GUI/ui/backArrow.png"))
        #hide from view sign up elements
        self.showSignIn()
        #assign func on btns
        self.btnSignUp.clicked.connect(self.showSignUp)
        self.btnBack.clicked.connect(self.showSignIn)
        self.btnSignUp2.clicked.connect(self.signUp)
        self.btnSignIn.clicked.connect(self.signIn) 
        self.lineEditFName.textChanged.connect(self.enableBtnSignUp2)
        self.lineEditLName.textChanged.connect(self.enableBtnSignUp2)
        self.lineEditMName.textChanged.connect(self.enableBtnSignUp2)
        self.lineEditPhone.textChanged.connect(self.enableBtnSignUp2)
    
     def paintEvent(self, event):
        self.labelCamera.setPixmap(self.image)

     @pyqtSlot(QPixmap)
     def setPixmap(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        self.update()

#Функция, принимающия распознанный ID из потока
     @pyqtSlot(int)   
     def getID(self, ID):
        currID = ID
        """Нам достаточно распознать человека один раз, поэтому 
           здесь эта проверка"""
        if (currID != self.UID and self.check == True):
            self.ID = currID
            self.check = False
            self.enableBtnSignIn()
        self.enableBtnSignUp2()
            
#Функция, принимающия ID неизвестного пользователя из потока  
     @pyqtSlot(int)   
     def getUID(self, UID):
        self.UID = UID
        self.ID = UID
        print("UID =" , self.UID)

#Событие закрытия текущего окна        
     def closeEvent(self, event):
            cap = cv2.VideoCapture(0)
            cap.release()
            self.thread.stop()
            print("thread stopped")
            event.accept()
            
     def showSignUp(self):
         #hide signin elemnts
         self.labelHeader.hide()
         self.btnSignUp.hide()
         self.labelInfo.hide()
         self.btnSignIn.hide()
         #show signup elements
         self.labelHeader2.show()
         self.btnBack.show()
         self.labelFName.show()
         self.labelLName.show()
         self.labelMName.show()
         self.labelPhone.show()
         self.lineEditFName.show()
         self.lineEditLName.show()
         self.lineEditMName.show()
         self.lineEditPhone.show()
         self.btnSignUp2.show()  
         
     def showSignIn(self):
         #hide from view sign up elements
         self.labelHeader2.hide()
         self.btnBack.hide()
         self.labelFName.hide()
         self.labelLName.hide()
         self.labelMName.hide()
         self.labelPhone.hide()
         self.lineEditFName.hide()
         self.lineEditLName.hide()
         self.lineEditMName.hide()
         self.lineEditPhone.hide()
         self.btnSignUp2.hide()
         #show sign in elements
         self.labelHeader.show()
         self.btnSignUp.show()
         self.labelInfo.show()
         self.btnSignIn.show()
                         
     def enableBtnSignIn(self): 
         if(self.ID != self.UID):
             self.btnSignIn.setEnabled(True)
         else:
             self.btnSignIn.setEnabled(False)  
    
     def enableBtnSignUp2(self):
        if(len(self.lineEditFName.text()) > 0 and  
           len(self.lineEditLName.text()) > 0 and
            len(self.lineEditMName.text()) > 0 and  
            len(self.lineEditPhone.text()) > 0 and
            self.ID == self.UID):
             self.btnSignUp2.setEnabled(True)
        else:
             self.btnSignUp2.setEnabled(False)  
        
     def signIn(self):
        if (self.ID != self.UID):
            CSV = CSVDatabase()
            role = (CSV.GetUser(self.ID))[1]
            self.close()
            if (int(role.role_id) == 1):
                self.readerWin = ReaderWindow(self.ID)
                self.readerWin.show()
            else:
                self.adminWin = AdminWindow(self.ID)
                self.adminWin.show()           

     def signUp(self):
        CSV = CSVDatabase()
        fName = self.lineEditFName.text() # first name 
        lName = self.lineEditLName.text() # last name
        mName = self.lineEditMName.text() # middle name
        phone = self.lineEditPhone.text() 
        #insert user in DB
        newID = NumOfLines(usersTable)
        user = User(newID, phone, fName, lName, mName)
        user._print()
        print("Result:")
        print(CSV.AddUser(user))
        self.thread.passNewID(newID)
        
       
class AdminWindow(QtWidgets.QMainWindow, AdminWin.Ui_MainWindow):
    def __init__(self, ID):
        super().__init__()
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.btnBook.clicked.connect(self.GetBook)
        self.btnAddBook.clicked.connect(self.AddBook) 
        self.btnInfoReaders.clicked.connect(self.GetInfoReaders) 
        self.btnInfoBooks.clicked.connect(self.GetInfoBooks) 
        self.btnInfoBBooks.clicked.connect(self.GetInfoBB) # get information about borrowed books
        self.ID = ID
        
    def GetBook(self):
        rec = book_recognizer.Recognizer()
        rec.Create(BRName)
#        #---Функция БД, присваивающая templ список с изображениями обложек-----------
        templ = [ os.path.join("infrastructure/Database/Books/Covers/", b) 
                for b in os.listdir("infrastructure/Database/Books/Covers/")
                 if os.path.isfile(os.path.join("infrastructure/Database/Books/Covers/", b)) ]
        #-----------------------------------------------------------------------------
        cap = cv2.VideoCapture(0)
        i = 0
        l = len(templ)
        res_arr = []
        _, frame = cap.read()
        ym, xm, _ = frame.shape
        for i in range(l):
            res_arr.append(0)
        
        
        while(True): 
            _, frame = cap.read()
            crop_frame = frame[ym//2 - 170 : ym//2 + 170, xm//2 - 120 : xm//2 + 120]
            cv2.rectangle(frame, (xm//2 - 110, ym//2 - 150), (xm//2 + 110, ym//2 + 150), (0, 255, 255))
            cv2.imshow("web", frame)
            cv2.waitKey(1)   
            recognize_result = rec.Recognize(crop_frame, templ, 0.7)
            print(res_arr, "\n")
            for i in range(l):
                res_arr[i] = res_arr[i] + recognize_result[i]
            if max(res_arr) > 1000:
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
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
         #disable editing
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["ID", "Phone", "First name",
                                                     "Last name", "Middle name"])
        #insert row
        self.table.verticalHeader().hide()
        
        CSV = CSVDatabase()
        User = CSV.GetAllUsers()
        for i in enumerate(User):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(User[i[0]].user_id))
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(User[i[0]].phone))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(User[i[0]].first_name))
            self.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(User[i[0]].last_name))
            self.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(User[i[0]].middle_name))
        #fit available space
        header = self.table.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        #self.tableWidget.resizeColumnsToContents()
        print("GetInfoReaders")
        
    def GetInfoBooks(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
         #disable editing
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                     "Publisher", "Publication date", "Cover"])
        #insert row
        self.table.verticalHeader().hide()
        
        CSV = CSVDatabase()
        Book = CSV.GetAllBooks()
        for i in enumerate(Book):
            c = ", " # строка для разделения авторов
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(Book[i[0]].book_id))
            authorsStr = "" # строка для размещения в ней ФИО авторов
            for j in enumerate(Book[i[0]].authors):
                if (j[0] == len(Book[i[0]].authors) - 1):
                    c = ''
                authorsStr += (Book[i[0]].authors[j[0]].first_name + ' ' +
                            Book[i[0]].authors[j[0]].last_name + ' ' +
                            Book[i[0]].authors[j[0]].middle_name + c)
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(authorsStr))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(Book[i[0]].title))
            self.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(Book[i[0]].publisher))
            self.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(Book[i[0]].year))
            self.table.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(Book[i[0]].file_path))
        #fit available space
        header = self.table.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        print("GetInfoBooks")
    
    def GetInfoBB(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(9)
        #disable editing
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["User ID", "Book ID", "First name", "Last name",
                                                     "Middle name", "Phone", "Title", "Borrow date",
                                                     "Return date"])
        #insert row
        self.table.verticalHeader().hide()
        
        CSV = CSVDatabase()
        BBook = CSV.GetBorrowedBooks()
        Book = BBook[0]
        DateB = BBook[1]
        DateR = BBook[2]
        User = BBook[3]
        for i in enumerate(DateB):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(User[i[0]].user_id))
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(Book[i[0]].book_id))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(User[i[0]].first_name))
            self.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(User[i[0]].last_name))
            self.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(User[i[0]].middle_name))
            self.table.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(User[i[0]].phone))
            self.table.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(Book[i[0]].title))
            self.table.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(DateB[i[0]]))
            self.table.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem(DateR[i[0]]))
        #fit available space
        header = self.table.horizontalHeader()    
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
    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.GetBook)
        #tabel 1 with borrowed books
        self.tableBooks.setColumnCount(6)
        #disable editing
        self.tableBooks.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Рассмотреть возможность вывода обложки книги в таблицу
        self.tableBooks.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date"])
        self.tableBooks.resizeColumnsToContents()
        #tabel 2 with previously taken books
        self.tableBooks2.setColumnCount(7)
        #disable editing
        self.tableBooks2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableBooks2.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date", "Return date"])
        self.tableBooks2.resizeColumnsToContents()    
    
    def GetBook(self):
        print("hello")

class BookWindow(QtWidgets.QMainWindow, BookWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.btnAddBook.clicked.connect(self.Add)
        self.btnAddBook.setEnabled(False)
        self.btnSelectFile.clicked.connect(self.OpenFile)
        self.lineEditTitle.textChanged.connect(self.EnableBtnAdd)
        self.lineEditAuthor.textChanged.connect(self.EnableBtnAdd)
        self.lineEditPublisher.textChanged.connect(self.EnableBtnAdd)
        self.lineEditDate.textChanged.connect(self.EnableBtnAdd)
   
    """сделать запись в БД"""
    def Add(self):
        title = self.lineEditTitle.text()
        author = self.lineEditAuthor.text()
        publisher = self.lineEditPublisher.text()
        date = self.lineEditDate.text()
        dateNow = str(datetime.now())
        dateNow = dateNow.replace(" ", "")
        dateNow = dateNow.replace(":", "")
        dateNow = dateNow.replace(".", "")
        coverName = dateNow
        self.Cover.save("infrastructure/Database/Books/Covers/" + coverName + ".png")
        print(title, " ", author, " ", publisher, " ", date, " ",dateNow)
        print("add")
        self.close()
        
    """Добавить путь до обложки в БД
       В функции добавления новой обложки необходимо реализовать именование обложек
        в соответствии с БД, проверять имя на уникальность и т.д"""
    def OpenFile(self):
        fileName = QFileDialog.getOpenFileName(self.labelPicture, 
                                                     'Open File',"",
                                                     "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        """Pixmap - показываем миниатюру картинки на экране загрузки 
           self.Cover - сохраняем полную картинку, чтобы потом ее записать в нужную папку"""
        if(fileName[0] != ""):
            pixmap = QPixmap(fileName[0])
            self.Cover = pixmap 
            pixmap = pixmap.scaled(self.labelPicture.width(),
                                   self.labelPicture.height(), 
                                   QtCore.Qt.KeepAspectRatio)
            self.labelPicture.setPixmap(pixmap)
            self.EnableBtnAdd()
            print(self.labelPicture.pixmap())
            print("open")
        
    def EnableBtnAdd(self):
        if(len(self.lineEditTitle.text()) > 0 and
           len(self.lineEditAuthor.text()) > 0 and
           len(self.lineEditPublisher.text()) > 0 and
           len(self.lineEditDate.text()) > 0 and 
           self.labelPicture.pixmap()):
             self.btnAddBook.setEnabled(True)
        else:
             self.btnAddBook.setEnabled(False)   

def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = StartWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 