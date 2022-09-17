#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
from app.mainwindow import MainWindowMain
from PyQt5 import QtCore, QtWidgets
import sys


def main():
    mode = "app"
    print("")
    if mode == "app":
        runapp()



def runapp():
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec_())


if __name__ == "__main__":
    main()
# with open(f"./app/style/new_project_style.json") as file:
    #     self.style_dict = json.load(file)
    # self.setStyleSheet(style.format_file(self.style_dict))
