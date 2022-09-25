#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
from app.mainwindow import MainWindowMain
from PyQt5 import QtCore, QtWidgets
import sys
import os

PATH = os.path.dirname(__file__)

def main():
    mode = "app"
    if mode == "app":
        runapp()


def runapp():
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    print(root.primaryScreen())
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec_())


if __name__ == "__main__":
    main()
