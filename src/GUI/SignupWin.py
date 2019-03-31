# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignupWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 451)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Russia))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEditFName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditFName.setGeometry(QtCore.QRect(180, 100, 176, 25))
        self.lineEditFName.setObjectName("lineEditFName")
        self.labelFName = QtWidgets.QLabel(self.centralwidget)
        self.labelFName.setGeometry(QtCore.QRect(40, 110, 74, 19))
        self.labelFName.setObjectName("labelFName")
        self.labelLName = QtWidgets.QLabel(self.centralwidget)
        self.labelLName.setGeometry(QtCore.QRect(40, 150, 72, 19))
        self.labelLName.setObjectName("labelLName")
        self.labelMName = QtWidgets.QLabel(self.centralwidget)
        self.labelMName.setGeometry(QtCore.QRect(40, 200, 90, 19))
        self.labelMName.setObjectName("labelMName")
        self.lineEditLName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditLName.setGeometry(QtCore.QRect(180, 150, 176, 25))
        self.lineEditLName.setObjectName("lineEditLName")
        self.lineEditMName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditMName.setGeometry(QtCore.QRect(180, 200, 176, 25))
        self.lineEditMName.setObjectName("lineEditMName")
        self.labelPhone = QtWidgets.QLabel(self.centralwidget)
        self.labelPhone.setGeometry(QtCore.QRect(40, 250, 44, 19))
        self.labelPhone.setObjectName("labelPhone")
        self.lineEditPhone = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPhone.setGeometry(QtCore.QRect(180, 250, 176, 25))
        self.lineEditPhone.setObjectName("lineEditPhone")
        self.btnSignUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnSignUp.setGeometry(QtCore.QRect(40, 320, 321, 71))
        self.btnSignUp.setObjectName("btnSignUp")
        self.labelHeader = QtWidgets.QLabel(self.centralwidget)
        self.labelHeader.setGeometry(QtCore.QRect(110, 30, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelHeader.setFont(font)
        self.labelHeader.setObjectName("labelHeader")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(380, 40, 380, 350))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCamera.sizePolicy().hasHeightForWidth())
        self.labelCamera.setSizePolicy(sizePolicy)
        self.labelCamera.setText("")
        self.labelCamera.setObjectName("labelCamera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Join Smart Library"))
        self.labelFName.setText(_translate("MainWindow", "First name"))
        self.labelLName.setText(_translate("MainWindow", "Last name"))
        self.labelMName.setText(_translate("MainWindow", "Middle name"))
        self.labelPhone.setText(_translate("MainWindow", "Phone"))
        self.btnSignUp.setText(_translate("MainWindow", "Sign up for Smart Library"))
        self.labelHeader.setText(_translate("MainWindow", "Join Smart Library"))

