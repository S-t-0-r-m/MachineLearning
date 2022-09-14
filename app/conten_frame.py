from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
plt.style.use("bmh")
import numpy as np
import os
PATH = os.path.dirname(__file__)

class ContenFrame(QtWidgets.QTabWidget):
    def __init__(self, reg_obj,parent = None) -> None:
        super().__init__(parent)
        self.reg_obj = reg_obj

        self.parent_element = parent
        self.time = 0
        self.df_type = "norm"
        self.df_size = "test"

        uic.loadUi(f"{PATH}/ui/mainwindow.ui", self)
        
        self.reg_obj = reg_obj
        self.setGeometry(170,53, parent.width - 170, parent.height - 74)
        self.ChatFrame.resize( 651, 700)
        self.StatsFrame.resize(251, parent.height-200)
        self.cav = Canvas( reg_obj, self.ui.ChatFrame)
        self.cav.print_single_normalised_plot()
        self.HeadingL.setText(reg_obj.get_featur_name())
        self.LearnLLineEdit.setText(str(reg_obj.learn_rate))
        self.LearnLSBtn.clicked.connect(self.set_learen_rate)
        self.MaxEpochLEdit.setText(str(reg_obj.max_epochs))
        self.MaxEpochBtn.clicked.connect(self.set_max_epochs)
        self.TestBtn.clicked.connect(self.change_to_test_chart)
        self.TrainBtn.clicked.connect(self.change_to_train_chart)
        self.chartTypeBtn.clicked.connect(self.change_chart_type)

    def change_chart_type(self):
        name = self.cav.change_chart_type()
        self.chartTypeBtn.setText(f"Chart: {name}")
        self.cav.draw()

    def change_to_test_chart(self):
        self.cav.df_size = "test"
        self.cav.clear_plot()
        self.cav.draw()

    def change_to_train_chart(self):
        self.cav.df_size = "train"
        self.cav.clear_plot()
        self.cav.draw()

    def set_learen_rate(self):
        self.reg_obj.learn_rate = float(self.LearnLLineEdit.text())

    def set_max_epochs(self):
        self.reg_obj.max_epochs = int(self.MaxEpochLEdit.text())

    def update_contend(self, time):
        self.set_epoch()
        self.set_r_squrad()
        self.set_time(time)
        self.update_plot()
        
    def update_plot(self):
        self.cav.deleteLater()
        self.cav = Canvas( self.reg_obj, self.ChatFrame, self.df_type, self.df_size)
        self.cav.print_single_normalised_plot()
        self.cav.show()

    def set_time(self, time):
        self.time+= time
        self.TimeLNum.setText(f"{round(self.time, 3)} Seconds")

    def set_epoch(self):
        self.EpochLNum.setText(str(self.reg_obj.num_of_epochs))

    def set_r_squrad(self,):
        self.RSquaredLNum.setText(str(self.reg_obj.get_r_squard()))

    def resiz(self, width, height) -> None:
        self.resize(width - 170 , height - 74)
        self.StatsFrame.setGeometry(QtCore.QRect(width - 421, 80, 251, height-200))
        self.chartSettingFrame.resize(width - 440, 38)
        self.HeadingL.move(int(((width-170)/2)-175), 0)
        self.resetBtn.move(width-(421- 100), 50)
        self.ChatFrame.resize(width - 470, height-230)
        self.cav.resize(width - 470, height-80)

    def create_step_plot(self):
        cav = StepCanvas(self.reg_obj, self.ui.scrollArea)


class Canvas(FigureCanvas):
    def __init__(self, reg_obj, parent= None,  df_type = "norm", size = "test"):
        self.fig, self.ax = plt.subplots(2, 1,figsize=(7.5,7.8), facecolor='#151819')
        super().__init__(self.fig)
        self.df_type = df_type
        self.df_size = size
        self.reg_obj = reg_obj
        self.plot = "Default"

        self.setParent(parent)
        self.parent= parent
        self.move(0,-90)

        self.upper_limit = 1.1
        self.lower_limit = -0.1

    def change_chart_type(self):
        if self.plot == "Default":
            self.plot = "Correlation"
        elif self.plot == "Correlation":
            self.plot = "Default"

        self.clear_plot()
        return self.plot

    def clear_plot(self):
        self.ax[0].cla()
        self.ax[1].cla()
        self.print_single_normalised_plot(False)

    def print_correlation_plot(self):
        x = self.calc_y_predicted()
        y = self.reg_obj.dataset.get_series(self.reg_obj.dataset.get_dependet_feature(),self.df_type, self.df_size)


        
        
    def print_single_normalised_plot(self, bol = True):

        self.ax[0].set_xlim(self.lower_limit, self.upper_limit)
        self.ax[0].set_ylim(self.lower_limit, self.upper_limit)

        self.ax[0].set_facecolor("#202124")
        self.ax[1].set_facecolor("#202124")

        x = None
        y = None

        line_x = None
        line_y = None

        loss = None

        if self.plot == "Default":

            x = self.reg_obj.dataset.get_series(self.reg_obj.get_featur_name(), self.df_type, self.df_size)
            y = self.reg_obj.dataset.get_series(self.reg_obj.dataset.get_dependet_feature(),self.df_type, self.df_size)

            loss = self.clac_loss(
                self.reg_obj.hypothesis, self.reg_obj.create_feature_matrixes(self.df_type, self.df_size), y.to_numpy()
            )

            line_x, line_y = self.calc_line(self.reg_obj.hypothesis)

        elif self.plot == "Correlation":
            x = self.calc_y_predicted()
            y = self.reg_obj.dataset.get_series(self.reg_obj.dataset.get_dependet_feature(),self.df_type, self.df_size)

            loss = self.clac_loss(np.array([0,1]), self.calc_corr_line(x), y.to_numpy())

            line_x, line_y = self.calc_line(np.array([0,1]))

        im = self.ax[0].scatter(
                x,
                y,
                c=np.absolute(loss),
                cmap="jet",
                edgecolors="black",
                linewidths=1,
                alpha=0.8,
            )

        self.ax[0].plot(line_x, line_y, "r")

        self.ax[1].hist(loss, bins=50, edgecolor="black")

        if bol:
            self.print_colorbar(im)

    def print_colorbar(self, im):

        plt.colorbar(im,  ax=self.ax[0])
        A = np.arange(0, 50)
        
        plt.colorbar(im,  ax=self.ax[1])

    def calc_y_predicted(self):
        max = self.reg_obj.create_feature_matrixes(self.df_type, self.df_size)
        hyp = self.reg_obj.get_hypothesis()
        return hyp @ max
    
    def clac_loss(self,param_vector, feat_matx, y_vector):
        return (feat_matx.T @ param_vector) - y_vector

    def calc_corr_line(self, x):
        x_matrx = np.ones(len(x))
        x_matrx = np.vstack([x_matrx, x])
        return x_matrx

    def calc_line(self,function ):
        x_matrx = np.ones(50)
        for exponent in range(1, function.size):
            x_matrx = np.vstack(
                [x_matrx, np.linspace(self.lower_limit, self.upper_limit, num=50) ** exponent]
            )

        y_list = function @ x_matrx

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







        

