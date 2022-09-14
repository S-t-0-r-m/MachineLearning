import time
from app.conten_frame import ContenFrame
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import os

PATH = os.path.dirname(__file__)

class RegSidebar:
    def __init__(self, parent) -> None:
        self.parent = parent
        
        pass

class ClassSidebar:
    def __init__(self, parent) -> None:
        self.parent = parent
        
        pass

class DeepSidebar:
    def __init__(self, parent) -> None:
        self.parent = parent
        
        pass
    

class DepFeatSelctFrame(QtWidgets.QFrame):
    def __init__(self, regression_list, dataset, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.dataset = dataset
        self.nav_area = SideNavBar(regression_list, self)

        self.setGeometry(QtCore.QRect(0, 53, 170, 700))
        self.setStyleSheet("QFrame{background-color:#0e1517;}")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("DepFeaturFrame")
        self.DepFeaturLabel = QtWidgets.QLabel("Dependent Featur:", self)
        self.DepFeaturLabel.setGeometry(QtCore.QRect(10, 0, 111, 21))
        self.DepFeaturLabel.setStyleSheet(
            "QLabel {font: bold; color: #C1C1C1; text-align: center; border-width: 0px 0px 0px 0px}"
        )
        self.DepFeaturLabel.setObjectName("DepFeaturLabel")
        self.DepFeatComBox = QtWidgets.QComboBox(self)
        self.DepFeatComBox.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.DepFeatComBox.setEditable(False)
        self.DepFeatComBox.setCurrentText("")
        self.DepFeatComBox.setObjectName("DepFeatComBox")
        self.SetDepFeat = QtWidgets.QPushButton("Set", self)
        self.SetDepFeat.setEnabled(False)
        self.SetDepFeat.setGeometry(QtCore.QRect(120, 30, 41, 23))
        self.SetDepFeat.setObjectName("SetDepFeat")
        self.SetDepFeat.clicked.connect(self.set_dependen_featur)

    def set_dependen_featur(self):
        self.dataset.set_dependet_feature(self.DepFeatComBox.currentText())
        self.dataset.save_dataset(self.parent.project_name)
        self.parent.create_single_regression_objs()
        self.update_scrollarea(self.parent.regression_list)

    def populate_DepFeatComBox(self, dataset):
        if dataset is None:
            return

        self.dataset = dataset

        for column in self.dataset.get_df():
            self.DepFeatComBox.addItem(column)
        self.DepFeatComBox.setCurrentText(self.dataset.get_dependet_feature())

        self.SetDepFeat.setEnabled(True)

    def update_scrollarea(self, regression_list):
        self.nav_area.update_bar(regression_list)


class SideNavBar(QtWidgets.QScrollArea):
    def __init__(self, regression_list, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent

        self.setGeometry(QtCore.QRect(0, 61, 171, 550))
        self.setStyleSheet(
            "QScrollArea QWidget{background-color: #0e1517; border: solid #ffffff; border-width: 0px 0px 0px 0px }"
            "QScrollArea{background-color: #0e1517; border: none }"
        )
        self.setLineWidth(1)
        self.setWidgetResizable(True)
        self.setObjectName("FeaturListScrollArea")
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 171, 550))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.setWidget(self.scrollAreaWidgetContents)

        self.run_btn = QtWidgets.QPushButton("Run", self.scrollAreaWidgetContents)
        self.style_run_btn(self.run_btn)
        self.run_btn.setMinimumSize(QtCore.QSize(30, 23))
        self.run_btn.clicked.connect(self.run_onclick)
        self.run_btn.hide()

        self.stop_btn = QtWidgets.QPushButton("Stop", self.scrollAreaWidgetContents)
        self.stop_btn.setMinimumSize(QtCore.QSize(30, 23))
        self.style_stop_btn(self.stop_btn)
        self.stop_btn.clicked.connect(self.stop_onclick)
        self.stop_btn.hide()

        self.regression_obj_list = regression_list
        self.SideNavBar_btn_list = []
        self.current_contend_list = []
        self.current_index = -1

        self.populate_SideNavBar()

    def resize_contend(self, width, height):
        if self.current_index >= 0:
            self.current_contend_list[self.current_index].resiz(width, height)

    def update_bar(self, regression_list):
        self.regression_obj_list = regression_list
        self.populate_SideNavBar()

    def reset_SideNavBar(self):
        for btn in self.SideNavBar_btn_list:
            btn.deleteLater()
        if not self.run_btn is None:
            self.run_btn.hide()

        self.SideNavBar_btn_list = []

    def populate_SideNavBar(self):
        self.reset_SideNavBar()
        row = 0
        if self.regression_obj_list:
            for regrs_obj in self.regression_obj_list:
                self.create_regression_button(regrs_obj, row, 2)
                self.current_contend_list.append(ContenFrame(regrs_obj, self.parent.parent))
                row += 1
            self.add_spacer(row + 1)
        else:
            self.no_data()

    def create_regression_button(self, regrs_obj, row, size):
        feat_btn = QtWidgets.QPushButton(
            regrs_obj.get_featur_name(), self.scrollAreaWidgetContents
        )
        feat_btn.setObjectName("feat_btn")
        feat_btn.setMinimumSize(QtCore.QSize(140, 23))
        self.gridLayout.addWidget(feat_btn, row, 0, 1, 2)
        self.SideNavBar_btn_list.append(feat_btn)
        feat_btn.clicked.connect(partial(self.select_feature, row))
        self.style_SideNavBar_button(feat_btn)
        feat_btn.show()

    def select_feature(self, row):
        if self.current_index >= 0:
            self.current_contend_list[self.current_index].hide()
        self.current_contend_list[row].show()

        self.deselect_row()
        self.show_run_btn(row)

        self.current_index = row

        self.selected_featur_btn_style(self.SideNavBar_btn_list[row])

        self.parent.parent.print_me()

    def deselect_row(self):
        if self.current_index >= 0:
            btn = self.SideNavBar_btn_list[self.current_index]
            self.gridLayout.addWidget(btn, self.current_index, 0, 1, 2)
            self.style_SideNavBar_button(btn)

    def show_run_btn(self, row):
        self.gridLayout.addWidget(self.run_btn, row, 1, 1, 1)
        self.run_btn.show()

    def add_spacer(self, row):
        self.setWidget(self.scrollAreaWidgetContents)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout.addItem(spacerItem, row, 0, 1, 1)
    
    def show_spot_btn(self):
        self.gridLayout.addWidget(self.stop_btn, self.current_index, 1, 1, 1)
        self.stop_btn.show()

    def run_onclick(self):
        start = time.time()
        row = self.current_index
        self.run_btn.hide()
        self.show_spot_btn()
        self.worker = WorkerThread(self.regression_obj_list[row])
        self.worker.start()
        self.worker.finished.connect(
            partial(self.worker_finished, self.regression_obj_list[row],  start, row)
        )
    def stop_onclick(self):
        self.regression_obj_list[self.current_index].stop = True 

    def worker_finished(self, regression_obj, start, row):
        end = time.time()

        self.current_contend_list[row].update_contend(end -start)
        self.current_contend_list[row].show()
        
        self.run_btn.show()
        self.stop_btn.hide()

    def no_data(self):
        NoData = QtWidgets.QLabel("No Data", self.scrollAreaWidgetContents)
        NoData.setGeometry(QtCore.QRect(170, 30, 931, 691))
        NoData.setStyleSheet(
            "QLabel{ color: rgba(255, 255, 255, 0.2); font: bold;  font-size: 20px;}"
        )
        self.gridLayout.addWidget(NoData, 0, 0, 1, 1)
        NoData.setAlignment(QtCore.Qt.AlignCenter)
        self.SideNavBar_btn_list.append(NoData)
        NoData.show()

    def style_run_btn(self, btn):
        btn.setStyleSheet(
            "QPushButton{background-color: rgba(50, 168, 82, 0.5); border: None;font-weight: bold;}"
            "QPushButton:hover{background-color: rgb(50, 168, 82);}"
        )

    def style_stop_btn(self, btn):
        btn.setStyleSheet(
            "QPushButton{background-color: rgb(163, 26, 26); border: None;font-weight: bold;}"
            "QPushButton:hover{background-color: rgb(163, 26, 26);}"
        )

    def style_SideNavBar_button(self, bottun):
        bottun.setStyleSheet(
            "QPushButton {color: #C1C1C1; text-align: left; border: None}"
            "QPushButton:hover{background-color: rgba(255,255,255,0.1);}"
        )
        bottun.setIcon(QtGui.QIcon(f"{PATH}/resources/angle-right.png"))

    def selected_featur_btn_style(self, button):
        button.setStyleSheet(
            "QPushButton {background-color: rgba(255,255,255,0.1); font: bold; color: #ffffff; text-align: left; padding-left: 5px; border: solid #ffffff; border-width: 0px 0px 0px 3px} "
            "QPushButton:hover{background-color: rgba(255,255,255,0.1);}"
        )
        button.setIcon(QtGui.QIcon(f"{PATH}/resources/angle-right-ffffff.png"))
        self.gridLayout.addWidget(button, self.current_index, 0, 1, 1)


class WorkerThread(QtCore.QThread):
    def __init__(self, regression_obj) -> None:
        super().__init__()
        self.regression_obj = regression_obj

    def run(self):
        self.regression_obj.linear_regression()