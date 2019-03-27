# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginWin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnSignUp = QtWidgets.QPushButton(self.centralwidget)
        self.btnSignUp.setGeometry(QtCore.QRect(40, 290, 321, 81))
        self.btnSignUp.setObjectName("btnSignUp")
        self.btnSignIn = QtWidgets.QPushButton(self.centralwidget)
        self.btnSignIn.setGeometry(QtCore.QRect(40, 130, 321, 81))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.btnSignIn.setFont(font)
        self.btnSignIn.setObjectName("btnSignIn")
        self.labelHeader = QtWidgets.QLabel(self.centralwidget)
        self.labelHeader.setGeometry(QtCore.QRect(50, 50, 301, 34))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.labelHeader.setFont(font)
        self.labelHeader.setObjectName("labelHeader")
        self.labelInfo = QtWidgets.QLabel(self.centralwidget)
        self.labelInfo.setGeometry(QtCore.QRect(50, 260, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelInfo.setFont(font)
        self.labelInfo.setObjectName("labelInfo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Library Login"))
        self.btnSignUp.setText(_translate("MainWindow", "Sign up"))
        self.btnSignIn.setText(_translate("MainWindow", "Sign in"))
        self.labelHeader.setText(_translate("MainWindow", "Sign in to Smart Library"))
        self.labelInfo.setText(_translate("MainWindow", "If you are not a member:"))

