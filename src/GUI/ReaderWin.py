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
        MainWindow.resize(1280, 693)
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
        self.btnBook.setGeometry(QtCore.QRect(30, 590, 291, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBook.sizePolicy().hasHeightForWidth())
        self.btnBook.setSizePolicy(sizePolicy)
        self.btnBook.setObjectName("btnBook")
        self.tableBooks = QtWidgets.QTableWidget(self.centralwidget)
        self.tableBooks.setGeometry(QtCore.QRect(30, 110, 591, 451))
        self.tableBooks.setObjectName("tableBooks")
        self.tableBooks.setColumnCount(0)
        self.tableBooks.setRowCount(0)
        self.tableBooks2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableBooks2.setGeometry(QtCore.QRect(660, 110, 591, 451))
        self.tableBooks2.setObjectName("tableBooks2")
        self.tableBooks2.setColumnCount(0)
        self.tableBooks2.setRowCount(0)
        self.labelInfo2 = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo2.setGeometry(QtCore.QRect(660, 70, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo2.setFont(font)
        self.labelInfo2.setObjectName("labelInfo2")
        self.labelInfo1 = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo1.setGeometry(QtCore.QRect(30, 60, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo1.setFont(font)
        self.labelInfo1.setObjectName("labelInfo1")
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
        self.labelInfo2.setText(_translate("MainWindow", "Books you had taken before"))
        self.labelInfo1.setText(_translate("MainWindow", "Borrowed books"))

