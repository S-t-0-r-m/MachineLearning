from app.sidebar_main import DeepSidebar, ClassSidebar, RegSidebar
from app.new_project_dialog import NewProjectDialog
from dataset import Dataset
import regression

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import os

very_light_blue =  "hsl(217, 12%, 80%)"
light_grey = "hsl(217, 12%, 63%)"
medium_grey = "hsl(216, 12%, 54%)"
dark_blue = "hsl(213, 19%, 18%)"
very_dark_blue = "hsl(216, 12%, 8%)"
orange = " hsl(25, 97%, 53%)"

PATH = os.path.dirname(__file__)

class MainWindowMain(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        uic.loadUi(f"{PATH}/ui/mainwindow.ui", self)

        
        self.setWindowIcon(QtGui.QIcon(os.path.join(PATH, ".." ,"resources", "ai-icon-9.png" )))
        self.height = 860
        self.width = 1200

        self.project_name = ""
        self.dataset = None
        self.current_mode = None
        self.regression_list = []
        self.dialog = None

        window_elements = [
                self.regression
             ]

        self.actionOpen_new_Project.triggered.connect(self.open_new_project)
        self.actionOpen_Project.triggered.connect(self.open_project)

    def open_new_project(self):
        self.dialog = NewProjectDialog()
        self.dialog.show()

    def open_project(self):
        folderpath = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                "Open Directory",
                "C:\\Users\\sbues\\VSCode\\python\\Regression\\projects",
            )
        )

        status = False
        if folderpath != "":
            self.project_name = folderpath.split("/")[-1]
            status = self.load_dataset(folderpath, self.project_name)

        if status:
            self.create_single_regression_objs()
            self.current_side_bar[self.current_mode].populate_DepFeatComBox(
                self.dataset
            )
            self.current_side_bar[self.current_mode].update_scrollarea(
                self.regression_list
            )

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
        if type(self.current_side_bar) is RegSidebar:
            self.current_side_bar.update_bar(self.regression_list)

    def check_is_sidebar_exist(self):
        if type(self.current_side_bar) is RegSidebar:
            return True
        return False

    def select_upperframe_button_style(self, bottun):
        bottun.setStyleSheet(
            "QPushButton {font: bold; color: #ffffff; text-align: center; border: solid #ffffff; border-width: 0px 0px 1px 0px} QPushButton:hover {background-color: rgba(255,255,255,0.1);}"
        )

    def reset_upperframe_button_style(self):
        for bottun in self.upperframe_list:
            bottun.setStyleSheet(
                "QPushButton {font: bold; color: #C1C1C1; text-align: center;border: None} QPushButton:hover {background-color: rgba(255,255,255,0.1);}"
            )

    def create_single_regression_objs(self):
        self.regression_list = [
            regression.SingleVarRegression(column, self.dataset, "polynomial", 3)
            for column in self.dataset.get_df()
            if column != self.dataset.get_dependet_feature()
        ]

    # def closeEvent(self, event: QtGui.QCloseEvent) -> None:
    #     if not self.dialog is None:
    #         self.dialog.deleteLater()
    #     return super().closeEvent(event)


    # def resizeEvent(self, event) -> None:
    #     self.height = event.size().height()
    #     self.width = event.size().width()
    #     self.ui.upperframe.resize(self.width, 31)

    #     for bar in self.current_side_bar:
    #         bar.resize(170, self.height - 74)
    #         bar.nav_area.resize(171, self.height - 150)
    #         #bar.nav_area.scrollAreaWidgetContents.resize(171, height - 150)

            
    #         print(f"width: {self.width}, height: {self.height}")
    #         bar.nav_area.resize_contend(self.width, self.height)

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
