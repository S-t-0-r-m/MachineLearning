from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from typing import Callable
import pandas as pd
import dataset
import settings
import os
import sys


very_light_blue =  "hsl(217, 12%, 80%)"
light_grey = "hsl(217, 12%, 63%)"
medium_grey = "hsl(216, 12%, 54%)"
dark_blue = "hsl(213, 19%, 18%)"
very_dark_blue = "hsl(216, 12%, 8%)"
orange = "hsl(25, 97%, 53%)"


PATH = os.path.dirname(__file__)


class NewProjectDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None) -> None:
        print("ds")
        super().__init__(parent)
        self.parent_element = parent

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
               
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(PATH, "..", "resources", "ai-icon-9.png"))
        )
        QtGui.QFontDatabase.addApplicationFont("./resources/roboto_regular.ttf")

        self.resize(600, 600)

        self.user_inputs = {
            "dataframe": None,
            "df_is_valid": False,
            "separator": None,
            "path": None,
            "poject_name": None,
            "poject_type": None,
        }

        self.error_dialog = None
        self.frame = FirstPage(self)

        self.frame.navbtn.next_btn.clicked.connect(self.test)


    def quit_frame(self):
         self.deleteLater()

    def test(self):
        print("test")

    def set_seperator(self) -> None:
        self.user_inputs["separator"] = self.comBoxSep.currentData()

    def set_path(self) -> None:
        self.user_inputs["path"] = self.path_lineEdit.text()

    def set_poject_name(self) -> None:
        self.user_inputs["poject_name"] = self.name_lineEdit.text()

    def set_poject_type(self) -> None:
        self.user_inputs["poject_type"] = self.projectTypeComBox.currentText()

    def set_df_is_valid_to_true(self) -> None:
        if self.check_df_is_valid():
            self.user_inputs["df_is_valid"] = True

    def set_dataframe(self) -> None:
        if not self.check_file():
            return

        try:
            self.user_inputs["dataframe"] = pd.read_csv(self.user_inputs["path"])

        except pd.errors.EmptyDataError:
            print("The File is Empty")
            self.prompt_error_dialog("The File is Empty")

        except pd.errors.ParserError:
            print("An error occured while parseing the file")

        except TypeError:
            print("TypeError")

        except:
            print("An error occured")

    def prompt_error_dialog(self, error: str) -> None:
        self.error_dialog = ErrorDialog(error)
        self.error_dialog.show()

    def set_path_in_line_edit_with_file_browser(self) -> None:
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open file",
            "C:\\Users\\sbues\\VSCode\\python\\Regression\\datasets",  # demo
            "CSV files (*.csv)",
        )[0]
        self.path_lineEdit.setText(filepath)

    def submit_dataframe(self) -> None:
        self.set_path()
        self.set_seperator()
        self.set_dataframe()

        if not self.user_inputs["dataframe"] is None:
            self.check_df_is_valid()
            self.create_table_view()

    def check_df_is_valid(self) -> bool:
        df = self.user_inputs["dataframe"]

        if df is None:
            return False
        elif df.shape[0] <= 2:
            return False
        elif df.shape[1] <= 2:
            return False
        else:
            return True

    def check_file(self) -> bool:
        return os.path.exists(self.user_inputs["path"])

    def create_table_view(self) -> None:
        model = pandasModel(self.user_inputs["dataframe"])
        self.tableView.setModel(model)
        self.tableView.update()

    def create_dataset_object(self) -> None:
        return dataset.Dataset(
            self.user_inputs["dataframe"], self.user_inputs["separator"]
        )

    def check_everything_is_filled_out(self) -> bool:
        for key, item in self.user_inputs.items():
            if key == "df_is_valid":
                if item is False:
                    return False
            else:
                if item is None:
                    return False
        return True

    def save_dataset(self) -> None:
        dataset.save_dataset(
            self.user_inputs["dataframe"],
            self.user_inputs["poject_name"],
            self.user_inputs["separator"],
        )

    def save_settings(self) -> None:
        setting = settings.Setting(
            self.user_inputs["poject_type"],
            self.user_inputs["dataframe"].columns[0],
            self.user_inputs["separator"],
        )
        settings.save_settings(setting, self.user_inputs["poject_name"])

    def accept(self) -> None:
        self.set_poject_name()
        self.set_poject_type()

        if not self.check_everything_is_filled_out():
            print("Please fill all fields")
            return

        self.save_dataset()
        self.save_settings()

        self.done(0)

    def reject(self) -> None:
        self.done(0)


