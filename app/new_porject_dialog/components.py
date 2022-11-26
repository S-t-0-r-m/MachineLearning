from app.new_porject_dialog.elements import *
from typing import Callable, Protocol


class InputContainer(Protocol):

    def get_input(self) -> str | None:
        """
        Return the input the user has entered, if no value has
        been set yet it returns 'None'
        """
        ...
    
    def get_input_key(self) -> str:
        """
        Returns the key to the input Dictionary, where the value 
        should be stored in.
        """
        ...

    def show(self) -> None:
        """
        Makes the Widget Visibel
        """
        ...

    def hide(self) -> None:
        """
        Hides the Widget
        """
        ...


class PathInput(QtWidgets.QWidget):
    def __init__(self, key: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("path_input_container")
        self.input_key: str = key

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("path_v_layout")
        self.vertical_layout.setSpacing(15)

        self.head = ElementHeading("path_head", "Path")

        self.text = ElementText(
            "path_text",
            "Please enter the path to the file with which you want to train the model.<br>Only .csv and .txt files are aloud and make sure all values are separated correctly<br> and each row has only one datatype")

        self.path_line_edit = ElementLineEdit("path")

        self.browse_btn = ElementButton("browes")

        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.addWidget(self.path_line_edit)
        self.vertical_layout.addWidget(self.browse_btn)

        self.vertical_layout.setAlignment(
            self.path_line_edit, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.setAlignment(
            self.browse_btn, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.browse_btn.clicked.connect(
            self.set_path_in_line_edit_with_file_browser)

        self.hide()

    def set_path_in_line_edit_with_file_browser(self) -> None:
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Open file",
            "C:\\Users\\sbues\\VSCode\\python\\Regression\\datasets",  # demo
            "CSV, Txt Files (*.csv , *.txt)",
        )[0]
        if filepath:
            self.path_line_edit.setText(filepath)

    def get_input_key(self):
        return self.input_key

    def get_input(self) -> str:
        return self.path_line_edit.text()


class SeparatorInput(QtWidgets.QWidget):
    def __init__(self, key: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sep_input_container")
        self.input_name: str = key

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("sep_v_layout")
        self.vertical_layout.setSpacing(15)

        self.head = ElementHeading(
            "sep_head", "Separator"
        )

        self.text = ElementText(
            "sep_text",
            "Please select the Separator which is used in your file. It is importen to <br> select the correct one otherwise the programm will not be able to read the file!",
        )

        self.sep_input = RadioButtonsGroup(
            "sep",
            {
            "sep_coma": [RadioButton("coma", ",", is_first=True), ","],
            "sep_colon": [RadioButton("colon", ":", ), ":"],
            "sep_semi": [RadioButton("semi", ";"), ";"],
            "sep_sub": [RadioButton("sub", "-"), "-"],
            "sep_tab": [RadioButton("tab", "Tab"), "\t"],
            "sep_space": [RadioButton("space", "Space", is_last=True), " "],
            }
        )

        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.addWidget(self.sep_input)

        self.hide()

    def get_input_key(self):
        return self.input_name

    def get_input(self):
        return self.sep_input.get_current_value()


class DataframeCheck(QtWidgets.QWidget):
    def __init__(self, key, w, get_func, parent=None) -> None:
        super().__init__(parent)
        self.hide()
        self.setObjectName("DataframeCheck_input_container")
        self.setContentsMargins(0,0,0,0)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("DataframeCheck_v_layout")
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(15)


        self.get_func = get_func
        self.input_key = key
        self.column_list: list[str] = None

        self.head = ElementHeading("df_head", "Dataframe")

        self.text = ElementText("df_text",
                                "Please verify that the programm read and parsed the file correctly.\n Also make sure that it meets the following criterias: \n\n- Exampels with missing data will be ignored  \n- More than one column \n- More than one row \n- Each row has only one datatype"
                                )

        self.col_area = CheckButtonScrollArea(w)

        self.head.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.text.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.addWidget(self.col_area)
    
    # def show(self) -> None:
    #     self.append_columns(self.get_func())
    #     return super().show()

    def get_input_key(self):
        return self.input_key

    def append_columns(self, col_list: list[str]):
        self.col_area.fill_layout([CheckButton(name) for name in col_list])

    def get_input(self):
        return self.col_area.get_input()


class NameInput(QtWidgets.QWidget):
    def __init__(self, key: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("name_input_container")

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setObjectName("name_input_v_layout")
        self.vertical_layout.setSpacing(15)

        self.input_key: str = key

        self.head = ElementHeading("name_head", "Project Name")

        self.text = ElementText(
            "name_text",
            "Please give your project a name"
        )

        self.vertical_layout.addWidget(self.head)
        self.vertical_layout.addWidget(self.text)

        self.hide()

    def get_input_key(self):
        return self.input_key

    def get_input(self):
        return "None"

class NavButtonFrame(QtWidgets.QFrame):
    def __init__(self, next_list: list[None | Callable], parent=None, ) -> None:
        super().__init__(parent)
        self.setMinimumSize(250, 25)

        self.next_list = next_list

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("NavButtonFrame_h_layout")
        self.horizontal_layout.setContentsMargins(100, 0, 100, 0)

        self.next_btn = NextNavButton("next_btn", "Next", self)
        self.back_btn = BackNavButton("back_btn", "Back", self)

        self.nr_of_pages = len(next_list)

    def next_page(self):

        self.next_btn.set_text(self.current_page, self.nr_of_pages)
        self.next_btn.exe_aux_functions(self.current_page)
        self.back_btn.set_visibiltiy(self.current_page)

    def page_back(self):

        self.next_btn.set_text(self.current_page, self.nr_of_pages)
        self.back_btn.set_visibiltiy(self.current_page)

    def connect_next_btn(self, methode: Callable):
        self.next_btn.clicked.connect(methode)

    def connect_back_btn(self, methode: Callable):
        self.back_btn.clicked.connect(methode)

class PageContent(Protocol):
    pass

class PathSeparatorPage():
    pass
