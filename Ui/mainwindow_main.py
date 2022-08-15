from Ui.mainwindow import Ui_MainWindow
from Ui.dataset_dialog_main import DatasetDialog
from Ui.conten_frame_main import ContenFrame

from dataset import Dataset
import regression
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from functools import partial


class MainWindowMain(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./resources/ai-icon-9.png"))

        self.upperframe_list = [
            self.ui.regression,
            self.ui.classification,
            self.ui.deep_learn
        ]

        self.project_name = ""
        self.dataset = None
        self.current_mode= None
        self.regression_list = []

        self.current_side_bar = [
            DepFeatSelctFrame(self.regression_list, self.dataset, self), 
            DepFeatSelctFrame(self.regression_list,self.dataset, self), 
            DepFeatSelctFrame(self.regression_list, self.dataset, self)
            ]
            

        self.ui.regression.clicked.connect(self.select_regression_mode)
        self.ui.classification.clicked.connect(self.select_classification_mode)
        self.ui.deep_learn.clicked.connect(self.select_deep_learn_mode)

        self.ui.actionOpen_new_Project.triggered.connect(self.open_new_project)
        self.ui.actionOpen_Project.triggered.connect(self.open_project)

        self.select_regression_mode()

    def open_new_project(self):
        window = DatasetDialog(self)
        window.show()

    def open_project(self):
        folderpath = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Open Directory",
                "C:\\Users\\sbues\\VSCode\\python\\Regression\\projects",
            )
        )
        self.project_name = folderpath.split("/")[-1]
        status = self.load_dataset(folderpath, self.project_name)

        if status:
            self.create_single_regression_objs(
                
            )
            self.current_side_bar[self.current_mode].populate_DepFeatComBox(self.dataset)
            self.current_side_bar[self.current_mode].update_scrollarea(self.regression_list)

    def load_dataset(self, path, project_name):
        try:
            self.dataset = Dataset()
            self.dataset.load_dataset(path, project_name)
        except Exception as e:
            print(e)
            print("error: mainwindow -> open_project() ")
            return False
        return True

    def update_SideNavBar(self):
        if type(self.current_side_bar) is SideNavBar:
            self.current_side_bar.update_bar(self.regression_list)
    
    def check_is_sidebar_exist(self):
        if type(self.current_side_bar) is SideNavBar:
            return True
        return False
            

    def select_regression_mode(self):
        self.reset_upperframe_button_style()
        self.select_upperframe_button_style(self.ui.regression)

        self.current_side_bar[1].hide()
        self.current_side_bar[2].hide()
        self.current_side_bar[0].show()

        self.current_mode = 0


    def select_classification_mode(self):
        self.reset_upperframe_button_style()
        self.select_upperframe_button_style(self.ui.classification)
        self.current_side_bar[0].hide()
        self.current_side_bar[2].hide()
        self.current_side_bar[1].show()
        self.current_mode = 1


    def select_deep_learn_mode(self):
        self.reset_upperframe_button_style()
        self.select_upperframe_button_style(self.ui.deep_learn)
        self.current_side_bar[0].hide()
        self.current_side_bar[1].hide()

        self.current_side_bar[2].show()

        self.current_mode = 2

    def select_upperframe_button_style(self, bottun):
        bottun.setStyleSheet(
            "QPushButton {font: bold; color: #ffffff; text-align: center; border: solid #ffffff; border-width: 0px 0px 1px 0px} QPushButton:hover {background-color: rgba(255,255,255,0.1);}"
        )

    def reset_upperframe_button_style(self):
        for bottun in self.upperframe_list:
            bottun.setStyleSheet(
                "QPushButton {font: bold; color: #C1C1C1; text-align: center;border: None} QPushButton:hover {background-color: rgba(255,255,255,0.1);}"
            )

    def create_single_regression_objs(self ):
        self.regression_list = [
            regression.SingleVarRegression(column, self.dataset, "polynomial", 3)
            for column in self.dataset.get_df()
            if column != self.dataset.get_dependet_feature()
        ]

    def print_me(self):
        print("Print Me!")


class DepFeatSelctFrame(QtWidgets.QFrame):
    def __init__(self, regression_list, dataset, parent = None) -> None:
        super().__init__(parent)
        self.parent =parent
        self.dataset = dataset
        self.nav_area =SideNavBar(regression_list, self)

        self.setGeometry(QtCore.QRect(0, 53, 170,700))
        self.setStyleSheet("QFrame{background-color:#0e1517;}")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("DepFeaturFrame")
        self.DepFeaturLabel = QtWidgets.QLabel("Dependent Featur:",self)
        self.DepFeaturLabel.setGeometry(QtCore.QRect(10, 0, 111, 21))
        self.DepFeaturLabel.setStyleSheet("QLabel {font: bold; color: #C1C1C1; text-align: center;  border-width: 0px 0px 0px 0px}")
        self.DepFeaturLabel.setObjectName("DepFeaturLabel")
        self.DepFeatComBox = QtWidgets.QComboBox(self)
        self.DepFeatComBox.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.DepFeatComBox.setEditable(False)
        self.DepFeatComBox.setCurrentText("")
        self.DepFeatComBox.setObjectName("DepFeatComBox")
        self.SetDepFeat = QtWidgets.QPushButton("Set",self)
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

    def update_scrollarea(self,  regression_list):
        self.nav_area.update_bar(regression_list)


