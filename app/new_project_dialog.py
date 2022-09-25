from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from typing import Callable
import pandas as pd
import dataset
import settings
import os
import sys

PAGE_HEIGHT = 1500
PAGE_WIDTH = 1500


very_light_blue = "hsl(217, 12%, 80%)"
light_grey = "hsl(217, 12%, 63%)"
medium_grey = "hsl(216, 12%, 54%)"
dark_blue = "hsl(213, 19%, 18%)"
very_dark_blue = "hsl(216, 12%, 8%)"
orange = "hsl(25, 97%, 53%)"


PATH = os.path.dirname(__file__)


class NewProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
    
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(500, 500)

        self.frame =PageContend(self)
        self.frame.set_quit_dialog(self.quit_dialog)


    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.old_positon = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        delta = QtCore.QPoint(event.globalPos()) - self.old_positon
        self.move(self.x( ) + delta.x(), self.y( ) + delta.y())
        self.old_positon = event.globalPos()
        return super().mouseMoveEvent(event)

    def quit_dialog(self):
        self.deleteLater()
    
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.frame.resize(event.size().width() ,event.size().height())
        return super().resizeEvent(event)


    


class PageContend(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("first_page")
        self.setGeometry(QtCore.QRect(0, 0, 500, 500))
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("page_v_layout")
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)

        self.user_inputs = {
            "dataframe": None,
            "df_is_valid": False,
            "separator": None,
            "path": None,
            "poject_name": None,
            "poject_type": None,
        }

        self.current_page = 0

        self.header = PageHeader(self)
        self.vertical_layout.addWidget(self.header)

        self.pages =[
            [PathInput(self), SeparatorSelect( self), NavNextButton(self)],
            [None, NavButtonFrame(self)],
            [None, None, NavBackButton(self)]
        ]

        self.pages[0][2].clicked.connect(self.submit_dataframe)
        self.pages[1][1].connect_next_signal(self.next_page)
        self.pages[1][1].connect_back_signal(self.back_page)
        self.pages[2][2].clicked.connect(self.back_page)
        
        with open("./app/style/new_project_style.qss", "r") as file:
            self.setStyleSheet(file.read())

        self.hide_all_widgets()
        self.load_page()

    def set_path(self) -> None:
        self.user_inputs["path"] = self.pages[0][0].get_input()

    def set_seperator(self) -> None:
        self.user_inputs["separator"] = self.pages[0][1].get_input()
    
    def set_poject_name(self) -> None:
        self.user_inputs["poject_name"] = self.name_lineEdit.text()

    def set_poject_type(self) -> None:
        self.user_inputs["poject_type"] = self.projectTypeComBox.currentText()

    def set_df_is_valid_to_true(self) -> None:
        if self.check_df_is_valid():
            self.user_inputs["df_is_valid"] = True

    def set_df_is_valid_to_true(self) -> None:
        if self.check_df_is_valid():
            self.user_inputs["df_is_valid"] = True

    def submit_dataframe(self) -> None:
        self.set_path()
        self.set_seperator()
        self.set_dataframe()

        if not self.user_inputs["dataframe"] is None:
            self.next_page()

            # self.check_df_is_valid()
            # self.create_table_view()

    def set_dataframe(self) -> None:
        if not self.check_file():
            return

        try:
            self.user_inputs["dataframe"] = pd.read_csv(self.user_inputs["path"])
        except pd.errors.EmptyDataError:
            print("The File is Empty")
        except pd.errors.ParserError:
            print("An error occured while parseing the file")
        except TypeError:
            print("TypeError")
        except:
            print("An error occured")
    
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

    def check_file(self) -> bool:
        return os.path.exists(self.user_inputs["path"])
    
    def prompt_error_dialog(self, error: str) -> None:
        self.error_dialog = ErrorDialog(error)
        self.error_dialog.show()

    def load_page(self):
        for widget in self.pages[self.current_page]:
            if widget is None: continue
            self.vertical_layout.addWidget(widget)
            # self.vertical_layout.setAlignment(widget, QtCore.Qt.AlignCenter)
            widget.show()

    def hide_all_widgets(self):
        for page in self.pages:
            self.hide_page(page)

    def hide_page(self, page):
        for widget in page:
            if widget is None: continue
            widget.hide()
    
    def next_page(self):
        self.hide_page(self.pages[self.current_page])
        self.current_page += 1
        self.load_page()

    def back_page(self):
        self.hide_page(self.pages[self.current_page])
        self.current_page -= 1
        self.load_page()
    
    def set_quit_dialog(self, func: Callable):
        self.header.set_quit_btn_signal(func)
    
    def finish(self) -> None:
        self.set_poject_name()
        self.set_poject_type()

        if not self.check_everything_is_filled_out():
            print("Please fill all fields")
            return

        self.save_dataset()
        self.save_settings()


