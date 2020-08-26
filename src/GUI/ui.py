import sys
import enum
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# sys.path.insert(0, "src/infrastructure")
# from CSVDatabase import *
# from Entities.User import *
# from Entities.Book import *
import resources

unknownID = -1
class StyleHelper():
    @staticmethod
    def getWindowStyleSheet():
        return ("background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 rgba(16, 23, 38, 255), stop:1 rgba(24, 54, 83, 255));"
                "border-style: outset;"
                "border-width: 1px;"
                "border-color: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0 rgba(16, 23, 38, 255), stop:1 rgba(24, 54, 83, 255));")
                # "padding-left: 10px; padding-right: 10px; padding-top: 10px; padding-bottom: 10px;")

    @staticmethod
    def getTitleStyleSheet():
        return ("background-color: rgba(0,0,0,0);"
                "border: none;")
    @staticmethod
    def getLabelStyleSheet(fontSize):
        return ("color: white;"
                "background-color:  none;"
                "border: none;"
                # "padding-left: 10px; padding-right: 10px; padding-top: 1px; padding-bottom: 1px;"
                "font: " + str(fontSize) + "px 'Verdana';")

    @staticmethod
    def getPixmapStyleSheet():
        return ("background-color: none;"
                "border-style: solid;"
                "border-width: 4px;"
                "border-color: rgba(69, 90, 128, 100);")

    @staticmethod
    def getButtonStyleSheet(fontSize):
        return ("QPushButton {"
                "color: white;"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 #455a80);"
                "border: none;"
                "padding-left: 10px; padding-right: 10px; padding-top: 1px; padding-bottom: 1px;"
                "font: " + str(fontSize) + "px'Verdana';"
                "text-align:left 10px;"
                "border-top-left-radius: 5px;"
                "border-top-right-radius: 5px;"
                "border-bottom-left-radius: 5px;"
                "border-bottom-right-radius: 5px;"
                "}"
                "QPushButton:hover {"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(114,150,214,250));"
                "}"
                "QPushButton:disabled {"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(35, 39, 45, 250));"
                "color: lightgray;"
                "}")

    @staticmethod
    def getTextButtonStyleSheet(fontSize):
        return ("QPushButton {"
                "color: rgb(168, 172, 155);"
                "background-color: transparent;"
                "border: none;"
                # "padding-left: 10px; padding-right: 10px; padding-top: 1px; padding-bottom: 1px;"
                "font: " + str(fontSize) + "px'Verdana';"
                "}"
                "QPushButton:hover {"
                "color: white;"
                "}")

    @staticmethod
    def getCloseStyleSheet():
        return  ("QToolButton { "
                 "image: url(:/xclose.png);"
                 "background-color: none; "
                 "border: none;"
                 "}"
                 "QToolButton:hover {"
                 "image: url(:/xclose_light.png); "
                 "}")

    @staticmethod
    def getMinimizeStyleSheet():
        return ("QToolButton { "
                "image: url(:/dash.png);"
                "background-color: none; "
                "border: none;"
                "}"
                "QToolButton:hover {"
                "image: url(:/dash_light.png); "
                "}")

    @staticmethod
    def getLineEditStyleSheet():
        return ("color: white;"
                "background-color: rgba(0, 0, 0, 0);"
                "border-style: solid;"
                "border-color: rgba(125, 133, 148, 140);"
                "border-width: 1px;"
                "font: 12px 'Verdana';")

    @staticmethod
    def getTabWidgetStyleSheet():
        return ("QTabWidget {border: none;}"
                "QTabWidget::pane {"
                "background-color: transparent;"
                "border-style: solid;"
                "border-width: 1px;"
                "border-color: rgba(69, 90, 128, 100);"
                "}"
                "QTabWidget::tab-bar {"
                "alignment: center;"
                "background-color: transparent;"
                "}"
                "QTabBar::tab {"
                "color: white;"
                "font: 12px 'Verdana';"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 #455a80);"
                "border-style: solid;"
                "border-color: rgba(125, 133, 148, 140);"
                "border-width: 1px;"
                "margin-left: 3px;"
                "margin-right: 3px;"
                "border-top-left-radius: 5px;"
                "border-top-right-radius: 5px;"
                "border-bottom-left-radius: 5px;"
                "border-bottom-right-radius: 5px;"
                "padding: 9px;"
                "min-width: 130px"
                # "max-width: 400 px"
                #"width: 200px; }"
                "} "
                "QTabBar::tab:hover {"
                #"text-decoration: underline;"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(59,150,214,250));"
                "}"
                "QTabBar::tab:selected {"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(59,150,214,250));"#qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(114,150,214,250));"
                "padding: 10px;"
                "margin-bottom: -2px;"
                "}"
                )
                # "QTabWidget::pane {"
                # "background-color: rgba(0, 0, 0, 0);"
                # "border-style: solid;"
                # "border-width: 4px;"
                # "border-color: rgba(69, 90, 128, 160);"
                # # # "border-style: solid;"
                # # "border-width: 0px;"
                # # "border-color: rgba(69, 90, 128, 100);"
                # # "top:-1px;"
                # "}"
                # # "QTabBar {"
                # # "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(59,150,214,250));"
                # # "width: 256px;"
                # # "border: none;"
                # # "}"

                # "QTabBar::tab:selected {"
                # "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0 #687080, stop:0.85 rgba(114,150,214,250));"
                # "padding: 10px;"
                # "margin-bottom: -1px;"
                # "}")

    @staticmethod
    def getTableStyleSheet():
        return ("QTableWidget {background-color: transparent; border: none; color: white; gridline-color: transparent;}"
                "QHeaderView::section {"
                "color: white;"
                "background-color: transparent;"
                "font: 12px 'Verdana';"
                "}"
                "QHeaderView {background-color: transparent;}"
                "QTableCornerButton::section {background-color: transparent;}"
                "QScrollBar:horizontal {"
                "    border: 1px solid rgb(32, 47, 130);"
                "    background-color: light grey;"
                "    height:12px;"
                "    margin: 0px 0px 0px 0px;"
                "}"
                "QScrollBar::handle:horizontal {"
                "    background: rgba(59,150,214, 160);"
                "    border-top-left-radius: 3px;"
                "    border-top-right-radius: 3px;"
                "    border-bottom-left-radius: 3px;"
                "    border-bottom-right-radius: 3px;"
                "    width: 100px;"
                "    min-height: 0px;"
                "}"
                "QScrollBar::add-line:horizontal {"
                "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
                "    height: 0px;"
                "    subcontrol-position: bottom;"
                "    subcontrol-origin: margin;"
                "}"
                "QScrollBar::sub-line:horizontal {"
                "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                "    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
                "    height: 0 px;"
                "    subcontrol-position: top;"
                "    subcontrol-origin: margin;"
                "}")
        # QScrollBar:horizontal {"
        #         "border: 1px solid #999999;"
        #         "background:black;"
        #         "width:10px;    "
        #         "margin: 10px 10px 10px 10px;"
        #         "}")
                # "QScrollBar::handle:horizontal {"
                # "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                # "stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));"
                # "min-height: 0px;"
                # "}"
                # "QScrollBar::add-line:horizontal  {"
                # "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                # "stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
                # "height: 0px;"
                # "subcontrol-position: bottom;"
                # "subcontrol-origin: margin;"
                # "}"
                # "QScrollBar::sub-line:horizontal  {"
                # " background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
                # "stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
                # "height: 0 px;"
                # "subcontrol-position: top;"
                # " subcontrol-origin: margin;"
                # "}")
    @staticmethod
    def getSplitterStyleSheet():
        return ("QSplitter {background: transparent; border: none;}"
                "QSplitterHandle:hover {}"
                "QSplitter::handle:horizontal:hover {"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0.15 rgba(59,150,214, 0), stop:0.5 rgba(59,150,214, 200), stop:0.85 rgba(59,150,214,0));"
                "}"
               "QSplitter::handle:pressed{"
                "background-color: qlineargradient( spread:pad, x1:0 y1:0, x2:0 y2:1, stop:0.15 rgba(59,150,214, 0), stop:0.5 rgba(59,150,214, 200), stop:0.85 rgba(59,150,214,0));"
                "width: 10px;"
               "height: 500px;"
               "}")

