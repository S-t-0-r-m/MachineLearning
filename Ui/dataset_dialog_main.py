from Ui.dataset_dialog import Ui_Dialog
from dataset import Dataset
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class DatasetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.parent_element = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.dataset = None
        self.path = None

        self.ui.comBoxSep.setItemData(0, ",")
        self.ui.comBoxSep.setItemData(1, ";")
        self.ui.comBoxSep.setItemData(2, ":")
        self.ui.comBoxSep.setItemData(3, "\s+")
        self.ui.comBoxSep.setItemData(4, " ")
        self.ui.comBoxSep.setItemData(5, "-")

        self.ui.submitbtn.clicked.connect(self.submit_path_in_path_lineEdit)
        self.ui.btnBrowse.clicked.connect(self.set_path_in_line_edit_with_file_browser)

    def set_path_in_line_edit_with_file_browser(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open file",
            "C:\\Users\\sbues\\VSCode\\python\\Regression\\datasets",
            "CSV files (*.csv)",
        )[0]
        self.ui.path_lineEdit.setText(filepath)

    def submit_path_in_path_lineEdit(self):
        input_path = self.ui.path_lineEdit.text()

        if len(input_path) < 5 or not ".csv" in input_path[len(input_path) - 4 :]:
            print(f"Invalid Path: {self.ui.path_lineEdit.text()}")
            return
        self.path = input_path
        self.create_datframe()

        if self.dataset == None:
            return

    def create_table_view(self):
        model = pandasModel(self.dataset.get_df())
        self.ui.tableView.setModel(model)
        self.ui.tableView.update()

    def create_datframe(self):
        try:
            self.dataset = Dataset()
            self.dataset.set_up(
                self.path, "None", self.ui.comBoxSep.currentData(), True
            )
        except TypeError:
            print("error: dialog -> create_datfram() ")

    def get_pojectname(self):
        return self.ui.name_lineEdit.text()

    def accept(self):
        name = self.get_pojectname()
        if self.dataset == None or name == "":
            return

        self.dataset.save_dataset(name)
        self.parent_element.project_name = name
        self.done(0)

    def reject(self):
        self.done(0)


class pandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None) -> None:
        QtCore.QAbstractTableModel.__init__(self)
        self.data = data

    def rowCount(self, parent=None):
        return self.data.shape[0]

    def columnCount(self, parent=None):
        return self.data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.data.columns[col]
        return None


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    window = DatasetDialog()
    window.show()

    sys.exit(root.exec())
