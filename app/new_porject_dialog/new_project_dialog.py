from __future__ import annotations
# from PyQt6 import QtCore, QtGui, QtWidgets

from components import *
from functools import partial
from typing import Callable
import pandas as pd
import dataset
import settings
import os
import sys


WHITE = "rgb(255,255,255)"
LIGHT_GREY = "hsl(217, 12%, 63%)"
MEDIUM_GREY = "hsl(216, 12%, 54%)"
DARK_GREY = "hsl(213, 19%, 18%)"
VERY_LIGHT_BLUE = "hsl(217, 12%, 80%)"
LIGHT_BLUE = "hsl(250, 100%, 60%)"
MEDIUM_BLUE = "hsl(249,78%,36%)"
DARK_BLUE = "hsl(250, 78%, 22%)"
VERY_DARK_BLUE = "hsl(216, 12%, 8%)"


PATH = os.path.dirname(__file__)


class NewProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(500, 550)

        self.frame = PageContend(self)
        self.frame.set_quit_dialog(self.quit_dialog)

    def create_table_view(self) -> None:
        model = pandasModel(self.user_inputs["dataframe"])
        tb = QtWidgets.QTableView()
        self.tableView.setModel(model)
        self.tableView.update()


    def mousePressEvent(self, event):
        if event.position().toPoint().y() < 50:
            self.oldPos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.position().toPoint().y() < 50:
            delta = QtCore.QPoint(event.position().toPoint() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event):
        if event.position().toPoint().y() < 50:
            self.oldPos = event.position().toPoint()

    def quit_dialog(self):
        self.close()

    def expand_width(self):
        self.resize(1250, 520)

    def standart_width(self):
        self.resize(500, 520)

    # def resizeEvent(self, event) -> None:
    #     self.height = event.size().height()
    #     self.width = event.size().width()
    #     self.frame.resize(self.width, self.height)


class PageContend(QtWidgets.QFrame):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("page_content")
        self.setGeometry(QtCore.QRect(0, 0,500, 550))

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("page_v_layout")
        self.vertical_layout.setContentsMargins(0, 0, 0, 25)
        self.vertical_layout.setSpacing(25)

        self.user_inputs = {
            "dataframe":  None,
            "separator": None,
            "path": None,
            "df_is_valid": False,
            "columns_to_ignore": None,
            "poject_name": None,
            "poject_type": None,
        }

        self._current_page = 0

        self.header = PageHeader()
        self.vertical_layout.addWidget(self.header)

        self.quit_btn = QuitButton("quit", self)
        self.quit_btn.setGeometry(470, 6, 24, 24)

        self.pages: list[list[InputContainer]] = [
            [PathInput("path"), SeparatorInput("separator")],
            [DataframeCheck("columns_to_ignore", 500, self.get_dataframe)],
            [NameInput("poject_name"), None]
            ]
        
        

        self.nav_bar = NavButtonFrame(3, self)
        self.vertical_layout.addWidget(self.nav_bar)
        self.nav_bar.connect_back_btn(self.back_page) 
        self.nav_bar.connect_next_btn(self.next_page)

        self.set_style()
        self.load_page()

    def set_path(self, path: str) -> None:
        self.user_inputs["path"] = path

    def set_seperator(self, separator: str) -> None:
        self.user_inputs["separator"] = separator

    def set_poject_name(self, poject_name: str) -> None:
        self.user_inputs["poject_name"] = poject_name

    def set_poject_type(self, poject_type: str) -> None:
        self.user_inputs["poject_type"] = poject_type

    def set_df_is_valid(self) -> None:
        if self.check_df_is_valid():
            self.user_inputs["df_is_valid"] = True

    def set_dataframe(self, dataframe: pd.DataFrame):
        self.user_inputs["dataframe"] = dataframe

    def get_dataframe(self) -> pd.DataFrame:

        return self.user_inputs["dataframe"]

    def set_columns_to_ignore(self, columns_to_ignore: list[str]):
        self.user_inputs["columns_to_ignore"] = columns_to_ignore
        
    def create_dataframe(self) -> pd.DataFrame | None:

        if self.check_file():
            try:
                return pd.read_csv(self.user_inputs["path"], sep=self.user_inputs["separator"])
            except pd.errors.EmptyDataError:
                print("The File is Empty")
            except pd.errors.ParserError:
                print("An error occured while parseing the file")
            except TypeError:
                print("TypeError")
            except:
                print("An error occured")
        return None

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

    def create_dataset_object(self) -> dataset.Dataset:
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

    def submit_page_inputs(self) -> None:
        for element in self.pages[self._current_page]:
            self.user_inputs[element.get_input_key()] = element.get_input()

    def check_current_page_inputs(self) -> bool:
        for element in self.pages[self._current_page]:
            if not self.user_inputs[element.get_input_key()]:
                return False
        return True

    def load_page(self) -> None:
        for widget in self.pages[self._current_page]:
            if widget is None:
                continue
            
            self.vertical_layout.insertWidget(
                self.vertical_layout.count()-1, widget
            )
            widget.show()

    def hide_page(self) -> None:
        for widget in self.pages[self._current_page]:
            if widget is None:
                continue

            print(widget.get_input_key())
            self.vertical_layout.removeWidget(widget)
            widget.hide()

    def append_collumns_to_dataframe_check_frame(self):
        self.pages[1][0].append_columns(
            self.user_inputs["dataframe"].columns
        )

    def next_page(self) -> None:
        self.submit_page_inputs()
        if self.check_current_page_inputs():
            self.hide_page()
            self._current_page += 1
            self.load_page()

    def back_page(self) -> None:
        self.hide_page()
        self._current_page -= 1
        self.load_page()

    def set_quit_dialog(self, func: Callable) -> None:
        self.quit_btn.clicked.connect(func)

    def finish(self) -> None:
        self.save_dataset()
        self.save_settings()

    # def resizeEvent(self, event) -> None:
    #     self.quit_btn.move(event.size().width() - 30, 6)

    def set_style(self):
        self.setStyleSheet(
            f"""QFrame#{self.objectName()}{{  
                border-top-left-radius: 25px; 
                border-bottom-right-radius:25px; 
                background-color: hsl(213, 19%, 10%);  }}"""
        )


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
    root = QtWidgets.QApplication(sys.argv)
    window = NewProjectDialog()

    window.show()
    sys.exit(root.exec())
