import sys, os, re
sys.path.insert(0, 'src/GUI')
from execution import *

def main():
    app = QApplication(sys.argv)
    ex = Execution()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main() or 0)