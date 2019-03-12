# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BookWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(736, 413)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 61, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 150, 68, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 200, 101, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 250, 131, 31))
        self.label_5.setObjectName("label_5")
        self.lineEdit_title = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_title.setGeometry(QtCore.QRect(140, 100, 221, 25))
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.lineEdit_author = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_author.setGeometry(QtCore.QRect(140, 150, 221, 25))
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.lineEdit_publisher = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_publisher.setGeometry(QtCore.QRect(140, 200, 221, 25))
        self.lineEdit_publisher.setObjectName("lineEdit_publisher")
        self.lineEdit_date = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_date.setGeometry(QtCore.QRect(160, 250, 201, 25))
        self.lineEdit_date.setObjectName("lineEdit_date")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(20, 320, 201, 51))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 340, 210, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_pix = QtWidgets.QLabel(self.centralwidget)
        self.label_pix.setGeometry(QtCore.QRect(480, 60, 210, 260))
        self.label_pix.setText("")
        self.label_pix.setObjectName("label_pix")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(410, 20, 68, 19))
        self.label_7.setObjectName("label_7")
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setGeometry(QtCore.QRect(480, 20, 210, 25))
        self.lineEdit_name.setObjectName("lineEdit_name")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Adding Book"))
        self.label.setText(_translate("MainWindow", "Add a new book"))
        self.label_2.setText(_translate("MainWindow", "Title :"))
        self.label_3.setText(_translate("MainWindow", "Author :"))
        self.label_4.setText(_translate("MainWindow", "Publisher :"))
        self.label_5.setText(_translate("MainWindow", "Publication date :"))
        self.pushButton_add.setText(_translate("MainWindow", "Add"))
        self.pushButton.setText(_translate("MainWindow", "Select file"))
        self.label_7.setText(_translate("MainWindow", "Name :"))

