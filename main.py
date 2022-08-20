#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
import time
import regression
import concurrent.futures
from dataset import Dataset
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import numpy as np

from app.mainwindow_main import MainWindowMain
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    mode = "app"

    if mode == "app":
        runapp()
        return

    dep_feature = "MEDV"
    data = Dataset()
    data.set_up("datasets/housing.csv", dep_feature, "\s+", False)
    reg = create_single_regression_objs(data, dep_feature)
    print_single_normalised_plot(data, reg)
    for regs in reg:
        print_plot(regs)


def runapp():

    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    root = QtWidgets.QApplication(sys.argv)
    window = MainWindowMain()
    window.show()

    sys.exit(root.exec())


def create_single_regression_objs(data, dep_feature):
    start = time.time()
    regrs_list = []

    regrs_list = [
        regression.SingleVarRegression(column, data, "polynomial", 3)
        for column in data.normalised_df
        if column == "LSTAT"
    ]
    #!= dep_feature
    end = time.time()
    print(f"Time: {round(end - start, 3)}s")

    return regrs_list


def print_single_normalised_plot(data, regs):

    upper_limit = 1.1
    lower_limit = -0.1

    df_type = "norm"
    size = "test"

    for reg in regs:

        figur, ax = plt.subplots(2, 1, figsize=(4, 5))

        ax[0].set_xlim(lower_limit, upper_limit)
        ax[0].set_ylim(lower_limit, upper_limit)

        x = data.get_series(reg.get_featur_name(), df_type, size)
        y = data.get_series(data.get_dependet_feature(), df_type, size)

        print(f"epochs: {reg.num_of_epochs}")
        print(f"R^2: {reg.get_r_squard()} %")
        print(reg.step_size_list.shape[1])

        list = clac_loss(
            reg.hypothesis, reg.create_feature_matrixes(df_type, size), y.to_numpy()
        )

        x_list, y_list = calc_line(reg, upper_limit, lower_limit)

        im = ax[0].scatter(
            x,
            y,
            c=np.absolute(list),
            cmap="jet",
            edgecolors="black",
            linewidths=1,
            alpha=0.8,
        )
        ax[0].set_title(reg.get_featur_name())
        ax[0].plot(x_list, y_list, "r")

        plt.colorbar(im, ax=ax[0])

        ax[1].hist(list, bins=50, edgecolor="black")

    plt.show()

def print_plot(reg_obj):
    x = create_x(reg_obj.step_size_list)
    fig, ax = plt.subplots(reg_obj.step_size_list.shape[1], 1,figsize=(6.51,8), facecolor='#151819')

    for i in range(reg_obj.step_size_list.shape[1]):
        ax[i].plot(x, reg_obj.step_size_list[1:,i], "r")
    plt.show()

    

    
def create_x( step_size_list):
    return  np.arange(10, step_size_list.shape[0]*10, 10)


def clac_loss(param_vector, feat_matx, y_vector):
    return (feat_matx.T @ param_vector) - y_vector


def calc_line(reges, upper_limit, lower_limit):
    x_matrx = np.ones(50)
    for exponent in range(1, reges.get_hypothesis().size):
        x_matrx = np.vstack(
            [x_matrx, np.linspace(lower_limit, upper_limit, num=50) ** exponent]
        )

    y_list = reges.get_hypothesis() @ x_matrx

    return (x_matrx[1], y_list)


if __name__ == "__main__":
    main()
