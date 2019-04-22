import sys, os, re
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
    
    def __init__(self, recName):
       QThread.__init__(self)
       self.check = False
       self.name = recName
    
    def run(self):
       if (self.name == "face"):
         self.faceRecognition()
       if (self.name == "book"):
         self.bookRecognition()
       
    def faceRecognition(self):
        rec = face_recognizer.FaceRecognizer.create(FRName)
        rec.init(dllPath) # передавать через параметры
        rec.XMLPath(dbPath)
        cap = cv2.VideoCapture(0)
        UID = rec.getUID()
        self.returnUID.emit(UID)

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
            
    def bookRecognition(self):
        rec = book_recognizer.Recognizer()
        rec.create(BRName)
        templ = []

        for i in os.listdir("infrastructure/Database/Books/Covers/"):
            if (re.fullmatch('\d+.png', i)):
                templ.append(os.path.join("infrastructure/Database/Books/Covers/", i))
        
#   
        cap = cv2.VideoCapture(0)
        i = 0
        det = cv2.ORB_create()
        l = len(templ)
        resArr = []
        desTpl = []
        _, frame = cap.read()
        ym, xm, _ = frame.shape
        for i in range(l):
            resArr.append(0)
    
        #Список с ключевыми точками шаблонов
        for t in templ:
            tpl = cv2.imread(t)
            tplGray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
            _, tmp = det.detectAndCompute(tplGray, None)
            desTpl.append(tmp)
        
