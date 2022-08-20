from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.contend_frame import Ui_TabWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
plt.style.use("bmh")
import numpy as np


class  ContenFrame(QtWidgets.QTabWidget):
    def __init__(self, reg_obj,parent = None) -> None:
        super().__init__(parent)
        self.reg_obj = reg_obj

        self.parent_element = parent
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)
        self.reg_obj = reg_obj
        self.setGeometry(170,53,998, 751)
        cav = Canvas( reg_obj, self.ui.ChatFrame)
        
    
    def create_step_plot(self):
        cav = StepCanvas(self.reg_obj, self.ui.scrollArea)



class Canvas(FigureCanvas):
    def __init__(self, reg_obj, parent= None):
        fig, self.ax = plt.subplots(2, 1,figsize=(6.51,8), facecolor='#151819')
        super().__init__(fig)
        self.setParent(parent)
        self.move(0,-90)
        self.print_single_normalised_plot(reg_obj)

    def print_single_normalised_plot(self, reg_obj):

        upper_limit = 1.1
        lower_limit = -0.1

        df_type = "norm"
        size = "test"

        self.ax[0].set_xlim(lower_limit, upper_limit)
        self.ax[0].set_ylim(lower_limit, upper_limit)

        x = reg_obj.dataset.get_series(reg_obj.get_featur_name(), df_type, size)
        y = reg_obj.dataset.get_series(reg_obj.dataset.get_dependet_feature(), df_type, size)

        #print(f"epochs: {reg_obj.num_of_epochs}")
        #print(f"R^2: {reg_obj.get_r_squard()} %")

        print(reg_obj.hypothesis)

        list = self.clac_loss(
                reg_obj.hypothesis, reg_obj.create_feature_matrixes(df_type, size), y.to_numpy()
            )

        x_list, y_list = self.calc_line(reg_obj, upper_limit, lower_limit)

        im = self.ax[0].scatter(
                x,
                y,
                c=np.absolute(list),
                cmap="jet",
                edgecolors="black",
                linewidths=1,
                alpha=0.8,
            )

        self.ax[0].plot(x_list, y_list, "r")
  
        plt.colorbar(im,  ax=self.ax[0])

        self.ax[0].set_facecolor("#202124")
        self.ax[1].set_facecolor("#202124")

        self.ax[1].hist(list, bins=50, edgecolor="black")

    def clac_loss(self,param_vector, feat_matx, y_vector):
        return (feat_matx.T @ param_vector) - y_vector

    def calc_line(self,reges, upper_limit, lower_limit):
        x_matrx = np.ones(50)
        for exponent in range(1, reges.get_hypothesis().size):
            x_matrx = np.vstack(
                [x_matrx, np.linspace(lower_limit, upper_limit, num=50) ** exponent]
            )

        y_list = reges.get_hypothesis() @ x_matrx

        return (x_matrx[1], y_list)

class StepCanvas(FigureCanvas):
    def __init__(self, reg_obj, parent= None):
        fig, self.ax = plt.subplots(reg_obj.step_size_list.shape[1], 1,figsize=(6.51,8), facecolor='#151819')
        super().__init__(fig)
        self.setParent(parent)
        self.print_plot(reg_obj)

    def print_plot(self, reg_obj):
        x = self.create_x(reg_obj.step_size_list)

        for i in range(reg_obj.step_size_list.shape[1]):
            self.ax[i].plot(x, reg_obj.step_size_list[1:,i], "r")
        plt.show()

    def create_x(self, step_size_list):
        return  np.arange(10, step_size_list.shape[0]*10, 10)   







        

