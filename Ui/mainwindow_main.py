from tkinter import Button
from Ui.mainwindow import Ui_MainWindow
from Ui.dataset_dialog_main import DatasetDialog
from dataset import Dataset
import regression
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from functools import partial


class MainWindowMain(QtWidgets.QMainWindow):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.upperframe_list = [self.ui.lin_regression, self.ui.log_regression, self.ui.deep_learn]
        self.FeaturListScrollArea_list = []
        self.project_name = ""
        self.dataset = None
        self.currentcontend = None
        regression_list = None 

        self.ui.lin_regression.clicked.connect(partial(self.select_ml_mode, self.ui.lin_regression))
        self.ui.log_regression.clicked.connect(partial(self.select_ml_mode, self.ui.log_regression))
        self.ui.deep_learn.clicked.connect(partial(self.select_ml_mode, self.ui.deep_learn))

        self.ui.actionOpen_new_Project.triggered.connect(self.open_new_project)
        self.ui.actionOpen_Project.triggered.connect(self.open_project)

        self.ui.SetDepFeat.clicked.connect(self.set_dependen_featur)

    def set_dependen_featur(self):
        self.dataset.set_dependet_feature(self.ui.DepFeatComBox.currentText())
        self.dataset.save_dataset(self.project_name)
        self.populate_FeaturListScrollArea()
        
    def open_new_project(self):
        window = DatasetDialog(self)
        window.show()

    def populate_DepFeatComBox(self):
        for column in self.dataset.get_df():
            self.ui.DepFeatComBox.addItem(column)

        self.ui.DepFeatComBox.setCurrentText(self.dataset.get_dependet_feature())
        
    def open_project(self):

        folderpath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", "C:\\Users\\sbues\\VSCode\\python\\Regression\\projects"))
        self.project_name = folderpath.split("/")[-1]
        
        try:
            self.dataset = Dataset()
            self.dataset.load_dataset(folderpath, self.project_name)
            self.populate_DepFeatComBox()
            self.populate_FeaturListScrollArea()
        except:
            print("error: mainwindow -> open_project() ")
    
    def load_dataset(self):
        if self.project_name == "":
            return
        self.dataset = Dataset()
        self.dataset.load_dataset(self.project_name)
        
    def populate_FeaturListScrollArea(self):

        for btn in self.FeaturListScrollArea_list:
            btn.deleteLater()

        self.FeaturListScrollArea_list = []

        row = 0
        for  column in self.dataset.get_df():
            if column == self.dataset.get_dependet_feature():
                continue
            
            self.create_regression_button(column, row)
            row += 1
        row += 1
        self.ui.FeaturListScrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.gridLayout.addItem(spacerItem, row , 0, 1, 1)
        self.ui.SetDepFeat.setEnabled(True)
        
    def select_ml_mode(self, bottun):
        self.reset_upperframe_button()

        bottun.setStyleSheet("QPushButton {font: bold; color: #ffffff; text-align: center; border: solid #ffffff; border-width: 0px 0px 1px 0px} QPushButton:hover {background-color: rgba(255,255,255,0.1);}")

        self.Mode = bottun

    def reset_upperframe_button(self):
        for bottun in self.upperframe_list:
            bottun.setStyleSheet("QPushButton {font: bold; color: #C1C1C1; text-align: center;border: None} QPushButton:hover {background-color: rgba(255,255,255,0.1);}")

    def select_featur(self, button):
        self.reset_sideframe_button()
        button.setStyleSheet("QPushButton {background-color: rgba(255,255,255,0.1); font: bold; color: #ffffff; text-align: left; padding-left: 5px; border: solid #ffffff; border-width: 0px 0px 0px 3px} "
        "QPushButton:hover{background-color: rgba(255,255,255,0.1);}")
        button.setIcon(QtGui.QIcon("./resources/angle-right-ffffff.png"))

    def reset_sideframe_button(self):
        for bottun in self.FeaturListScrollArea_list:
            bottun.setStyleSheet("QPushButton {color: #C1C1C1; text-align: left; border: None}"
                "QPushButton:hover{background-color: rgba(255,255,255,0.1);}")
            bottun.setIcon(QtGui.QIcon("./resources/angle-right.png"))

    def create_regression_button(self, name, row):
        feat_btn = QtWidgets.QPushButton(name, self.ui.scrollAreaWidgetContents)
        feat_btn.setObjectName("feat_btn")
        self.style_FeaturListScrollArea_button(feat_btn)
        feat_btn.setMinimumSize(QtCore.QSize(0, 23))
        self.ui.gridLayout.addWidget(feat_btn, row, 0, 1, 1)
        self.FeaturListScrollArea_list.append(feat_btn)
        feat_btn.clicked.connect(partial(self.select_featur, feat_btn))

    def style_FeaturListScrollArea_button(self, bottun):
        bottun.setStyleSheet("QPushButton {color: #C1C1C1; text-align: left; border: None}"
            "QPushButton:hover{background-color: rgba(255,255,255,0.1);}")
        bottun.setIcon(QtGui.QIcon("./resources/angle-right.png"))

    def create_single_regression_objs(data, dep_feature):
        
        regrs_list = []
        
        regrs_list = [regression.SingleVarRegression(column, data, "polynomial", 3) for column in data.normalised_df if column != dep_feature]
            #!= dep_feature
        
        

        return regrs_list


if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    root = QtWidgets.QApplication(sys.argv)
    #root.setStyleSheet(open('./style.css').read())
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec())