class PageHeader(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("page_header")

        self.setMinimumSize(500,50)

        self.page_heading = QtWidgets.QLabel("New Project", self)
        self.page_heading.setGeometry(0, 0, 500, 50)
        self.page_heading.setObjectName("page_heading")
        self.page_heading.setAlignment(QtCore.Qt.AlignCenter)

        self.quit_btn = QtWidgets.QPushButton(self)
        self.quit_btn.setGeometry(470, 6, 24, 24)
        self.quit_btn.setObjectName("quit_btn")
        self.quit_btn.setIcon(QtGui.QIcon("./resources/cross-small.png"))
        self.quit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def set_quit_btn_signal(self, func: Callable) -> None:
        self.quit_btn.clicked.connect(func)


class PathInput(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("path_frame")
        
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("path_v_layout")
        self.vertical_layout.setSpacing(15)

        self.head = QtWidgets.QLabel("Path", self)
        self.head.setObjectName("path_head")
        self.head.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.setAlignment(self.head, QtCore.Qt.AlignCenter)

        self.text = QtWidgets.QLabel(
            "Please enter the path to the file with which you want to train the model.<br>Only .csv and .txt files are aloud and make sure all values are separated correctly<br> and each row has only one datatype",
            self,)
        self.text.setObjectName("path_text")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.setAlignment(self.text, QtCore.Qt.AlignCenter)

        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.setMaximumWidth(450)
        self.line_edit.setMinimumSize(450, 25)
        self.line_edit.setObjectName("path_line_edit")
        self.line_edit.setPlaceholderText("PATH")
        self.line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.line_edit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.vertical_layout.addWidget(self.line_edit)
        self.vertical_layout.setAlignment(self.line_edit, QtCore.Qt.AlignCenter)
        
        self.browse_btn = QtWidgets.QPushButton("Browse", self)
        self.browse_btn.setMaximumWidth(100)
        self.browse_btn.setMinimumSize(100, 25)
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.vertical_layout.addWidget(self.browse_btn)
        self.vertical_layout.setAlignment(self.browse_btn, QtCore.Qt.AlignCenter)

        self.browse_btn.clicked.connect(self.set_path_in_line_edit_with_file_browser)

    def get_input(self)-> str:
        return self.line_edit.text()

    def set_path_in_line_edit_with_file_browser(self) -> None:
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open file",
            "C:\\Users\\sbues\\VSCode\\python\\Regression\\datasets",  # demo
            "CSV files (*.csv)",
        )[0]
        if filepath:
            self.line_edit.setText(filepath)


class SeparatorSelect(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sep_frame")

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("sep_v_layout")
        self.vertical_layout.setSpacing(15)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding) #

        self.head = QtWidgets.QLabel("Separator", self)
        self.head.setAlignment(QtCore.Qt.AlignCenter)
        self.head.setObjectName("sep_head")

        self.text = QtWidgets.QLabel(
            "Please select the Separator which is used in your file. It is importen to <br> select the correct one otherwise the programm will not be able to read the file!",
            self,
        )
        self.text.setObjectName("sep_text")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.sep_input = SeparatorButtonsFrame()

        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.addWidget(self.sep_input)
        self.head.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum) #

        # self.vertical_layout.setAlignment(self.head, QtCore.Qt.AlignCenter)
        # self.vertical_layout.setAlignment(self.text, QtCore.Qt.AlignCenter)
        # self.vertical_layout.setAlignment(self.sep_input, QtCore.Qt.AlignCenter)
        self.text.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum) #

    def get_input(self):
        return self.sep_input.get_current_sep()


