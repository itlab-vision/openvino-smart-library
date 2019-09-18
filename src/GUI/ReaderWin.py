# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReaderWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1220, 682)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelHello = QtWidgets.QLabel(self.centralwidget)
        self.labelHello.setGeometry(QtCore.QRect(20, 20, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelHello.setFont(font)
        self.labelHello.setObjectName("labelHello")
        self.btnBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnBook.setGeometry(QtCore.QRect(30, 560, 291, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBook.sizePolicy().hasHeightForWidth())
        self.btnBook.setSizePolicy(sizePolicy)
        self.btnBook.setObjectName("btnBook")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(40, 90, 472, 354))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCamera.sizePolicy().hasHeightForWidth())
        self.labelCamera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelCamera.setFont(font)
        self.labelCamera.setText("")
        self.labelCamera.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.labelCamera.setObjectName("labelCamera")
        self.labelInfo2 = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo2.setGeometry(QtCore.QRect(40, 470, 481, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo2.setFont(font)
        self.labelInfo2.setObjectName("labelInfo2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(550, 20, 651, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableBooks1 = QtWidgets.QTableWidget(self.tab)
        self.tableBooks1.setGeometry(QtCore.QRect(0, 0, 651, 611))
        self.tableBooks1.setObjectName("tableBooks1")
        self.tableBooks1.setColumnCount(0)
        self.tableBooks1.setRowCount(0)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableBooks2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableBooks2.setGeometry(QtCore.QRect(0, 0, 651, 601))
        self.tableBooks2.setObjectName("tableBooks2")
        self.tableBooks2.setColumnCount(0)
        self.tableBooks2.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reader"))
        self.labelHello.setText(_translate("MainWindow", "Welcome,"))
        self.btnBook.setText(_translate("MainWindow", "Get or return a book"))
        self.labelInfo2.setText(_translate("MainWindow", "Place the book in the selected area"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Borrowed books"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Books taken before"))
