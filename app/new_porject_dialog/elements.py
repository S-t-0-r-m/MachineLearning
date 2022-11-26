from __future__ import annotations
from PyQt6 import QtCore, QtGui, QtWidgets
from functools import partial

import pandas as pd


WHITE = "rgb(255,255,255)"
LIGHT_GREY = "hsl(217, 12%, 63%)"
MEDIUM_GREY = "hsl(216, 12%, 54%)"
DARK_GREY = "hsl(213, 19%, 18%)"
VERY_LIGHT_BLUE = "hsl(217, 12%, 80%)"
LIGHT_BLUE = "hsl(250, 100%, 60%)"
MEDIUM_BLUE = "hsl(249,78%,36%)"
DARK_BLUE = "hsl(250, 78%, 22%)"
VERY_DARK_BLUE = "hsl(216, 12%, 8%)"


class QuitButton(QtWidgets.QPushButton):
    def __init__(self, name: str,  parent=None) -> None:
        super().__init__(parent)
        self.setObjectName(f"{name}_btn")
        self.setIcon(QtGui.QIcon(r"./resources/cross-small.png"))
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor))

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"""QPushButton#{self.objectName()}{{
                border-radius: 12px;
                border: solid white;
                border-width: 1px 1px 1px 1px;
                qproperty-iconSize: 24px;}}"""

            f"""QPushButton#{self.objectName()}:hover{{
                background-color: red;}}"""
        )


class PageHeader(QtWidgets.QLabel):
    def __init__(self,  parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("page_header")
        self.setText("New Project")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.font_size = "30"

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"""QLabel#{self.objectName()}{{
                font-weight:bold;
                font-size: {self.font_size}pt;
                color: white;
                border-top-left-radius: 25px;
                background-color: hsl(213, 19%, 18%); }}"""
        )


class ElementLineEdit(QtWidgets.QLineEdit):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setMinimumSize(450, 25)
        self.setObjectName(f"{name}_line_edit")
        self.setPlaceholderText("PATH")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.IBeamCursor)
        )

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"""QLineEdit#{self.objectName()}{{
                    background-color: rgb(44, 20, 165);
                    border-radius: 12px;
                    color: hsl(216, 12%, 54%);}}"""
        )


class ElementButton(QtWidgets.QPushButton):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 25)
        self.setObjectName(f"{name}_btn")
        self.setText(name.capitalize())
        self.setCursor(QtGui.QCursor(
            QtCore.Qt.CursorShape.PointingHandCursor))

        self.set_style()

    def set_style(self):
        # hsl(213, 19%, 18%)
        self.setStyleSheet(
            f"""QPushButton#{self.objectName()}{{
                background-color: rgb(44, 20, 165);
                border-radius: 12px;
                color: hsl(216, 12%, 54%);}}"""
        )


class ElementHeading(QtWidgets.QLabel):
    def __init__(self, obj_name, text, font_size: int = 30, parent=None, ) -> None:
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(f"{obj_name}_heading")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.font_size: int = font_size

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"""QLabel#{self.objectName()}{{  
                font-weight:bold;
                font-size: 20pt;
                color: hsl(217, 12%, 80%); }}"""
        )


class ElementText(QtWidgets.QLabel):
    def __init__(self, obj_name, text, parent=None, ) -> None:
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(f"{obj_name}")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"""QLabel#{self.objectName()}{{
                text-align: center;
                color: hsl(216, 12%, 54%); }}"""
        )


class RadioButtonsGroup(QtWidgets.QFrame):
    def __init__(self, name, btn_dict: dict[RadioButton], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName(f"{name}_radio_btn_group")

        self.setMinimumSize(400, 50)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setObjectName("sep_h_layout")
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)

        self.activ_btn_name = None

        self.btn_dict = btn_dict

        for _, value in self.btn_dict.items():
            btn = value[0]
            self.add_btns_to_layout(btn)
            self.set_onclick(btn)

        self.set_style()

    def get_current_value(self) -> str:
        if not self.activ_btn_name is None:
            return self.btn_dict[self.activ_btn_name][1]
        else:
            return None

    def set_onclick(self, btn):
        btn.clicked.connect(partial(self.toggle_buttons, btn.objectName()))

    def add_btns_to_layout(self, btn) -> None:
        self.horizontal_layout.addWidget(btn)

    def toggle_buttons(self, name):
        if not self.activ_btn_name is None:
            self.btn_dict[self.activ_btn_name][0].deactivate_button()

        self.btn_dict[name][0].activate_button()
        self.activ_btn_name = name

    def set_style(self):
        self.setStyleSheet(f"""QFrame#{self.objectName()}{{
            margin:0px 50px 0px 50px;
        }}""")


