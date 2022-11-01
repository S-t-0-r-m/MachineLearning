#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
from app.mainwindow import MainWindowMain
from PyQt6 import QtCore, QtWidgets
import sys
import os

PATH = os.path.dirname(__file__)

def main():


    run_app()

 

def run_app():
    root = QtWidgets.QApplication(sys.argv)
    window = MainWindowMain()

    window.show()
    sys.exit(root.exec())


if __name__ == "__main__":
    main()

