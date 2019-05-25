import sys, os, re
sys.path.insert(0, 'GUI')
from functionality import *

def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = StartWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 