class SideNavBar(QtWidgets.QScrollArea):
    def __init__(self, regression_list, parent=None) -> None:
        super().__init__(parent)
        self.parent =parent

        self.regression_obj_list = regression_list
        self.SideNavBar_btn_list = []

        self.setGeometry(QtCore.QRect(0, 61, 171, 650))
        self.setStyleSheet("QScrollArea QWidget{background-color: #0e1517; border: solid #C1C1C1; border-width: 1px 0px 0px 0px;}")
        self.setLineWidth(1)
        self.setWidgetResizable(True)
        self.setObjectName("FeaturListScrollArea")
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 171, 641))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.setWidget(self.scrollAreaWidgetContents)

        self.populate_SideNavBar()

    def update_bar(self, regression_list):
        self.regression_obj_list = regression_list
        self.populate_SideNavBar()

    def create_run_btn(self, row):
        run_btn = QtWidgets.QPushButton("Run", self.scrollAreaWidgetContents)
        self.style_run_btn(run_btn)
        run_btn.setMinimumSize(QtCore.QSize(30, 23))
        self.gridLayout.addWidget(run_btn, row, 2, 1, 1)
        run_btn.show()

    def style_run_btn(self, btn):
        btn.setStyleSheet(
        "QPushButton{background-color: rgba(50, 168, 82, 0.5); border: None;}"
        "QPushButton:hover{background-color: rgb(50, 168, 82);}"
        )

    def create_regression_button(self, regrs_obj, row):
        feat_btn = QtWidgets.QPushButton(
            regrs_obj.get_featur_name(), self.scrollAreaWidgetContents
        )
        feat_btn.setObjectName("feat_btn")
        self.style_SideNavBar_button(feat_btn)
        feat_btn.setMinimumSize(QtCore.QSize(140, 23))
        self.gridLayout.addWidget(feat_btn, row, 0, 1, 2)
        self.SideNavBar_btn_list.append(feat_btn)
        feat_btn.clicked.connect(partial(self.select_feature, feat_btn, regrs_obj, row))
        feat_btn.show()

    def style_SideNavBar_button(self, bottun):
        bottun.setStyleSheet(
            "QPushButton {color: #C1C1C1; text-align: left; border: None}"
            "QPushButton:hover{background-color: rgba(255,255,255,0.1);}"
        )
        bottun.setIcon(QtGui.QIcon("./resources/angle-right.png"))

    def reset_SideNavBar_btn_style(self):
        for bottun in self.SideNavBar_btn_list:
            bottun.setStyleSheet(
                "QPushButton {color: #C1C1C1; text-align: left; border: None}"
                "QPushButton:hover{background-color: rgba(255,255,255,0.1);}"
            )
            bottun.setIcon(QtGui.QIcon("./resources/angle-right.png"))

    def add_spacer(self, row):
        self.setWidget(self.scrollAreaWidgetContents)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.gridLayout.addItem(spacerItem, row, 0, 1, 1)

    def reset_SideNavBar(self):
        for btn in self.SideNavBar_btn_list:
            btn.deleteLater()

        self.SideNavBar_btn_list = []

    def populate_SideNavBar(self):
        self.reset_SideNavBar()
        row = 0
        if self.regression_obj_list :
            for regrs_obj in self.regression_obj_list:
                self.create_regression_button(regrs_obj, row)
                #self.create_run_btn(row)
                row += 1

            self.add_spacer(row + 1)
        else:
            self.no_data()

    def no_data(self):
        NoData = QtWidgets.QLabel("No Data", self.scrollAreaWidgetContents)
        NoData.setGeometry(QtCore.QRect(170, 30, 931, 691))
        NoData.setStyleSheet("QLabel{ color: rgba(255, 255, 255, 0.2); font: bold;  font-size: 20px;}")
        self.gridLayout.addWidget(NoData, 0, 0, 1, 1)
        NoData.setAlignment(QtCore.Qt.AlignCenter)
        self.SideNavBar_btn_list.append(NoData)
        NoData.show()

    def select_feature(self, button, regrs_obj, row):
        self.reset_SideNavBar_btn_style()
        self.selected_featur_btn_style(button)
        self.gridLayout.addWidget(button, row, 0, 1, 1)
        self.create_run_btn( row)
        self.parent.parent.print_me()
        de = ContenFrame(self.parent.parent)
        de.show()

    def selected_featur_btn_style(self, button):
        
        button.setStyleSheet(
            "QPushButton {background-color: rgba(255,255,255,0.1); font: bold; color: #ffffff; text-align: left; padding-left: 5px; border: solid #ffffff; border-width: 0px 0px 0px 3px} "
            "QPushButton:hover{background-color: rgba(255,255,255,0.1);}"
        )
        button.setIcon(QtGui.QIcon("./resources/angle-right-ffffff.png"))


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    # root.setStyleSheet(open('./style.css').read())
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec())
