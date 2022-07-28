
import matplotlib.pyplot as plt
import numpy as np
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton


class Interface(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.bottun = QPushButton("push")
        self.label = QLabel("Hello World!!!!")
        self.setGeometry(500,300,400,300)  


        #self.setStyleSheet("background_color:red")
       

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
                2,
                
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

    def print_single_normalised_plot(self, data, regs):
        upper_limit= 1.1
        lower_limit = -0.1

        figur, ax = plt.subplots()
        ax.set_xlim(lower_limit, upper_limit)
        ax.set_ylim(lower_limit, upper_limit)

        for reg in regs:

            x_list, y_list = self.calc_line(reg, upper_limit, lower_limit)
            ax.scatter(
                data.get_norm_series(reg.name_list[1]),  # x
                data.get_norm_series(reg.name_list[0]),  # y
                2,
                
            )
            ax.set_title(reg.name_list[1])
            ax.plot(x_list, y_list, "r")
        plt.show()






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


if __name__ == "__main__":
    root =  QApplication(sys.argv)
    window = Interface(root)
    window.resize(800, 600)
    window.setStyleSheet('red')
    window.show()

    sys.exit(root.exec())