#        for k in range(0,100):
#            _, frame = cap.read()
#            cv2.rectangle(frame, (xm//2 - 110, ym//2 - 150), 
#                          (xm//2 + 110, ym//2 + 150), (0, 255, 255))
#            cv2.putText(frame, '0%', (200, 200),
#                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1],
#                                       rgbImage.shape[0], QImage.Format_RGB888)
#            pixmap = QPixmap.fromImage(convertToQtFormat)
#            resizeImage = pixmap.scaled(472, 354, Qt.KeepAspectRatio)
#            self.changePixmap.emit(resizeImage)      
            
        while(True): 
            _, frame = cap.read()
            cropFrame = frame[ym//2 - 170 : ym//2 + 170,
                                  xm//2 - 120 : xm//2 + 120]
            cv2.rectangle(frame, (xm//2 - 110, ym//2 - 150), 
                              (xm//2 + 110, ym//2 + 145), (0, 255, 255))
            
            if (self.check == True and resArr):
#                cropFrame = frame[ym//2 - 170 : ym//2 + 170,
#                                  xm//2 - 120 : xm//2 + 120]
#                cv2.rectangle(frame, (xm//2 - 110, ym//2 - 150), 
#                              (xm//2 + 110, ym//2 + 150), (0, 255, 255))
                recognizeResult = rec.recognize(cropFrame, desTpl, 0.7)
                out = str(100 * max(resArr) / 400)
                out = out + '%'
                cv2.putText(frame, out, (200, 200), cv2.FONT_HERSHEY_SIMPLEX,
                                                          1, (0, 255, 255), 2)
                for i in range(l):
                    resArr[i] = resArr[i] + recognizeResult[i]
                if max(resArr) > 400:
                    ID = resArr.index(max(resArr))
                    self.returnID.emit(ID)
                    resArr.clear()
                    for i in range(l):
                       resArr.append(0)
                    self.check = False; 
                    
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                         QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convertToQtFormat)
            resizeImage = pixmap.scaled(472, 354, Qt.KeepAspectRatio)
            self.changePixmap.emit(resizeImage)   
            
            
            
#        print(resArr, "\n")
#        idRes = resArr.index(max(resArr))
#        print("Book id = ", idRes)
        
#получить newID из основного потока
    def passNewID(self, newID):
        self.newID = newID
        self.check = True #флаг того, что newID получен и можно регистрировать
    
    def recognizeBook(self):
        self.check = True #флаг того, что нужно распознать книгу
        
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
        self.thread = Thread("face")
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
        
#зачем нужен paint event?
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
        user = User(-1, phone, fName, lName, mName)
        user._print()
        newID = CSV.AddUser(user)
        print("Result: ")
        if(newID == -1):
            print("This user is already registered")
        else:
            print("ID = ", newID)
            self.thread.passNewID(newID)
        
       
class AdminWindow(QtWidgets.QMainWindow, AdminWin.Ui_MainWindow):
    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())  
        self.labelInfo2.hide()
        
        self.image = QPixmap()
        self.thread = Thread("book")
        self.thread.changePixmap.connect(self.setPixmap) 
        self.thread.returnID.connect(self.getBookID)
        self.thread.start()
        
        self.comboBox.currentIndexChanged.connect(self.comboBoxChanged, 
                                                 self.comboBox.currentIndex()) 
        self.CSV = CSVDatabase()
        self.labelHello.setText(self.labelHello.text()+ self.CSV.GetUser(ID)[0].first_name)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.GetInfoBooks()
        self.btnBook.clicked.connect(self.GetBook)
        self.btnAddBook.clicked.connect(self.AddBook) 
        
        
    def comboBoxChanged(self):
        if(self.comboBox.currentIndex() == 0):
            self.GetInfoBooks()
        if(self.comboBox.currentIndex() == 1):
            self.GetInfoReaders()
        if(self.comboBox.currentIndex() == 2):
            self.GetInfoBB()
        
    def GetBook(self):
        #self.thread.recognizeBook()
        #self.labelInfo2.show()
        userId = 10 # получить id текущего пользователя
        bookId = 10 # получить id распознанной книги
        CSV = CSVDatabase()
        CSV.ChangeBookStatus(userId, bookId)
        print("Book`s status was changed")
        
    @pyqtSlot(QPixmap)
    def setPixmap(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        self.labelCamera.setPixmap(self.image)
        self.update()  
        
    @pyqtSlot(int)   
    def getBookID(self, ID):
         self.bookID = ID
         self.labelInfo2.hide()
         print(self.bookID)
        
    def AddBook(self):
        self.bookWin = BookWindow()
        self.bookWin.show()
        print("AddBook")
    
    def GetInfoReaders(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["ID", "Phone", "First name",
                                                     "Last name", "Middle name"])
        #insert row
        User = self.CSV.GetAllUsers()
        for i in enumerate(User):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(User[i[0]].user_id))
            self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(User[i[0]].phone))
            self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(User[i[0]].first_name))
            self.table.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(User[i[0]].last_name))
            self.table.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(User[i[0]].middle_name))
        self.table.resizeColumnsToContents()
        print("GetInfoReaders")
        
    def GetInfoBooks(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Cover"])
        #insert row
        Book = self.CSV.GetAllBooks()
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
        self.table.resizeColumnsToContents() 
        print("GetInfoBooks")
    
    def GetInfoBB(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(9)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["User ID", "Book ID", "First name", "Last name",
                                                     "Middle name", "Phone", "Title", "Borrow date",
                                                     "Return date"])
        #insert row
        self.table.verticalHeader().hide()
        BBook = self.CSV.GetBorrowedBooks()
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
        self.table.resizeColumnsToContents() 
        print("GetInfoBBooks")
        
    def closeEvent(self, event):
            cap = cv2.VideoCapture(0)
            cap.release()
            self.thread.stop()
            print("thread stopped")
            event.accept()      
    
class ReaderWindow(QtWidgets.QMainWindow, ReaderWin.Ui_MainWindow):
    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.btnBook.clicked.connect(self.GetBook)
        self.CSV = CSVDatabase()
        self.labelHello.setText(self.labelHello.text()+ 
                                self.CSV.GetUser(ID)[0].first_name)
        
        self.labelInfo2.hide()
        
        self.image = QPixmap()
        self.thread = Thread("book")
        self.thread.changePixmap.connect(self.setPixmap) 
        self.thread.returnID.connect(self.getBookID)
        self.thread.start()
        
        self.btnBook.clicked.connect(self.GetBook)
        CSV = CSVDatabase()
        BBook = CSV.GetBorrowedBooks()
        Book = BBook[0]
        DateB = BBook[1]
        DateR = BBook[2]
        User = BBook[3]
        
        #tabel 1 with borrowed books
        self.tableBooks1.setColumnCount(6)
        self.tableBooks1.verticalHeader().hide()
        #disable editing
        self.tableBooks1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Рассмотреть возможность вывода обложки книги в таблицу
        self.tableBooks1.setHorizontalHeaderLabels(["Book ID", "Authors", "Title", 
                                                    "Publisher", "Publication date", "Borrow date"])
        for i in enumerate(DateB):
            if((DateR[i[0]] == "-1") and (int(User[i[0]].user_id) == self.ID)):
                c = ", " # строка для разделения авторов
                rowPosition = self.tableBooks1.rowCount()
                self.tableBooks1.insertRow(rowPosition)
                self.tableBooks1.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(Book[i[0]].book_id))
                authorsStr = "" # строка для размещения в ней ФИО авторов
                for j in enumerate(Book[i[0]].authors):
                    if (j[0] == len(Book[i[0]].authors) - 1):
                        c = ''
                    authorsStr += (Book[i[0]].authors[j[0]].first_name + ' ' +
                                Book[i[0]].authors[j[0]].last_name + ' ' +
                                Book[i[0]].authors[j[0]].middle_name + c)
                self.tableBooks1.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(authorsStr))
                self.tableBooks1.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(Book[i[0]].title))
                self.tableBooks1.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(Book[i[0]].publisher))
                self.tableBooks1.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(Book[i[0]].year))
                self.tableBooks1.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(DateB[i[0]]))
        
        self.tableBooks1.resizeColumnsToContents()
        
        #tabel 2 with previously taken books
        self.tableBooks2.setColumnCount(7)
        self.tableBooks2.verticalHeader().hide()
