import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


def print_normalised_plot(data, reg):

    for reges in reg:

        f, ax = plt.subplots(1)

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        slope = reges.feat_list[1].get_parameter()
        intercept = reges.feat_list[0].get_parameter()
        plt.title(reges.name)
        plt.xlabel(reges.name)
        plt.ylabel("MEDV")

        x = np.linspace(-1, 2)
        y = slope * x + intercept

        ax.scatter(
            data.get_norm_series(reges.name),  # x
            data.get_norm_series(data.dep_feature), # y
        )
        ax.plot(x, y, "r")

    plt.show()
