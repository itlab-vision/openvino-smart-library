import cv2
import numpy as np

from ui import *

sys.path.insert(0,"src/modules")
import face_recognizer as fr
import book_recognizer as br

sys.path.insert(0,"src/infrastructure")
from CSVDatabase import *
from Entities.User import *
from Entities.Book import *

unknownID = -1
path = "src/infrastructure/resources/"
class Thread(QThread):
    camera = pyqtSignal(QPixmap)
    returnUserID = pyqtSignal(int)
    returnBookID = pyqtSignal(int)

    userID = -1
    bookID = -1
    newUserID = -1

    allID = {-1:-1}

    def __init__(self):
       QThread.__init__(self)

    def run(self):
        self.processCamera()

    def putText(self, img, text, pos, ix, iy, font, color, scale, thickness, rect = 1):
        textSize = cv2.getTextSize(text, font, scale, thickness)
        if rect:
            cv2.rectangle(img, pos, (textSize[0][0] + ix,
                        pos[1] - textSize[0][1] + iy), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, text, (pos[0], pos[1] + iy),
                font, scale, color, thickness)

    def recognizeUser(self, img, faceRec):
        faces, out = faceRec.recognize(img)
        userID = -1
        bookID = -1
        for face in faces:
            if len(faces) > 1:
                text = 'No more than one person at a time'
                self.putText(img, text, (0,30), 0, -5, cv2.FONT_HERSHEY_SIMPLEX,
                                            (22, 163, 245), 1, 2)

            if np.amax(out) > faceRec.threshold:
                userID = int(np.argmax(out) + 1)
                text = 'User #' + str(userID)
                self.putText(img, text, face[0], face[0][0], -5, cv2.FONT_HERSHEY_SIMPLEX,
                                            (22, 163, 245), 1, 2)
            else:
                text = 'Unknown'
                self.putText(img, text, face[0], face[0][0], -5, cv2.FONT_HERSHEY_SIMPLEX,
                                            (22, 163, 245), 1, 2)
            cv2.rectangle(img, face[0], face[1], (22, 163, 245), 2)
        return userID

    def processCamera(self):
        brArgs = dict(name='QR')
        self.bookRec = br.BookRecognizer.create(brArgs)
        print("init book recognizer")
        rdArgs = dict(name = 'DNNfr', rdXML = path+'face-reidentification-retail-0095.xml', rdWidth = 128, rdHeight = 128,
                  rdThreshold = 0.8, fdName = 'DNNfd', fdXML = path+'face-detection-retail-0004.xml', fdWidth = 300, fdHeight = 300,
                  fdThreshold = 0.9, lmName = 'DNNlm', lmXML = path+'landmarks-regression-retail-0009.xml',
                  lmWidth= 48, lmHeight= 48)
        self.faceRec = fr.FaceRecognizer.create(rdArgs)
        print("init face recognizer")
        self.cap = cv2.VideoCapture(0)
        print("open camera")
        self.recBook = False
        self.regUser = False

        while True:
            ret, img =  self.cap.read()
            if (img is None): break

            self.userID = self.recognizeUser(img, self.faceRec)
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qtImage = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                         QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qtImage)

            if(self.regUser):
                self.userID = self.faceRec.register(img)
                self.allID[self.userID] = self.newUserID
                self.regUser = False

            if(self.recBook):
                 self.bookID = recognizeBook(img)
                 self.recBook = False

            self.camera.emit(pixmap)
            self.returnUserID.emit(self.allID[self.userID])
            self.returnBookID.emit(0)

    def recognizeBook(img):
        data = self.bookRec.recognize(img)
        try:
            bID = int(data.split(' ')[0])
            return bID
        except ValueError:
            return -1

    def startRecBook(self, rec):
        self.recBook = True

    def registerUser(self, ID):
        self.newUserID = ID
        self.regUser = True

    def stop(self):
        self.exit()
        self.cap.release()
        print("cap released")
        print("thread stopped")