class SeparatorButtonsFrame(QtWidgets.QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("sep_btn_frame")
        # self.setMaximumSize(400, 25)
        self.setMinimumSize(400,50)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("sep_h_layout")
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding) #

        # self.horizontal_layout.addItem(QtWidgets.QSpacerItem(
        #     40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        # ))

        self.activ_btn_name = None
        self.btn_dict = {
            "sep_coma": [QtWidgets.QPushButton(",", self), ","],
            "sep_colon": [QtWidgets.QPushButton(":", self), ":"],
            "sep_semi": [QtWidgets.QPushButton(";", self), ";"],
            "sep_sub": [QtWidgets.QPushButton("-", self), "-"],
            "sep_tab": [QtWidgets.QPushButton("Tab", self), "\t"],
            "sep_space": [QtWidgets.QPushButton("Space", self), " "],
        }


        self.set_attributs()
        self.style_btn_dict()

        # self.horizontal_layout.addItem(QtWidgets.QSpacerItem(
        #     40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        # ))

    def sizeHint(self):
        return QtCore.QSize(400, 50) 

    def get_current_sep(self) -> str:
        return self.activ_btn_name

    def set_attributs(self)-> None:
        for key, value in self.btn_dict.items():
            button = value[0]

            # button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding) #
            button.setMinimumSize(50, 25)
            button.setObjectName(key)
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            button.clicked.connect( partial( self.style_activ_btn, key))
            self.horizontal_layout.addWidget(button)
            # self.horizontal_layout.setAlignment(button, QtCore.Qt.AlignHCenter)

    def style_btn_dict(self)-> None:
        for _, value in self.btn_dict.items():
            self.style_btn(value[0])

    def style_btn(self, btn)-> None:
        x = 1
        if btn.objectName() == "sep_space":
            x = 0
        btn.setStyleSheet(
            "QPushButton#"
            + btn.objectName()
            + "{background-color: rgb(44,20,165); color: hsl(216, 12%, 54%); border: solid rgb(86, 53, 255); border-width: 0px"
            + str(x)
            + "px 0px 0px; }"
        )

    def activ_btn(self, btn)-> None:
        x = 1
        if btn.objectName() == "sep_space":
            x = 0
        btn.setStyleSheet(
            "QPushButton#"
            + btn.objectName()
            + "{background-color: hsl(250, 78%, 20%); color: hsl(217, 12%, 80%); border: solid rgb(86, 53, 255); border-width: 0px "
            + str(x)
            + "px 0px 0px;}"
        )

    def style_activ_btn(self, btn_n)-> None:
        if not self.activ_btn_name is None:
            self.style_btn(self.btn_dict[self.activ_btn_name][0])

        self.activ_btn(self.btn_dict[btn_n][0])
        self.activ_btn_name = btn_n

class DataframeCheck(QtWidgets.QFrame):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)


class NavNextButton(QtWidgets.QPushButton):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setText("Next")
        self.setObjectName("next_btn")
        # self.setMinimumSize(100,25)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
    
 
class NavBackButton(QtWidgets.QPushButton):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setText("Back")
        self.resize(100,25)
        self.setMinimumSize(100, 25)
        self.setMaximumSize(100,25)
        self.setObjectName("back_btn")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


class NavButtonFrame(QtWidgets.QFrame):
    def __init__(self,  parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(250, 25)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("NavButton_h_layout")
        self.horizontal_layout.setContentsMargins(0,0,0,0)

        self.next_btn = NavNextButton(self)
        self.back_btn = NavBackButton(self)

        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.next_btn)

    def connect_next_signal(self, methode):
        self.next_btn.clicked.connect(methode)

    def connect_back_signal(self, methode):
        self.back_btn.clicked.connect(methode)


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
    print(root.devicePixelRatio())
    window = ErrorDialog("test")
    window.show()

    sys.exit(root.exec())
