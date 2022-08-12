import sys
from tkinter import Widget
from PyQt5 import QtCore, QtGui, QtWidgets


class Interface(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.w_height = 700
        self.w_wights = 1100

        self.setWindowTitle(" Machine Learning")
        self.setWindowIcon(QtGui.QIcon("./pics/ai-icon-9.png"))
        self.setGeometry(400, 300, self.w_wights, self.w_height)
        self.autoFillBackground()

        self.sideframe_nxt_elem_y_position = 0
        self.sideframe_elem_height = 25

        self.upperframe = QtWidgets.QFrame(self)
        self.upperframe.setGeometry(QtCore.QRect(0, 0, self.w_wights, 50))
        self.upperframe.setStyleSheet(
            "background-color: #18191a; border-bottom: solid #ccc; border-width: 1px"
        )

        self.btn1 = QtWidgets.QPushButton(f"Add new Project", self.upperframe)
        self.btn1.setGeometry(QtCore.QRect(0, 0, 150, 49))
        self.btn1.setIcon(QtGui.QIcon("./pics/add-icon.png"))
        self.btn1.clicked.connect(self.new_project)
        self.btn1.setStyleSheet(
            "QPushButton {font: bold; color: #C1C1C1; text-align: center; }"
        )

        self.btn2 = QtWidgets.QPushButton(f" Open Project", self.upperframe)
        self.btn2.setGeometry(QtCore.QRect(151, 0, 150, 49))
        self.btn2.setIcon(QtGui.QIcon("./pics/list-icon.png"))
        self.btn2.setStyleSheet(
            "QPushButton {font: bold; color: #C1C1C1; text-align: center; }"
        )

        self.sideframe = QtWidgets.QFrame(self)
        self.sideframe.setGeometry(QtCore.QRect(0, 50, 150, self.w_height - 50))
        self.sideframe.setStyleSheet("background-color: #18191a")
        self.sidef_elem_list = []

        self.contendframe = QtWidgets.QFrame(self)
        self.contendframe.setGeometry(QtCore.QRect(150, 50, self.w_wights - 150, self.w_height - 50))
        self.contendframe.setStyleSheet("background-color: #262729")

        

    def create_sidebar_btn(self, name):

        btn = QtWidgets.QPushButton(f"{name} ", self.sideframe)
        btn.setGeometry(QtCore.QRect(0, self.sideframe_nxt_elem_y_position + 1, 150, self.sideframe_elem_height))
        btn.setIcon(QtGui.QIcon("./pics/angle-right.png"))
        btn.setStyleSheet(
                "QPushButton { font-family: Arila; color: #C1C1C1; text-align: left; border: None; padding-left: 10px;}"
                "QPushButton:focus { background-color: rgba( 35, 46, 166,0.5); border: 1px solid rgb(54, 121, 255);}"
                "QPushButton:hover{background-color: rgba(255, 255, 255, 0.2);}"
            )
        btn.clicked.connect(self.create_contend)
        self.sidef_elem_list.append(btn)
        btn.show()
        self.increment_next_position()

    def create_sidebar_lable(self, name):

        label = QtWidgets.QLabel(f" {name}", self.sideframe)
        label.setGeometry(QtCore.QRect(0, self.sideframe_nxt_elem_y_position + 1, 150, 25))
        label.setStyleSheet(
            "QLabel {font: bold; color: #C1C1C1; text-align: left; border-bottom: solid #505050; border-width: 1px; margin-right: 20px;}"
        )

        label.show()
        self.sidef_elem_list.append(label)
        self.increment_next_position()

    def increment_next_position(self):
        self.sideframe_nxt_elem_y_position += self.sideframe_elem_height
        
    def destroy_sidebar(self) -> None:
        for elemant in self.sidef_elem_list:
            elemant.setParent(None)
        self.sideframe_nxt_elem_y_position = 0



            
    def create_contend(self, name):

        label = QtWidgets.QLabel(f" {name}", self.sideframe)
        label.setGeometry(QtCore.QRect(0, self.sideframe_nxt_elem_y_position + 1, 150, 25))
        label.setStyleSheet(
            "QLabel {font: bold; color: #C1C1C1; text-align: left; border-bottom: solid #ccc; border-width: 1px;}"
        )




if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    root = QtWidgets.QApplication(sys.argv)
    root.setStyleSheet(open("./style/StyleSheet.css").read())
    window = Interface()
    window.show()

    sys.exit(root.exec())