class RadioButton(QtWidgets.QPushButton):
    def __init__(self, obj_name, text, parent=None, is_first=False, is_last=False) -> None:
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(f"sep_{obj_name}")
        self.setMinimumSize(50, 25)
        self.setMinimumHeight(25)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.is_first = is_first
        self.is_last = is_last
        self.is_active = False
        self.color = LIGHT_GREY
        self.bg_color = MEDIUM_BLUE
        self.font_weight = "normal"

        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"QPushButton#{self.objectName()}{{background-color: {self.bg_color}; color: {self.color}; font-weight: {self.font_weight}; {self.get_border_style()} {self.get_radius_style()} }}")

    def get_radius_style(self):
        if self.is_first:
            return "border-top-left-radius: 12px; border-bottom-left-radius: 12px;"
        elif self.is_last:
            return "border-top-right-radius: 12px; border-bottom-right-radius: 12px;"
        else:
            return ""

    def get_border_style(self):
        if not self.is_active:
            if self.is_last:
                return "border: none;"
            else:
                return f"border: solid {LIGHT_BLUE}; border-width: 0px 1px 0px px;"
        else:
            if self.is_first:
                return f"border: solid {VERY_LIGHT_BLUE}; border-width: 1px 0px 1px 1px; border-right-width: 1px; border-right-color:  {LIGHT_BLUE}; border-right-style: solid;"
            elif self.is_last:
                return f"border: solid {VERY_LIGHT_BLUE}; border-width: 1px 1px 1px 0px;"
            else:
                return f"border: solid {VERY_LIGHT_BLUE}; border-width: 1px 0px 1px 0px; border-right-width: 1px; border-right-color:  {LIGHT_BLUE}; border-right-style: solid;"

    def activate_button(self):
        self.color = WHITE
        # self.bg_color = DARK_BLUE
        self.font_weight = "bold"
        self.is_active = True
        self.set_style()

    def deactivate_button(self):
        self.color = LIGHT_GREY
        # self.bg_color = MEDIUM_BLUE
        self.font_weight = "normal"
        self.is_active = False
        self.set_style()

    def toggle_button(self):
        if self.is_active:
            self.deactivate_button()
        else:
            self.activate_button()


class CheckButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None) -> None:
        super().__init__(parent)

        self.setText(text)
        self.setObjectName(f"{text}_btn".lower())
        self.setMinimumHeight(25)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.clicked.connect(self.toggle_button)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                           QtWidgets.QSizePolicy.Policy.Maximum)

        self.is_checked = True
        self.color = LIGHT_GREY
        self.bg_color = MEDIUM_BLUE
        self.font_width = QtCore.QRect(
            QtGui.QFontMetrics(self.font()).boundingRect(self.text())).width() + 20

        self.set_style()

    def get_is_checked(self) -> bool:
        return self.is_checked

    def get_button_width(self) -> int:
        return self.font_width

    def set_style(self) -> None:
        self.setStyleSheet(
            "QPushButton#%s{background-color: %s; color: %s; border-radius: 12px; padding:0px 10px 0px 10px;}" % (
                self.objectName(), self.bg_color, self.color
            ))

    def activate_button(self) -> None:
        self.color = LIGHT_GREY
        self.bg_color = MEDIUM_BLUE
        self.is_checked = True
        self.set_style()

    def deactivate_button(self) -> None:
        self.color = DARK_GREY
        self.bg_color = VERY_DARK_BLUE
        self.is_checked = False
        self.set_style()

    def toggle_button(self) -> None:
        if self.is_checked:
            self.deactivate_button()
        else:
            self.activate_button()


