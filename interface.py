import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


class Interface():
    def __init__(self) -> None:
        root = tk.Tk(className=" Maschine Learning")
        root.configure(background='#323739')
        root.geometry("1980x1080")
        root.mainloop()



    def print_normalised_plot(self, data, reg):

        upper_limit= 1.1
        lower_limit = -0.1
        columns = 4
        rows = int(len(reg)/columns+1)

        
        figur, ax = plt.subplots(rows,columns)
        j = 0
        i = 0
        for reges in reg:
            if j >= columns:
                j = 0
                i += 1
                
            ax[i,j].set_xlim(lower_limit, upper_limit)
            ax[i,j].set_ylim(lower_limit, upper_limit)

            x_list, y_list = self.calc_line(reges, upper_limit, lower_limit)

            ax[i,j].scatter(
                data.get_norm_series(reges.name_list[1]),  # x
                data.get_norm_series(reges.name_list[0]),  # y
                2
            )
            ax[i,j].set_title(reges.name_list[1])
            ax[i,j].plot(x_list, y_list, "r")
            j += 1

        plt.show()

    def calc_line(self, reges, upper_limit, lower_limit):
        x_matrx = np.ones(500)
        for exponent in range(1,reges.param_vector.size):
             x_matrx = np.vstack([ x_matrx, np.linspace(lower_limit, upper_limit, num=500) **exponent])

        y_list=  reges.param_vector @ x_matrx 

        return(x_matrx[1] ,y_list)




    def print_step_size_plot(self, data, reg):
        for reges in reg:

            f, ax = plt.subplots(1)

            plt.title(reges.name_list[1])
            plt.xlabel(reges.name_list[1])
            plt.ylabel(reges.name_list[0])
            x = np.arange(0, len(reges.step_size))
            print(reges.step_size_list)

            ax.plot(
                x, reges.step_size,  # x  # y
            )
            plt.show()

