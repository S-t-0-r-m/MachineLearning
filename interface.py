import matplotlib.pyplot as plt
import numpy as np
from tkinter import *

class Interface:

    def __init__(self) -> None:
        root = Tk()
        #root.mainloop()


    def print_normalised_plot(self,data, reg):

        for reges in reg:

            f, ax = plt.subplots(1)

            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.1)

            #slope7 = reges.param_vector[7]
            #slope6 = reges.param_vector[6]
            #slope5 = reges.param_vector[5]
            slope4 = reges.param_vector[4]
            slope3 = reges.param_vector[3]
            slope2 = reges.param_vector[2]
            slope = reges.param_vector[1]
            intercept = reges.param_vector[0]

            plt.title(reges.name_list[1])
            plt.xlabel(reges.name_list[1])
            plt.ylabel(reges.name_list[0])
            #  slope7 * (x**7) + slope6 * (x**6) + slope5 * (x**5) +

            x = np.linspace(-1, 2)
            y = slope4 * (x**2) +slope3 * (x**3) + slope2 * (x**2) + slope * x + intercept

            ax.scatter(
                data.get_norm_series(reges.name_list[1]), # x
                data.get_norm_series(reges.name_list[0]), # y
            )
            ax.plot(x, y, "r")

        plt.show()
