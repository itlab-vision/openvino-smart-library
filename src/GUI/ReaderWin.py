# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReaderWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 682)
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
        self.tableBooks = QtWidgets.QTableWidget(self.centralwidget)
        self.tableBooks.setGeometry(QtCore.QRect(560, 80, 701, 541))
        self.tableBooks.setObjectName("tableBooks")
        self.tableBooks.setColumnCount(0)
        self.tableBooks.setRowCount(0)
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
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(560, 30, 371, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reader"))
        self.labelHello.setText(_translate("MainWindow", "Welcome,"))
        self.btnBook.setText(_translate("MainWindow", "Get or return a book"))
        self.labelInfo2.setText(_translate("MainWindow", "Place the book in the selcted area"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Borrowed books"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Books taken before"))

