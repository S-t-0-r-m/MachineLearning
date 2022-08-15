from PyQt5 import QtCore, QtGui, QtWidgets
from Ui.contend_frame import Ui_TabWidget

class  ContenFrame(QtWidgets.QTabWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        self.parent_element = parent
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)
        self.setGeometry(170,53,998, 751)

        