#       #disable editing
        self.tableBooks2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableBooks2.setHorizontalHeaderLabels(["Book ID", "Authors", "Title", 
                                                    "Publisher", "Publication date", "Borrow date", "Return date"])
        for k in enumerate(DateB):
            if((DateR[k[0]] != "-1") and (int(User[k[0]].user_id) == self.ID)):
                c = ", " # строка для разделения авторов
                rowPosition = self.tableBooks2.rowCount()
                self.tableBooks2.insertRow(rowPosition)
                self.tableBooks2.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(Book[k[0]].book_id))
                authorsStr = "" # строка для размещения в ней ФИО авторов
                for t in enumerate(Book[k[0]].authors):
                    if (t[0] == len(Book[k[0]].authors) - 1):
                        c = ''
                    authorsStr += (Book[k[0]].authors[t[0]].first_name + ' ' +
                                Book[k[0]].authors[t[0]].last_name + ' ' +
                                Book[k[0]].authors[t[0]].middle_name + c)
                self.tableBooks2.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(authorsStr))
                self.tableBooks2.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(Book[k[0]].title))
                self.tableBooks2.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(Book[k[0]].publisher))
                self.tableBooks2.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(Book[k[0]].year))
                self.tableBooks2.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(DateB[k[0]]))
                self.tableBooks2.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(DateR[k[0]]))
                
        self.tableBooks2.resizeColumnsToContents()    
        
    @pyqtSlot(QPixmap)
    def setPixmap(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
        self.image = image
        self.labelCamera.setPixmap(self.image)
        self.update()  
        
    @pyqtSlot(int)   
    def getBookID(self, ID):
         self.bookID = ID
         self.labelInfo2.hide()
         print(self.bookID)
    
    def GetBook(self):
        #self.thread.recognizeBook()
        #self.labelInfo2.show()
        userId = 10 # получить id текущего пользователя
        bookId = 10 # получить id распознанной книги
        CSV = CSVDatabase()
        CSV.ChangeBookStatus(userId, bookId)
        print("Book`s status was changed")
        # при нажатии на кнопку "Get book" этот метод срабатывает дважды
        
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
        """Нескольких авторов одной книги вводить в форму через запятную"""
        authors = []
        fname = ""
        lname = ""
        mname = ""
        flag = 0
        for c in author:
            if(flag == 4):
                flag = 0
                if(c == ' '):
                    continue;
            if(c == ' '):
                flag = flag + 1
                continue
            if(c == ','):
                flag = 4
                authors.append(Author(-1, fname, lname, mname))
                fname = ""
                lname = ""
                mname = ""
                continue
            if(flag == 0):
                fname += c
                continue
            if(flag == 1):
                lname += c
                continue
            if(flag == 2):
                mname += c
                continue
        authors.append(Author(-1, fname, lname, mname))
        
        publisher = self.lineEditPublisher.text()
        date = self.lineEditDate.text()
        dateNow = str(datetime.now())
        dateNow = dateNow.replace(" ", "")
        dateNow = dateNow.replace(":", "")
        dateNow = dateNow.replace(".", "")
        coverName = dateNow
        self.Cover.save("infrastructure/Database/Books/Covers/" + coverName + ".png")
        print(title, " ", author, " ", publisher, " ", date, " ",dateNow)
        book = Book(-1, coverName, title, date, publisher, authors)
        CSV = CSVDatabase()
        newID = CSV.AddBook(book)
        if(newID == -1):
            print("This book is already registered")
        else:
            print("ID = ", newID)
        self.close()
        
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
    window = ReaderWindow(1)  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 