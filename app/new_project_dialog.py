from mimetypes import init
import dataset
import settings
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pandas as pd
import os
import sys

light_grey = "hsl(217, 12%, 63%)"
medium_grey = "hsl(216, 12%, 54%)"
dark_blue = "hsl(213, 19%, 18%)"
very_dark_blue = "hsl(216, 12%, 8%)"
orange = "hsl(25, 97%, 53%)"

PATH = os.path.dirname(__file__)


class NewProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent_element = parent

        uic.loadUi(f"{PATH}/ui/new_project_dialog.ui", self)
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(PATH, "..", "resources", "ai-icon-9.png"))
        )

        self.resize(1300, 500)

        self.user_inputs = {
            "dataframe": None,
            "df_is_valid": False,
            "separator": None,
            "path": None,
            "poject_name": None,
            "poject_type": None,
        }

        self.comBoxSep.setItemData(0, ",")
        self.comBoxSep.setItemData(1, ";")
        self.comBoxSep.setItemData(2, ":")
        self.comBoxSep.setItemData(3, "\t")
        self.comBoxSep.setItemData(4, " ")
        self.comBoxSep.setItemData(5, "-")

        self.error_dialog = None
        self.left_frame = FirstPage(self)

        self.submitbtn.clicked.connect(self.submit_dataframe)
        self.btnBrowse.clicked.connect(self.set_path_in_line_edit_with_file_browser)

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
        self.setObjectName("first_page")
        self.setGeometry(QtCore.QRect(700, 10, 500, 500))

        self.quit_btn = QtWidgets.QPushButton(self)
        self.quit_btn.setGeometry( 460,10,24,24)
        self.quit_btn.setObjectName("quit_btn")

        self.page_heading = QtWidgets.QLabel("<h1>New Project</h1>", self)
        self.page_heading.setGeometry( 150,0,200,50)
        self.page_heading.setObjectName("page_heading")
        self.page_heading.setAlignment(QtCore.Qt.AlignCenter)

        self.path_text =  QtWidgets.QLabel("<h1>Path</h1> Please enter the path to the file with wiches you want to train the model.<br>Only .csv and .txt files are aloud and make sure all values are separated by a separator<br> and each row has only one datatype", self)
        self.path_text.setGeometry(25,50,450,100)
        self.path_text.setObjectName("path_text")
        self.path_text.setAlignment(QtCore.Qt.AlignCenter)

        self.path_input = PathInput(50, 175, self)

        self.sep_text = QtWidgets.QLabel("<h1>Separator</h1> Please select the Separator wichts is use to separat the values in your file. It is importen to <br> select the correct one outherwise the program will not be abel to read the file ", self)
        self.sep_text.setGeometry(25,260,450,100)
        self.sep_text.setObjectName("sep_text")
        self.sep_text.setAlignment(QtCore.Qt.AlignCenter)

        self.sep_select = SeparatorSelect(100, 375, self)

        self.navbtn = NavButton(200, 450, True, False, self)
        
        with open(os.path.join(PATH,"style","new_project_style.txt") ,"r") as fh:
            self.setStyleSheet(fh.read())


class SeparatorSelect():
    def __init__(self, pos_x: int, pos_y: int, parent = None) -> None:

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.rad_btn_dict = {
            "coma": [QtWidgets.QRadioButton("     ,", parent), ","],
            "colon": [QtWidgets.QRadioButton("     :", parent), ":"],
            "semi": [QtWidgets.QRadioButton("     ;", parent), ";"],
            "sub": [QtWidgets.QRadioButton("     -", parent), "-"],
            "tab": [QtWidgets.QRadioButton("   Tab", parent), "\t"],
            "space": [QtWidgets.QRadioButton(" Space", parent), " "]
        }

        self.set_position()


    def set_position(self) -> None:
        for key, value in self.rad_btn_dict.items():
            value[0].setGeometry(self.pos_x, self.pos_y,50,25)
            value[0].setObjectName(key)
            self.pos_x += 50

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
        
        if self.has_previous:
            self.back_btn = QtWidgets.QPushButton("Back", parent)
            self.back_btn.setGeometry(self.pos_x, self.pos_y, 100, 25)
            self.back_btn.setObjectName("back_btn")
        
        if self.has_next and self.has_previous:
            self.next_btn.setGeometry(self.pos_x, self.pos_y, 100, 25)
            self.back_btn.setGeometry(self.pos_x + 100, self.pos_y, 100, 25)


class PathInput:
    def __init__(self, pos_x: int, pos_y: int, parent = None) -> None:

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.line_edit = QtWidgets.QLineEdit(parent)
        self.line_edit.setGeometry(self.pos_x, self.pos_y, 400, 25)
        self.line_edit.setObjectName("line_edit")
        self.line_edit.setPlaceholderText("PATH")
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)

        self.browse_bnt = QtWidgets.QPushButton("Browes", parent)
        self.browse_bnt.setGeometry(self.pos_x + 170, self.pos_y+ 40, 60, 25)
        self.browse_bnt.setObjectName("browse_bnt")


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