class FirstPage(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent_element = parent
        self.setObjectName("first_page")
        self.setGeometry(QtCore.QRect(10, 10, 500, 500))

        self.user_inputs = {
            "dataframe": None,
            "df_is_valid": False,
            "separator": None,
            "path": None,
            "poject_name": None,
            "poject_type": None,
        }

        self.header = PageHeader(0,0,self)
        self.path_input = PathInput(0, 75, self)
        self.sep_select = SeparatorSelect(0, 265, self)
        self.navbtn = NavButton(200, 450, True, False, self)
        
        self.header.set_quit_btn_signal(self.quit_frame)
        self.path_input.set_signal(self.set_test_num)

        with open("./app/style/new_project_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def quit_frame(self):
         self.parent_element.deleteLater()

    def set_test_num(self):
        self.test_num += 1
        print(self.test_num)

class PageHeader(QtWidgets.QFrame):
    def __init__(self, pos_x: int, pos_y: int, parent = None) -> None:
        super().__init__(parent)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setGeometry(self.pos_x, self.pos_y,500,50)

        self.page_heading = QtWidgets.QLabel("<h1>New Project</h1>", self)
        self.page_heading.setGeometry( 0,0,500,50)
        self.page_heading.setObjectName("page_heading")
        self.page_heading.setAlignment(QtCore.Qt.AlignCenter)

        self.quit_btn = QtWidgets.QPushButton(self)
        self.quit_btn.setGeometry( 470,6,24,24)
        self.quit_btn.setObjectName("quit_btn")
        self.quit_btn.setIcon(QtGui.QIcon('./resources/cross-small.png'))
        self.quit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def set_quit_btn_signal(self, func: Callable):
        self.quit_btn.clicked.connect(func)


class SeparatorSelect(QtWidgets.QFrame):
    def __init__(self, pos_x: int, pos_y: int, parent = None) -> None:
        super().__init__(parent)
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.setGeometry(self.pos_x, self.pos_y,500, 200)
        self.setObjectName("sep_frame")

        self.head = QtWidgets.QLabel("<h1>Separator</h1>", self)
        self.head.setGeometry(190,0,120,50)
        self.head.setObjectName("sep_head")
        

        self.text = QtWidgets.QLabel("Please select the Separator which is used in your file. It is importen to <br> select the correct one otherwise the programm will not be able to read the file!", self)
        self.text.setGeometry(25,25,450,100)
        self.text.setObjectName("sep_text")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.activ_btn_name = None

        self.btn_dict = {
            "sep_coma": [QtWidgets.QPushButton(",", parent), ","],
            "sep_colon": [QtWidgets.QPushButton(":", parent), ":"],
            "sep_semi": [QtWidgets.QPushButton(";", parent), ";"],
            "sep_sub": [QtWidgets.QPushButton("-", parent), "-"],
            "sep_tab": [QtWidgets.QPushButton("Tab", parent), "\t"],
            "sep_space": [QtWidgets.QPushButton("Space", parent), " "]
        }

        self.set_attributs()
        self.style_btn_dict()

    def set_attributs(self) -> None:
        x = 100
        for key, value in self.btn_dict.items():
            value[0].setGeometry(self.pos_x + x, self.pos_y+100,50,25)
            value[0].setObjectName(key)
            value[0].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            value[0].clicked.connect(partial(self.style_activ_btn,key))
            x += 50

    def style_btn_dict(self):
        for _, value in self.btn_dict.items():
            self.style_btn(value[0])

    def style_btn(self, btn):
        x = 1
        if btn.objectName() == "sep_space":
            x=0
        btn.setStyleSheet("QPushButton#"+btn.objectName()+"{background-color: rgb(44,20,165); color: hsl(216, 12%, 54%); border: solid rgb(86, 53, 255); border-width: 0px "+str(x) +"px 0px 0px;}" )

    def activ_btn(self, btn):
        x = 1
        if btn.objectName() == "sep_space":
            x=0
        btn.setStyleSheet("QPushButton#"+btn.objectName()+"{background-color: rgb(65, 42, 181); color: hsl(216, 12%, 54%); border: solid rgb(86, 53, 255); border-width: 0px "+str(x) +"px 0px 0px;}" )

    def style_activ_btn(self, btn_n):
        if not self.activ_btn_name is None:
            self.style_btn(self.btn_dict[self.activ_btn_name][0])

        self.activ_btn(self.btn_dict[btn_n][0])
        self.activ_btn_name = btn_n
        print(self.activ_btn_name)


class PathInput(QtWidgets.QFrame):
    def __init__(self, pos_x: int, pos_y: int, parent = None) -> None:
        super().__init__(parent)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.setGeometry(self.pos_x, self.pos_y,500, 200)

        self.head = QtWidgets.QLabel("<h1>Path</h1>", self)
        self.head.setGeometry(200,0,100,50)
        self.style_head()

        self.text = QtWidgets.QLabel("Please enter the path to the file with which you want to train the model.<br>Only .csv and .txt files are aloud and make sure all values are separated correctly<br> and each row has only one datatype", self)
        self.style_text()

        self.line_edit = QtWidgets.QLineEdit(self)
        self.style_line_edit()
        
        self.browse_btn = QtWidgets.QPushButton("Browes", self)
        self.style_browse_btn()

    def style_head(self):
        self.head.setObjectName("path_head")
        self.head.setGeometry(200,0,100,50)
        self.head.setAlignment(QtCore.Qt.AlignCenter)
        self.head.setFont(QtGui.QFont("roboto-regular",10))

        
    def style_text(self):
        self.text.setGeometry(25,50,450,40)
        self.text.setObjectName("path_text")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setFont(QtGui.QFont("roboto-regular",8))


    def style_line_edit(self):
        self.line_edit.setGeometry(50,110, 400, 25)
        self.line_edit.setObjectName("path_line_edit")
        self.line_edit.setPlaceholderText("PATH")
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setFont(QtGui.QFont("roboto-regular",8))
        self.line_edit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

    def style_browse_btn(self):
        self.browse_btn.setGeometry( 220, 145, 60, 25)
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.setFont(QtGui.QFont("roboto-regular",8))
        self.browse_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def set_signal(self, func):
        self.browse_btn.clicked.connect(func)


class NavButton():
    def __init__(self, pos_x: int, pos_y: int, has_next: bool, has_previous: bool, parent = None) -> None:
        self.has_previous = has_previous
        self.has_next = has_next

        self.pos_x = pos_x
        self.pos_y = pos_y

        if self.has_next:
            self.next_btn = QtWidgets.QPushButton("Next", parent)
            self.next_btn.setGeometry(self.pos_x, self.pos_y, 100, 25)
            self.next_btn.setObjectName("next_btn")
            self.next_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        if self.has_previous:
            self.back_btn = QtWidgets.QPushButton("Back", parent)
            self.back_btn.setGeometry(self.pos_x, self.pos_y, 100, 25)
            self.back_btn.setObjectName("back_btn")
            self.back_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        if self.has_next and self.has_previous:
            self.next_btn.setGeometry(self.pos_x, self.pos_y, 100, 25)
            self.back_btn.setGeometry(self.pos_x + 100, self.pos_y, 100, 25)

    def set_next_signal(self, methode):
        self.next_btn.clicked.connect(methode)


class pandasModel(QtCore.QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent=None) -> None:
        QtCore.QAbstractTableModel.__init__(self)
        self.dataframe = dataframe

    def rowCount(self, parent=None) -> int:
        return self.dataframe.shape[0]

    def columnCount(self, parent=None) -> int:
        return self.dataframe.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole) -> str:
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self.dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.dataframe.columns[col]
        return None


class ErrorDialog(QtWidgets.QFrame):
    def __init__(self, error: str, parent=None) -> None:
        super().__init__(parent)
        self.parent_element = parent

        self.setFixedSize(450, 50)
        # self.setWindowIcon(QtGui.QIcon(os.path.join(PATH, ".." ,"resources", "ai-icon-9.png" )))
        # self.setWindowTitle("Error")

        self.error_label = QtWidgets.QLabel(error, self)

        self.error_label.show()
        self.error_label.setStyleSheet("QLabel{}")

        path = os.path.join(PATH, "..", "resources", "error-icon-.png")

        self.error_icon_label = QtWidgets.QLabel(self)
        self.error_icon_label.setPixmap(QtGui.QPixmap(path))
        self.error_icon_label.setStyleSheet("QLabel{margin:0px 0px 0px 50px;}")

        self.error_icon_label.show()
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.error_icon_label)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.error_label)


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    window = ErrorDialog("test")
    window.show()

    sys.exit(root.exec())