class EventsButton(QToolButton):
    def __init__(self, mainSize, styleSheet, parent= None):
        super(EventsButton, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumSize(25, 25)
        self.setMaximumSize(35, 35)
        self.setStyleSheet(styleSheet)

class TextButton(QPushButton):
    def __init__(self, text = "", parent = None):
        super(TextButton, self).__init__(parent)

        fontSize = 14
        font = QFont("Verdana", fontSize)
        fm = QFontMetrics(font)

        width = fm.width(text)
        height = fm.height()
        print(width, height)
        scaleFactor = QDesktopWidget().availableGeometry().width()/1920 - 0.05
        self.setMinimumSize(width , height)
        self.setMaximumSize(width+10, height+10)
        self.setText(text)
        self.setStyleSheet(StyleHelper().getTextButtonStyleSheet(int(fontSize*scaleFactor)))

class PlainButton(QPushButton):
    def __init__(self,  mainSize, text = "", maxHeight = 0, parent = None):
        super(PlainButton, self).__init__(parent)
        if(maxHeight == 0):
            maxHeight = mainSize.height()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumSize(mainSize.width()*0.3, maxHeight*0.05)
        self.setMaximumSize(mainSize.width()*0.35, maxHeight*0.05)
        self.setText(text)
        fontSize = 14
        scaleFactor = QDesktopWidget().availableGeometry().width()/1920 - 0.05
        print(fontSize*scaleFactor)
        self.setStyleSheet(StyleHelper().getButtonStyleSheet(int(fontSize*scaleFactor)))

class WebcamPixmap(QLabel):
    aspectRatio = 0
    def __init__(self, mainSize, parent= None):
        super(WebcamPixmap, self).__init__(parent)
        # self.setFixedSize(mainSize.width()*0.95, mainSize.height()*0.47)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # policy.setHeightForWidth(True)
        self.setScaledContents(True)
        self.image = QPixmap(":/cap.png")
        self.aspectRatio = 3/4 #self.image.height() / self.image.width()
        self.setSizePolicy(policy)
        self.setMinimumSize(mainSize.width()*0.2, mainSize.width()*self.aspectRatio*0.2)
        self.setMaximumSize(mainSize.width(), mainSize.width()*self.aspectRatio)
        self.setStyleSheet(StyleHelper().getPixmapStyleSheet())
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setPixmap(self.image.scaled(self.width(),self.height(),
                      Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        if(self.height() / self.width() > self.aspectRatio ):
            self.resize(self.width(), self.width()*self.aspectRatio)
        else:
            self.resize(self.height() / self.aspectRatio, self.height())
    

        # self.setPixmap(self.pixmap().scaled(self.width(),self.height(),
        #               Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.setPixmap(self.image.scaled(
        #     self.width(), self.height(),
        #     Qt.KeepAspectRatio,  Qt.SmoothTransformation))

    # def hasHeightForWidth(self):
    #     return True

    # def heightForWidth(self, width):
    #     return width*9/16

        # rgbImage = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
        # convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
        #                                  QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(convertToQtFormat)
        # resizeImage = pixmap.scaled(472, 354, Qt.KeepAspectRatio)

class TitleLabel(QLabel):
    def __init__(self, mainSize, parent= None):
        super(TitleLabel, self).__init__(parent)
        #self.setFixedSize(mainSize.width()*0.35, mainSize.height()*0.05)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.resize(mainSize.width()*0.35, mainSize.height()*0.05)
        self.image = QPixmap(":/title.png")
        self.setPixmap(self.image.scaled(self.width(),self.height(),
                        Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setStyleSheet(StyleHelper().getTitleStyleSheet())

class TextLabel(QLabel):
    def __init__(self, fontSize = 12, text = "", parent = None):
        super(TextLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setText(text)
        scaleFactor = QDesktopWidget().availableGeometry().width()/1920
        print(scaleFactor)
        self.setStyleSheet(StyleHelper().getLabelStyleSheet(int(fontSize*scaleFactor)))

class LineEdit(QLineEdit):
    def __init__(self, parent = None):
        super(LineEdit, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setStyleSheet(StyleHelper().getLineEditStyleSheet())

class Tab(QTabWidget):
    def __init__(self, mainSize, parent = None):
        super(Tab, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(mainSize.width()*0.5,mainSize.height()*0.5)
        desctopWidth = QDesktopWidget().availableGeometry().width()
        desctopHeight= QDesktopWidget().availableGeometry().height()
        self.setMaximumSize(desctopWidth*0.8, desctopHeight)
        self.setElideMode(Qt.ElideNone)
        self.setStyleSheet(StyleHelper().getTabWidgetStyleSheet())

class Table(QTableWidget):
    def __init__(self, colsHeaders,  parent = None):
        super(Table, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalHeader().hide()
        self.setColumnCount(len(colsHeaders))
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(colsHeaders)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        if(self.columnCount() > 5):
            self.horizontalHeader().setSectionResizeMode(self.columnCount()-1, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setSectionResizeMode(self.columnCount()-1, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setStretchLastSection(True)
        # self.resizeColumnsToContents()
        self.setShowGrid(False)
        self.setStyleSheet(StyleHelper().getTableStyleSheet())

    # def resizeEvent(self, event):
    #     print("resize table",self.width(), self.columnCount(), self.width()/self.columnCount())
    #     for i in range(self.columnCount()):
    #         print(i)
    #         self.setColumnWidth(i, self.width()/self.columnCount())

class UserTypes(enum.Enum):
    Reader = 1
    Administrator = 2

class MouseTypes(enum.Enum):
    Other = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    Move = 5
# ----------------------------------------------------------------------------------------------------------------------------

class SignInWindow(QMainWindow):
    userID = -1
    Role = UserTypes.Reader

    def __init__(self):
        super().__init__()
        self.initUI()

    def setLayouts(self):
        #interface widget layout
        self.interfaceWidget.setLayout(QVBoxLayout())
        self.interfaceWidget.layout().addWidget(self.MainWidget)
        #layouts
        headerWV = QVBoxLayout()
        controlWH = QHBoxLayout()
        titleWH = QHBoxLayout()
        cameraWH = QHBoxLayout()
        self.signInWH = QHBoxLayout()
        self.verticalSignIn = QVBoxLayout()
        self.inputInfo = QFormLayout()
        self.signUpWH = QHBoxLayout()
        self.verticalSignUp = QVBoxLayout()
        self.verticalWidgets = QVBoxLayout()

        # add widgets to layout
        controlWH.addWidget(self.titleText)
        controlWH.addStretch(1)
        controlWH.addWidget(self.btnMinimize)
        controlWH.addWidget(self.btnClose)

        headerWV.addLayout(controlWH)
        titleWH.addStretch(1)
        titleWH.addWidget(self.title)
        headerWV.addLayout(titleWH)
        cameraWH.addWidget(self.webcameraLabel)

        self.signInWH.addStretch(1)
        self.signInWH.addWidget(self.btnSignIn)
        self.signInWH.addWidget(self.btnSignUp)
        self.verticalSignIn.addStretch(1)
        self.verticalSignIn.addLayout(self.signInWH)

        self.signInWidget = QWidget()
        self.signInWidget.setStyleSheet("background-color: none; border: none;")
        self.signInWidget.setLayout(self.verticalSignIn)

        self.inputInfo.addRow(self.secondNameLabel, self.secondNameEdit)
        self.inputInfo.addRow(self.firstNameLabel, self.firstNameEdit)
        self.inputInfo.addRow(self.middleNameLabel, self.middleNameEdit)
        self.inputInfo.addRow(self.phoneLabel, self.phoneEdit)
        self.inputInfo.addRow(self.adminCodeLabel, self.adminCodeEdit)

        self.signUpWH.addStretch(1)
        self.signUpWH.addWidget(self.btnAccept)
        self.signUpWH.addWidget(self.btnBack)
        self.signUpWidget = QWidget()
        self.signUpWidget.setStyleSheet("background-color: none; border: none;")

        self.verticalSignUp.addLayout(self.inputInfo)
        self.verticalSignUp.addWidget(self.infoLabel)
        self.verticalSignUp.addStretch(1)
        self.verticalSignUp.addLayout(self.signUpWH)
        self.signUpWidget.setLayout(self.verticalSignUp)

        self.btnLayout = QStackedLayout()
        self.btnLayout.addWidget(self.signInWidget)
        self.btnLayout.addWidget(self.signUpWidget)
        self.btnLayout.setCurrentIndex(0)

        self.verticalWidgets.addLayout(headerWV)
        self.verticalWidgets.addLayout(cameraWH)
        self.verticalWidgets.addLayout(self.btnLayout)
        self.verticalWidgets.setContentsMargins(10, 10, 10, 20)
        self.MainWidget.setLayout(self.verticalWidgets)

    def initUI(self):

        print("init ui")
        # flags & attributes
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # geometry
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        desctopWidth = QDesktopWidget().availableGeometry().width()
        desctopHeight= QDesktopWidget().availableGeometry().height()
        self.resize(desctopWidth // 3.8, desctopHeight / 1.5)
        self.center()

        # general widgets
        self.MainWidget =  QWidget()
        self.interfaceWidget =  QWidget()
        self.signInWidget =  QWidget()
        self.signUpWidget =  QWidget()

        # interface widgets
        self.title = TitleLabel(self.size()) # work with Qt-Resourse-File
        self.btnClose = EventsButton(self.size(), StyleHelper().getCloseStyleSheet())
        self.btnMinimize = EventsButton(self.size(), StyleHelper().getMinimizeStyleSheet(),)
        self.webcameraLabel = WebcamPixmap(self.size(),
                                          StyleHelper().getPixmapStyleSheet())

        # signup dialogs
        self.secondNameLabel = TextLabel(15, "Фамилия*")
        self.secondNameEdit = LineEdit()

        self.firstNameLabel = TextLabel(15, "Имя*")
        self.firstNameEdit  = LineEdit()

        self.middleNameLabel = TextLabel(15, "Отчество*")
        self.middleNameEdit  = LineEdit()

        self.phoneLabel = TextLabel(15, "Телефон*")
        self.phoneEdit  = LineEdit()

        self.adminCodeLabel = TextLabel(15, "Код администратора")
        self.adminCodeEdit = LineEdit()
        self.adminCodeEdit.setEchoMode(QLineEdit.Password)
        self.infoLabel = TextLabel(10, "* - обязательно")

        # push buttons for sign in and sign up
        self.btnSignIn = PlainButton(self.size(), "ВОЙТИ")
        self.btnSignUp = PlainButton(self.size(), "СОЗДАТЬ АККАУНТ")
        self.btnAccept = PlainButton(self.size(), "ПРИНЯТЬ")
        self.btnBack = PlainButton(self.size(), "НАЗАД")
        self.titleText = TextLabel(15, "Вход в Smart Library")

        #style and effects
        self.shadowEffect = QGraphicsDropShadowEffect()
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setColor(QColor(0, 0, 0, 190))
        self.shadowEffect.setOffset(0)
        self.MainWidget.setStyleSheet(StyleHelper().getWindowStyleSheet())
        self.MainWidget.setGraphicsEffect(self.shadowEffect)

        # apply layouts to widgets
        self.setLayouts()
        self.setCentralWidget(self.interfaceWidget)

        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnSignUp.clicked.connect(self.showSignUp)
        self.btnBack.clicked.connect(self.showSignIn)
        self.mousePos = self.pos()
        print("end init ui")

    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.mousePos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.mousePos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.mousePos = event.globalPos()

    def closeEvent(self, event):
            event.accept()

    def showSignUp(self, event):
        self.btnLayout.setCurrentIndex(1)

    def showSignIn(self, event):
        self.btnLayout.setCurrentIndex(0)

    def enableBtnSignIn(self):
        if(self.userID != unknownID):
            self.btnSignIn.setEnabled(True)
        else:
            print(self.userID)
            self.btnSignIn.setEnabled(False)

    def enableBtnAccept(self):
        if(len(self.firstNameEdit.text()) > 0 and
           len(self.secondNameEdit.text()) > 0 and
            len(self.middleNameEdit.text()) > 0 and
            len(self.phoneEdit.text()) > 0 and
            self.userID == unknownID):
            self.btnAccept.setEnabled(True)
        else:
            self.btnAccept.setEnabled(False)

class MainWindow(QMainWindow):
    userID = -1
    bookID = -1
    mousePos = QPoint()
    mouseBtnPressed = MouseTypes.Other

    def __init__(self):
        super().__init__()
        self.initUI()

    def setLayouts(self):
        # interface widget layout
        self.interfaceWidget.setLayout(QVBoxLayout())
        self.interfaceWidget.layout().addWidget(self.MainWidget)

        # layouts
        controlWH = QHBoxLayout()
        buttonsWH = QHBoxLayout()
        leftH = QHBoxLayout()
        leftV = QVBoxLayout()
        table1Layout = QVBoxLayout()
        table2Layout = QVBoxLayout()
        table3Layout = QVBoxLayout()
        table4Layout = QVBoxLayout()
        table5Layout = QVBoxLayout()
        self.verticalWidgets = QVBoxLayout()

        # splitter
        bodyWH = QSplitter(Qt.Horizontal)
        bodyWH.setStyleSheet(StyleHelper.getSplitterStyleSheet())

        # reader
        table1Layout.addWidget(self.tableBorrowingHistory)
        table2Layout.addWidget(self.tableAvailableBooks)
        self.tabR1.setLayout(table1Layout)
        self.tabR2.setLayout(table2Layout)

        self.tabReaderWidget.addTab(self.tabR1, "ИСТОРИЯ")
        self.tabReaderWidget.addTab(self.tabR2, "ДОСТУПНЫЕ КНИГИ")

        # admin
        table3Layout.addWidget(self.tableBorrBooks)
        table4Layout.addWidget(self.tableBooks)
        table5Layout.addWidget(self.tableReaders)

        self.tabA1.setLayout(table3Layout)
        self.tabA2.setLayout(table4Layout)
        self.tabA3.setLayout(table5Layout)

        self.tabAdminWidget.addTab(self.tabA1, "ВЗЯТЫЕ КНИГИ")
        self.tabAdminWidget.addTab(self.tabA2, "КНИГИ")
        self.tabAdminWidget.addTab(self.tabA3, "ЧИТАТЕЛИ")

        # splitter left and right widgets
        self.left = QWidget()
        self.left.setStyleSheet("background-color: transparent; border: none;")
        self.right = QWidget()
        self.right.setStyleSheet("background-color: transparent; border: none;")

        self.adminReaderLayout = QStackedLayout()
        self.adminReaderLayout.addWidget(self.tabReaderWidget)
        self.adminReaderLayout.addWidget(self.tabAdminWidget)
        self.adminReaderLayout.setCurrentIndex(0)
        self.right.setLayout(self.adminReaderLayout)

        # add widgets to layout
        controlWH.addWidget(self.title)
        controlWH.addStretch(1)
        controlWH.addWidget(self.btnMinimize)
        controlWH.addWidget(self.btnClose)

        leftH.addWidget(self.btnExit)
        leftH.addWidget(self.btnStat)
        leftH.addStretch(1)
        leftV.addLayout(leftH)
        leftV.addWidget(self.webcameraLabel)
        self.left.setLayout(leftV)


        bodyWH.addWidget(self.left)
        bodyWH.addWidget(self.right)
        bodyWH.setCollapsible(0, False)
        bodyWH.setCollapsible(1, False)
        bodyWH.setStretchFactor(0,1)
        bodyWH.setStretchFactor(1,5)

        buttonsWH.addWidget(self.btnGetRetBook)
        buttonsWH.addWidget(self.btnAddBook)

        self.verticalWidgets.addLayout(controlWH)
        self.verticalWidgets.addWidget(bodyWH)
        self.verticalWidgets.addLayout(buttonsWH)
        self.verticalWidgets.setContentsMargins(10, 10, 10, 20)
        self.MainWidget.setLayout(self.verticalWidgets)


    def initUI(self):
        # flags & attributes
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        # geometry
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        desctopWidth = QDesktopWidget().availableGeometry().width()
        desctopHeight= QDesktopWidget().availableGeometry().height()
        self.setMinimumSize(desctopWidth / 2, desctopHeight / 2)
        self.setMaximumSize(desctopWidth , desctopHeight )
        self.resize(desctopWidth / 1.7, desctopHeight / 1.3)
        self.center()

        # general widgets
        self.MainWidget =  QWidget()
        self.MainWidget.setMouseTracking(True)
        self.interfaceWidget =  QWidget()
        self.AdminWidget =  QWidget()
        self.ReaderWidget =  QWidget()

        # interface widgets
        self.title = TitleLabel(self.size()) # work with Qt-Resourse-File
        self.btnClose = EventsButton(self.size(), StyleHelper().getCloseStyleSheet())
        self.btnMinimize = EventsButton(self.size(), StyleHelper().getMinimizeStyleSheet())
        self.webcameraLabel = WebcamPixmap(self.size(),
                                          StyleHelper().getPixmapStyleSheet())

        # admin tab with tables
        self.tabAdminWidget = Tab(self.size())
        self.tabA1 = QWidget()
        self.tabA2 = QWidget()
        self.tabA3 = QWidget()

        # reader tab with tables
        self.tabReaderWidget = Tab(self.size())
        self.tabR1 = QWidget()
        self.tabR2 = QWidget()

        # table with borrowing history
        self.tableBorrowingHistory  = Table(["ID", "Автор", "Название",
                                                    "Издатель", "Дата публикации","Взято",
                                                     "Возвращено"])
        # self.tableBorrowingHistory.verticalHeader().hide()

        # table with books for readers
        self.tableAvailableBooks = Table(["ID", "Автор", "Название",
                                                    "Издатель", "Дата публикации"])

        # table with borrowed books
        self.tableBorrBooks = Table(["User ID", "Book ID", "Фамилия", "Имя",
                                                     "Отчество", "Телефон", "Название", "Взято",
                                                     "Возвращено"])


        # table with all books
        self.tableBooks = Table(["ID", "Автор", "Название",
                                                    "Издатель", "Дата публикации"])

        # table with readers
        self.tableReaders = Table(["ID", "Фамилия", "Имя",
                                                     "Отчество", "Телефон"])

        #buttons
        self.btnExit = TextButton("Выход")
        self.btnBack = TextButton("Назад")
        self.btnStat = TextButton("Статистика")
        self.btnStat.hide()
        self.btnGetRetBook = PlainButton(self.size(), "Распознать книгу")
        self.btnAddBook = PlainButton(self.size(), "Добавить книгу")

        #style and effects
        self.shadowEffect = QGraphicsDropShadowEffect()
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setColor(QColor(0, 0, 0, 190))
        self.shadowEffect.setOffset(0)
        self.MainWidget.setStyleSheet(StyleHelper().getWindowStyleSheet())
        self.MainWidget.setGraphicsEffect(self.shadowEffect)

        # apply layouts to widgets
        self.setLayouts()
        self.setCentralWidget(self.interfaceWidget)
        self.centralWidget().setMouseTracking(True)

        # self.btnStat.hide()
        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnStat.clicked.connect(self.showAdminInfo)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def checkResizableField(self, event):
        pos = event.globalPos()
        x = self.x()
        y = self.y()
        width = self.width()
        height = self.height()

        # define rectangles for resize
        rectTop = QRect(x+9, y, width - 18, 7)
        rectBottom = QRect(x+9, y+height-7, width -18, 7)
        rectLeft = QRect(x, y+9, 7 , height - 18)
        rectRight = QRect(x+width-7, y+ 9, 7, height -18)
        rectInterface = QRect(x+9, y+9, width - 18, height -18)
        # print(event.globalPos(), x, y )

        if(rectTop.contains(pos)):
            self.setCursor(Qt.SizeVerCursor)
            return MouseTypes.Top
        elif(rectBottom.contains(pos)):
            self.setCursor(Qt.SizeVerCursor)
            return MouseTypes.Bottom
        elif(rectLeft.contains(pos)):
            self.setCursor(Qt.SizeHorCursor)
            return MouseTypes.Left
        elif(rectRight.contains(pos)):
            self.setCursor(Qt.SizeHorCursor)
            return MouseTypes.Right
        elif(rectInterface.contains(pos)):
            self.setCursor(QCursor())
            return MouseTypes.Move
        else:
            self.setCursor(QCursor())
            return MouseTypes.Other

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton ):
            self.mouseBtnPressed = self.checkResizableField(event)
            self.mousePos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.mouseBtnPressed  =  MouseTypes.Other

    def mouseMoveEvent(self, event):
        # print(event.globalPos())
        delta = QPoint (event.globalPos() - self.mousePos)
        if (self.mouseBtnPressed == MouseTypes.Move):
            self.move(self.x() + delta.x(),self.y() + delta.y())
        elif (self.mouseBtnPressed == MouseTypes.Bottom ):
            self.setGeometry(self.x(), self.y(),
                        self.width(), self.height() + delta.y())
        elif (self.mouseBtnPressed == MouseTypes.Top
             and self.minimumHeight() <= self.height() - delta.y() <= self.maximumHeight()):
            self.setGeometry(self.x(), self.y() + delta.y(),
                       self.width(), self.height() - delta.y())
        elif (self.mouseBtnPressed == MouseTypes.Left
              and self.minimumWidth() <= self.width() - delta.x() <= self.maximumWidth()):
            self.setGeometry(self.x() + delta.x(), self.y(),
                        self.width() - delta.x(),self.height())
        elif (self.mouseBtnPressed == MouseTypes.Right):
            self.setGeometry(self.x(), self.y(),
                        self.width() + delta.x(), self.height())
        else:
            self.checkResizableField(event)
        self.mousePos = event.globalPos()

    def passID(self, ID, role):
        self.userID = ID
        print("lib win id " ,  self.userID)
        if (role == UserTypes.Administrator):
            print("admin")
            self.btnStat.show()

    click = 0
    def showAdminInfo(self):
        self.adminReaderLayout.setCurrentIndex(self.click % 2)
        self.click  = self.click +1
        # rowPosition = self.tableBorrBooks.rowCount()
        # self.tableBorrBooks.insertRow(rowPosition)
        # self.tableBorrBooks.setItem(rowPosition, 0, QTableWidgetItem("1"))
        # self.tableBorrBooks.setItem(rowPosition, 1, QTableWidgetItem("1"))
        # self.tableBorrBooks.setItem(rowPosition, 2, QTableWidgetItem("1"))
        # self.tableBorrBooks.setItem(rowPosition, 3, QTableWidgetItem("1"))
        # self.tableBorrBooks.setItem(rowPosition, 4, QTableWidgetItem("1"))
        # self.tableBorrBooks.setItem(rowPosition, 5, QTableWidgetItem("1"))

class BookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.titleEdit.textChanged.connect(self.enableBtnAdd)
        self.authorEdit.textChanged.connect(self.enableBtnAdd)
        self.publisherEdit.textChanged.connect(self.enableBtnAdd)
        self.yearEdit.textChanged.connect(self.enableBtnAdd)
        self.btnAddBook.setEnabled(False)

    def setLayouts(self):
        #interface widget layout
        self.interfaceWidget.setLayout(QVBoxLayout())
        self.interfaceWidget.layout().addWidget(self.MainWidget)
        #layouts
        # headerWV = QVBoxLayout()
        controlWH = QHBoxLayout()
        # titleWH = QHBoxLayout()
        self.inputInfo = QFormLayout()
        self.verticalWidgets = QVBoxLayout()

        # add widgets to layout
        controlWH.addWidget(self.titleText)
        controlWH.addStretch(1)
        controlWH.addWidget(self.btnMinimize)
        controlWH.addWidget(self.btnClose)

        # headerWV.addLayout(controlWH)
        # titleWH.addStretch(1)
        # titleWH.addWidget(self.title)
        # # headerWV.addLayout(titleWH)


        self.inputInfo.addRow(self.titleLabel, self.titleEdit)
        self.inputInfo.addRow(self.authorLabel, self.authorEdit)
        self.inputInfo.addRow(self.publisherLabel, self.publisherEdit)
        self.inputInfo.addRow(self.yearLabel, self.yearEdit)

        self.btnLayout = QHBoxLayout()
        self.btnLayout.addWidget(self.btnAddBook)

        self.verticalWidgets.addLayout(controlWH)
        self.verticalWidgets.addLayout(self.inputInfo)
        self.verticalWidgets.addWidget(self.infoLabel)
        self.verticalWidgets.addLayout(self.btnLayout)
        self.verticalWidgets.setContentsMargins(10, 10, 10, 20)
        self.MainWidget.setLayout(self.verticalWidgets)

    def initUI(self):
        # flags & attributes
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # geometry
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        desctopWidth = QDesktopWidget().availableGeometry().width()
        desctopHeight= QDesktopWidget().availableGeometry().height()
        self.resize(desctopWidth // 4, desctopHeight // 3)
        self.center()

        # general widgets
        self.MainWidget =  QWidget()
        self.interfaceWidget =  QWidget()

        # interface widgets
        self.title = TitleLabel(self.size()) # work with Qt-Resourse-File
        self.btnClose = EventsButton(self.size(), StyleHelper().getCloseStyleSheet())
        self.btnMinimize = EventsButton(self.size(), StyleHelper().getMinimizeStyleSheet(),)

        # signup dialogs
        self.titleLabel = TextLabel(15, "Название*")
        self.titleEdit = LineEdit()

        self.authorLabel = TextLabel(15, "Автор*")
        self.authorEdit  = LineEdit()

        self.publisherLabel = TextLabel(15, "Издатель*")
        self.publisherEdit  = LineEdit()

        self.yearLabel = TextLabel(15, "Год*")
        self.yearEdit  = LineEdit()

        self.infoLabel = TextLabel(10, "* - обязательно")

        # push buttons for sign in and sign up
        self.btnAddBook = PlainButton(self.size(), "Добавить книгу", 600)
        self.titleText = TextLabel(15, "Добавление книги")

        #style and effects
        self.shadowEffect = QGraphicsDropShadowEffect()
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setColor(QColor(0, 0, 0, 190))
        self.shadowEffect.setOffset(0)
        self.MainWidget.setStyleSheet(StyleHelper().getWindowStyleSheet())
        self.MainWidget.setGraphicsEffect(self.shadowEffect)

        # apply layouts to widgets
        self.setLayouts()
        self.btnAddBook.resize(self.width()//3, self.height()//6)
        self.setCentralWidget(self.interfaceWidget)

        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.mousePos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.mousePos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.mousePos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.mousePos = event.globalPos()



    # def OpenFile(self):
    #     fileName = QFileDialog.getOpenFileName(self.labelPicture,
    #                                                  'Open File',"",
    #                                                  "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
    #     """Pixmap - показываем миниатюру картинки на экране загрузки
    #        self.Cover - сохраняем полную картинку, чтобы потом ее записать в нужную папку"""
    #     if(fileName[0] != ""):
    #         pixmap = QPixmap(fileName[0])
    #         self.Cover = pixmap
    #         pixmap = pixmap.scaled(self.labelPicture.width(),
    #                                self.labelPicture.height(),
    #                                QtCore.Qt.KeepAspectRatio)
    #         self.labelPicture.setPixmap(pixmap)
    #         self.EnableBtnAdd()
    #         print(self.labelPicture.pixmap())
    #         print("open")

    def enableBtnAdd(self):
        if(len(self.titleEdit.text()) > 0 and
           len(self.authorEdit.text()) > 0 and
           len(self.publisherEdit.text()) > 0 and
           len(self.yearEdit.text()) > 0):
             self.btnAddBook.setEnabled(True)
        else:
             self.btnAddBook.setEnabled(False)
