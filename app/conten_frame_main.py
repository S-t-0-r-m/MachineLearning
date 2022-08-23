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
        self.time = 0
        self.df_type = "norm"
        self.df_size = "test"

        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)
        self.reg_obj = reg_obj
        self.setGeometry(170,53, parent.width - 170, parent.height - 74)
        self.ui.ChatFrame.resize( 651, 700)
        self.ui.StatsFrame.resize(251, parent.height-200)
        self.cav = Canvas( reg_obj, self.ui.ChatFrame)
        self.cav.print_single_normalised_plot()
        self.ui.HeadingL.setText(reg_obj.get_featur_name())
        self.ui.LearnLLineEdit.setText(str(reg_obj.learn_rate))
        self.ui.LearnLSBtn.clicked.connect(self.set_learen_rate)
        self.ui.MaxEpochLEdit.setText(str(reg_obj.max_epochs))
        self.ui.MaxEpochBtn.clicked.connect(self.set_max_epochs)
        self.ui.TestBtn.clicked.connect(self.change_to_test_chart)
        self.ui.TrainBtn.clicked.connect(self.change_to_train_chart)

    def change_to_test_chart(self):
        self.cav.clear_plot()
        self.df_type = "test"


    def change_to_train_chart(self):
        self.cav.clear_plot()
        self.df_type = "train"

        self.cav.update()
        self.cav.show()


    def set_learen_rate(self):
        self.reg_obj.learn_rate = float(self.ui.LearnLLineEdit.text())

    def set_max_epochs(self):
        self.reg_obj.max_epochs = int(self.ui.MaxEpochLEdit.text())

    def update_contend(self, time):
        self.set_epoch()
        self.set_r_squrad()
        self.set_time(time)
        self.update_plot()
        
    def update_plot(self):
        self.cav.deleteLater()
        self.cav = Canvas( self.reg_obj, self.ui.ChatFrame, self.df_type, self.df_size)
        self.cav.show()

    def set_time(self, time):
        self.time+= time
        self.ui.TimeLNum.setText(f"{round(self.time, 3)} Seconds")

    def set_epoch(self):
        self.ui.EpochLNum.setText(str(self.reg_obj.num_of_epochs))

    def set_r_squrad(self,):
        self.ui.RSquaredLNum.setText(str(self.reg_obj.get_r_squard()))

    def resiz(self, width, height) -> None:
        self.resize(width - 170 , height - 74)
        self.ui.StatsFrame.setGeometry(QtCore.QRect(width - 421, 80, 251, height-200))
        self.ui.chartSettingFrame.resize(width - 440, 38)
        self.ui.HeadingL.move(int(((width-170)/2)-175), 0)
        self.ui.resetBtn.move(width-(421- 100), 50)
        self.ui.ChatFrame.resize(width - 470, height-230)
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
           

        self.setParent(parent)
        self.parent= parent
        self.move(0,-90)
        # self.print_single_normalised_plot(reg_obj)

    def clear_plot(self):
        self.ax[0].clf()
        self.ax[0].plot()
        


    def print_single_normalised_plot(self):

        upper_limit = 1.1
        lower_limit = -0.1

        self.ax[0].set_xlim(lower_limit, upper_limit)
        self.ax[0].set_ylim(lower_limit, upper_limit)

        x = self.reg_obj.dataset.get_series(self.reg_obj.get_featur_name(), self.df_type, self.df_size)
        y = self.reg_obj.dataset.get_series(self.reg_obj.dataset.get_dependet_feature(),self.df_type, self.df_size)

        #print(f"epochs: {reg_obj.num_of_epochs}")
        #print(f"R^2: {reg_obj.get_r_squard()} %")

        #print(reg_obj.hypothesis)

        list = self.clac_loss(
                self.reg_obj.hypothesis, self.reg_obj.create_feature_matrixes(self.df_type, self.df_size), y.to_numpy()
            )

        x_list, y_list = self.calc_line(self.reg_obj, upper_limit, lower_limit)

        im = self.ax[0].scatter(
                x,
                y,
                c=np.absolute(list),
                cmap="jet",
                edgecolors="black",
                linewidths=1,
                alpha=0.8,
            )
        #print(f"1. {type(im)}")
        self.ax[0].plot(x_list, y_list, "r")
        plt.colorbar(im,  ax=self.ax[0])
        A = np.arange(0, 50)

        self.ax[0].set_facecolor("#202124")
        self.ax[1].set_facecolor("#202124")

        imm =self.ax[1].hist(list, bins=50, edgecolor="black")
        
        plt.colorbar(im,  ax=self.ax[1])

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







        

