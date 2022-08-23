#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
import time
import regression
import concurrent.futures
from dataset import Dataset
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np

from app.mainwindow_main import MainWindowMain
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    mode = "app"

    if mode == "app":
        runapp()
        return



def runapp():

    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec())




if __name__ == "__main__":
    main()
