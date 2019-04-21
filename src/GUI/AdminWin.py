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
        MainWindow.resize(1280, 681)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(550, 90, 711, 561))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.labelInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo.setGeometry(QtCore.QRect(560, 20, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo.setFont(font)
        self.labelInfo.setObjectName("labelInfo")
        self.labelHello = QtWidgets.QLabel(self.centralwidget)
        self.labelHello.setGeometry(QtCore.QRect(20, 20, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelHello.setFont(font)
        self.labelHello.setObjectName("labelHello")
        self.btnAddBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnAddBook.setGeometry(QtCore.QRect(260, 580, 221, 61))
        self.btnAddBook.setObjectName("btnAddBook")
        self.btnBook = QtWidgets.QPushButton(self.centralwidget)
        self.btnBook.setGeometry(QtCore.QRect(20, 580, 221, 61))
        self.btnBook.setObjectName("btnBook")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(20, 90, 472, 354))
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
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(770, 30, 211, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.labelInfo2 = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo2.setGeometry(QtCore.QRect(20, 470, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelInfo2.setFont(font)
        self.labelInfo2.setObjectName("labelInfo2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Administrator"))
        self.labelInfo.setText(_translate("MainWindow", "Get information about"))
        self.labelHello.setText(_translate("MainWindow", "Welcome, "))
        self.btnAddBook.setText(_translate("MainWindow", "Add a new book"))
        self.btnBook.setText(_translate("MainWindow", "Get or return a book"))
        self.comboBox.setItemText(0, _translate("MainWindow", "books"))
        self.comboBox.setItemText(1, _translate("MainWindow", "readers"))
        self.comboBox.setItemText(2, _translate("MainWindow", "borrowed books"))
        self.labelInfo2.setText(_translate("MainWindow", "Place the book in the selected area"))

