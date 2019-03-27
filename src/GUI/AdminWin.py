# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AdminWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(310, 20, 941, 571))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.btnInfoReaders = QtWidgets.QPushButton(self.centralwidget)
        self.btnInfoReaders.setGeometry(QtCore.QRect(550, 620, 221, 61))
        self.btnInfoReaders.setObjectName("btnInfoReaders")
        self.btnInfoBooks = QtWidgets.QPushButton(self.centralwidget)
        self.btnInfoBooks.setGeometry(QtCore.QRect(790, 620, 221, 61))
        self.btnInfoBooks.setObjectName("btnInfoBooks")
        self.btnInfoBBooks = QtWidgets.QPushButton(self.centralwidget)
        self.btnInfoBBooks.setGeometry(QtCore.QRect(1030, 620, 221, 61))
        self.btnInfoBBooks.setObjectName("btnInfoBBooks")
        self.labelInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo.setGeometry(QtCore.QRect(310, 620, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo.setFont(font)
        self.labelInfo.setObjectName("labelInfo")
        self.labelHello = QtWidgets.QLabel(self.centralwidget)
        self.labelHello.setGeometry(QtCore.QRect(30, 10, 271, 121))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelHello.setFont(font)
        self.labelHello.setObjectName("labelHello")
        self.btnAddBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddBook.setGeometry(QtCore.QRect(30, 280, 221, 61))
        self.btnAddBook.setObjectName("btnAddBook")
        self.btnBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnBook.setGeometry(QtCore.QRect(30, 190, 221, 61))
        self.btnBook.setObjectName("btnBook")
        self.table.raise_()
        self.labelInfo.raise_()
        self.labelHello.raise_()
        self.btnAddBook.raise_()
        self.btnBook.raise_()
        self.btnInfoReaders.raise_()
        self.btnInfoBBooks.raise_()
        self.btnInfoBooks.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Administrator"))
        self.btnInfoReaders.setText(_translate("MainWindow", "Readers"))
        self.btnInfoBooks.setText(_translate("MainWindow", "Books"))
        self.btnInfoBBooks.setText(_translate("MainWindow", "Borrowed books"))
        self.labelInfo.setText(_translate("MainWindow", "Get information about:"))
        self.labelHello.setText(_translate("MainWindow", "Welcome, "))
        self.btnAddBook.setText(_translate("MainWindow", "Add a new book"))
        self.btnBook.setText(_translate("MainWindow", "Get or return a book"))

