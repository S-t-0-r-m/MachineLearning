import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


def print_normalised_plot(data, reg):

    for reges in reg:

        f, ax = plt.subplots(1)

        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        slope = reges.param_vector[1]
        intercept = reges.param_vector[0]

        plt.title(reges.name_list[1])
        plt.xlabel(reges.name_list[1])
        plt.ylabel(reges.name_list[0])

        x = np.linspace(-1, 2)
        y = slope * x + intercept

        ax.scatter(
            data.get_norm_series(reges.name_list[1]),  # x
            data.get_norm_series(reges.name_list[0]), # y
        )
        ax.plot(x, y, "r")

    plt.show()