class Execution(QMainWindow):

    CSV = CSVDatabase()
    userID = 1
    bookID = -1
    regID = -1
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.signIn = SignInWindow()
        self.signIn.show()
        self.libraryWin = MainWindow()

        self.signIn.btnSignIn.clicked.connect(self.enterLib)
        self.signIn.btnAccept.clicked.connect(self.registerUser)
        self.libraryWin.btnExit.clicked.connect(self.exitLib)

        self.image = QPixmap()
        self.thread = Thread()

        self.thread.camera.connect(self.showWebCameraOnSignIn)
        self.thread.returnUserID.connect(self.getUserID)
        self.thread.returnBookID.connect(self.getBookID)

        self.thread.start()
        print("thread started")
        self.signCloseEvent = self.signIn.closeEvent
        self.mainCloseEvent = self.libraryWin.closeEvent
        self.signIn.closeEvent = self.closeEvent


    def enterLib(self):
        self.signIn.closeEvent = self.signCloseEvent
        self.libraryWin.closeEvent = self.closeEvent
        self.signIn.close()
        self.thread.camera.disconnect(self.showWebCameraOnSignIn)
        self.thread.camera.connect(self.showWebCameraOnMainWin)
        self.libraryWin.passID(0, UserTypes.Administrator)
        self.libraryWin.show()
        self.updateReaderTables()
        self.updateAdminTables()

    def exitLib(self):
        self.libraryWin.closeEvent =  self.mainCloseEvent
        self.signIn.closeEvent = self.closeEvent
        self.libraryWin.close()
        self.thread.camera.disconnect(self.showWebCameraOnMainWin)
        self.thread.camera.connect(self.showWebCameraOnSignIn)
        self.signIn.show()

    @pyqtSlot(QPixmap)
    def showWebCameraOnSignIn(self, image):
        self.image = image
        width = self.signIn.webcameraLabel.width()
        height = self.signIn.webcameraLabel.height()
        newImage = self.image.scaled(width, height,
                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # newImage.save("i.png", "PNG")
        self.signIn.webcameraLabel.setPixmap(newImage)
        self.signIn.update()

    @pyqtSlot(QPixmap)
    def showWebCameraOnMainWin(self, image):
        self.image = image
        width = self.libraryWin.webcameraLabel.width()
        height = self.libraryWin.webcameraLabel.height()
        newImage = self.image.scaled(width, height,
                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # newImage.save("i.png", "PNG")
        self.libraryWin.webcameraLabel.setPixmap(newImage)
        self.libraryWin.update()

    @pyqtSlot(int)
    def getUserID(self, ID):
        self.userID = ID
        self.signIn.enableBtnSignIn()
        self.signIn.enableBtnAccept()

    @pyqtSlot(int)
    def getBookID(self, ID):
         self.bookID = ID

    @pyqtSlot(int)
    def getRegisterID(self, ID):
        self.regID = ID

    def registerUser(self):
        fName = self.signIn.firstNameEdit.text()
        sName = self.signIn.secondNameEdit.text()
        mName = self.signIn.middleNameEdit.text()
        phone = self.signIn.phoneEdit.text()
        adminCode = self.signIn.adminCodeEdit.text()

        if(adminCode == "XyzYjm"):
            admin = 2
        else:
            admin = 1

        user = User(-1, phone, fName, sName, mName)
        user._print()
        ID = self.CSV.AddUser(user, admin)

        print("Result: ")
        if(ID == -1):
            print("This user is already registered")
        else:
            print("ID = ", ID)
            self.thread.registerUser(ID)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def borrowingHistory(self):
        BBook = self.CSV.GetBorrowedBooks()
        Book = BBook[0]
        DateB = BBook[1]
        DateR = BBook[2]
        User = BBook[3]
        for i in enumerate(DateB):
            rowPosition = self.libraryWin.tableBorrBooks.rowCount()
            self.libraryWin.tableBorrBooks.insertRow(rowPosition)
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 0, QTableWidgetItem(User[i[0]].user_id))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 1, QTableWidgetItem(Book[i[0]].book_id))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 2, QTableWidgetItem(User[i[0]].first_name))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 3, QTableWidgetItem(User[i[0]].last_name))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 4, QTableWidgetItem(User[i[0]].middle_name))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 5, QTableWidgetItem(User[i[0]].phone))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 6, QTableWidgetItem(Book[i[0]].title))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 7, QTableWidgetItem(DateB[i[0]]))
            self.libraryWin.tableBorrBooks.setItem(rowPosition, 8, QTableWidgetItem(DateR[i[0]]))
        self.libraryWin.tableBorrBooks.resizeColumnsToContents()

    def readers(self):
        User = self.CSV.GetAllUsers()
        for i in enumerate(User):
            rowPosition = self.libraryWin.tableReaders.rowCount()
            self.libraryWin.tableReaders.insertRow(rowPosition)
            self.libraryWin.tableReaders.setItem(rowPosition, 0, QTableWidgetItem(User[i[0]].user_id))
            self.libraryWin.tableReaders.setItem(rowPosition, 1, QTableWidgetItem(User[i[0]].phone))
            self.libraryWin.tableReaders.setItem(rowPosition, 2, QTableWidgetItem(User[i[0]].first_name))
            self.libraryWin.tableReaders.setItem(rowPosition, 3, QTableWidgetItem(User[i[0]].last_name))
            self.libraryWin.tableReaders.setItem(rowPosition, 4, QTableWidgetItem(User[i[0]].middle_name))
        self.libraryWin.tableReaders.resizeColumnsToContents()
    
    def borrowingHistoryOneUser(self):
        BBook = self.CSV.GetBorrowedBooks()
        Book = BBook[0]
        DateB = BBook[1]
        DateR = BBook[2]
        User = BBook[3]
        for i in enumerate(DateB):
            rowPosition = self.libraryWin.tableBorrowingHistory.rowCount()
            if(self.userID != int(User[i[0]].user_id)):
                continue
            self.libraryWin.tableBorrowingHistory.insertRow(rowPosition)
            authorsStr = "" # строка для размещения в ней ФИО авторов

            c = ", " # строка для разделения авторов
            for j in enumerate(Book[i[0]].authors):
                if (j[0] == len(Book[i[0]].authors) - 1):
                    c = ''
                authorsStr += (Book[i[0]].authors[j[0]].first_name + ' ' +
                            Book[i[0]].authors[j[0]].last_name + ' ' +
                            Book[i[0]].authors[j[0]].middle_name + c)

            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 0, QTableWidgetItem(Book[i[0]].book_id))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 1, QTableWidgetItem(authorsStr))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 2, QTableWidgetItem(Book[i[0]].title))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 3, QTableWidgetItem(Book[i[0]].publisher))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 4, QTableWidgetItem(Book[i[0]].year))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 5, QTableWidgetItem(DateB[i[0]]))
            self.libraryWin.tableBorrowingHistory.setItem(rowPosition, 6, QTableWidgetItem(DateR[i[0]]))
        self.libraryWin.tableBorrowingHistory.resizeColumnsToContents()

    def availabelBooks(self):
        Book = self.CSV.GetAllBooks()
        for i in enumerate(Book):
            rowPosition = self.libraryWin.tableAvailableBooks.rowCount()
            self.libraryWin.tableAvailableBooks.insertRow(rowPosition)
            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 0, QTableWidgetItem(Book[i[0]].book_id))
            authorsStr = "" # строка для размещения в ней ФИО авторов

            c = ", " # строка для разделения авторов
            for j in enumerate(Book[i[0]].authors):
                if (j[0] == len(Book[i[0]].authors) - 1):
                    c = ''
                authorsStr += (Book[i[0]].authors[j[0]].first_name + ' ' +
                            Book[i[0]].authors[j[0]].last_name + ' ' +
                            Book[i[0]].authors[j[0]].middle_name + c)

            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 1, QTableWidgetItem(authorsStr))
            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 2, QTableWidgetItem(Book[i[0]].title))
            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 3, QTableWidgetItem(Book[i[0]].publisher))
            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 4, QTableWidgetItem(Book[i[0]].year))
            self.libraryWin.tableAvailableBooks.setItem(rowPosition, 5, QTableWidgetItem(Book[i[0]].file_path))
        self.libraryWin.tableAvailableBooks.resizeColumnsToContents()

    def updateReaderTables(self):
        self.borrowingHistoryOneUser()
        self.availabelBooks()

    def updateAdminTables(self):
        self.readers()
        self.borrowingHistory()