class CheckButtonScrollArea(QtWidgets.QScrollArea):
    def __init__(self, widget_width, parent=None) -> None:
        super().__init__(parent)
        # self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("col_scroll_area")
        self.setWidgetResizable(True)

        self.scrollAreaWidget = QtWidgets.QWidget()
        # self.scrollAreaWidget.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaWidget.setObjectName(u"scrollAreaWidget")
        self.setWidget(self.scrollAreaWidget)

        self.vertical_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        # self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setObjectName(u"col_v_Layout")

        self.margin = 100
        self.widget_width = widget_width - self.margin

        self.h_layout_list: list[CheckBtnHLayout] = []

        self.set_style()
        self.add_spacer()

    def fill_layout(self, btn_list: list[CheckButton]) -> None:
        self.reset_layout()
        while btn_list:
            sum_btn_width = 0
            layout = CheckBtnHLayout(self.widget_width)

            while sum_btn_width < self.widget_width and btn_list:
                btn = btn_list.pop()
                layout.append_button(btn)
                sum_btn_width += btn.get_button_width()+5

            self.add_ButtonHLayout(layout)

    def add_spacer(self):
        self.vertical_layout.addSpacerItem(QtWidgets.QSpacerItem(
            1, 1, QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding
        ))

    def reset_layout(self):
        while self.h_layout_list:
            layout = self.h_layout_list.pop()
            layout.delete_layout()

    def add_ButtonHLayout(self, layout):
        self.vertical_layout.insertLayout(
            self.vertical_layout.count() - 1, layout)
        self.h_layout_list.append(layout)

    def get_input(self):
        l = []
        for layout in self.h_layout_list:
            l.extend(layout.get_check_btns())
        return l

    def set_style(self):
        self.setStyleSheet(
            "QScrollArea#col_scroll_area{background: transparent; border-radius: 12px; border: solid white; border-width: 0px 0px 0px 0px; margin: 0px 0px 0px 0px;}"
            "QWidget#scrollAreaWidget{background: transparent;}")

        self.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical{background: rgb(59,59,90); border:none; width:14px; margin: 14 0 14 0; border-radius:0px;}"
            "QScrollBar::handle:vertical{background: rgb(80,80,122); min-height: 30px; border-radius: 7px; }"
            "QScrollBar::handle:vertical:hover{background: rgb(255,0,127);  }"
            "QScrollBar::add-line:vertical {background: rgb(59,59,90); border:none; height:15px; border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; subcontrol-position:bottom; subcontrol-origin:margin; margin: 0 0 3 0;}"
            "QScrollBar::add-line:vertical:hover{background: rgb(255,0,127); }"
            "QScrollBar::sub-line:vertical {background: rgb(59,59,90); border:none; height:15px; border-top-left-radius: 7px; border-top-right-radius: 7px; subcontrol-position:top; subcontrol-origin:margin;  margin: 3 0 0 0;}"
            "QScrollBar::sub-line:vertical:hover{background: rgb(255,0,127); }"

            "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {background:none;}"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background:none;}"
        )

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.widget_width = event.size().width() - 100
        print(f"{self.widget_width = }")
        return super().resizeEvent(event)


class CheckBtnHLayout(QtWidgets.QHBoxLayout):
    def __init__(self, parent_width, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("col_page_h_layout")
        self.setSpacing(5)


        self.setContentsMargins(5,0,5,0)

        self.sum_btn_width: int = 10

        self.btn_list: list[CheckButton] = []

        self.add_spacer()

    def get_check_btns(self) -> list[str]:
        return [btn.text() for btn in self.btn_list if not btn.get_is_checked()]

    def get_empty_width(self) -> int:
        return self.sum_btn_width

    def delete_layout(self) -> None:
        while self.btn_list:
            btn = self.btn_list.pop()
            btn.deleteLater()
        self.deleteLater()

    def add_width(self, btn_width: int) -> None:
        self.sum_btn_width -= (btn_width + self.spacing())

    def check_btn_fits_in(self, btn_width: int) -> bool:
        return self.sum_btn_width > btn_width + self.margin.left()

    def append_button(self, btn: CheckButton) -> None:
        self.insertWidget(self.count()-1, btn)
        self.btn_list.append(btn)
        self.add_width(btn.get_button_width())

    def add_spacer(self):
        for _ in range(0, 2):
            self.addSpacerItem(QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred
            ))


class NextNavButton(QtWidgets.QPushButton):
    def __init__(self, next_list, parent: QtWidgets = None) -> None:
        super().__init__(parent)
        self.setObjectName("next_btn")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.next_list: list[function] = next_list

    def set_text(self, current_page, nr_of_pages):
        if current_page < nr_of_pages:
            self.setText("Next")
        else:
            self.setText("Finish")
    
    def exe_aux_functions(self):
        if self.next_list[self.current_page-1]:
            self.next_list[self.current_page-1]()


class BackNavButton(QtWidgets.QPushButton):
    def __init__(self,  parent: QtWidgets = None) -> None:
        super().__init__(parent)
        self.setText("Back")
        self.setObjectName("back_btn")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.current_page: int = 1

    def set_visibiltiy(self):
        if self.current_page > 1:
            self.show()
        else:
            self.hide()


class pandasModel(QtCore.QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent: QtWidgets = None) -> None:
        QtCore.QAbstractTableModel.__init__(self)
        self.dataframe = dataframe

    def rowCount(self, parent=None) -> int:
        return self.dataframe.shape[0]

    def columnCount(self, parent=None) -> int:
        return self.dataframe.shape[1]

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole) -> str:
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self.dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.dataframe.columns[col]
        return None
