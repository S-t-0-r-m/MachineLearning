# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contend_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(950, 742)
        TabWidget.setStyleSheet("QTabWidget{background-color: #202124; border:none;}")
        TabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.summeryTab = QtWidgets.QWidget()
        self.summeryTab.setStyleSheet("QWidget{background-color: #151819; }")
        self.summeryTab.setObjectName("summeryTab")
        self.HeadingL = QtWidgets.QLabel(self.summeryTab)
        self.HeadingL.setGeometry(QtCore.QRect(300, 0, 350, 60))
        self.HeadingL.setStyleSheet("QLabel{ color:#C1C1C1; font: bold;  font-size: 30px; border:solid #C1C1C1; border-width: 0px px 5px 0px}")
        self.HeadingL.setAlignment(QtCore.Qt.AlignCenter)
        self.HeadingL.setObjectName("HeadingL")
        self.StatsFrame = QtWidgets.QFrame(self.summeryTab)
        self.StatsFrame.setEnabled(True)
        self.StatsFrame.setGeometry(QtCore.QRect(690, 80, 251, 611))
        self.StatsFrame.setStyleSheet("QFrame{ border: solid #C1C1C1; border-width: 0px 0px 0px 1px;}")
        self.StatsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StatsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.StatsFrame.setObjectName("StatsFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.StatsFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.StatsFrame)
        self.listWidget.setEnabled(True)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 100))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listWidget.setStyleSheet("QListWidget{ background-color: #2F2F2F;color:#C1C1C1;border: solid grey; border-width: 1px;}")
        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 9, 0, 1, 2)
        self.LearnLLineEdit = QtWidgets.QLineEdit(self.StatsFrame)
        self.LearnLLineEdit.setEnabled(True)
        self.LearnLLineEdit.setStyleSheet("QLineEdit {background-color: #2F2F2F; color: #edebeb; border: solid red; width: 9px 1px 1px 1px}")
        self.LearnLLineEdit.setObjectName("LearnLLineEdit")
        self.gridLayout.addWidget(self.LearnLLineEdit, 12, 0, 1, 1)
        self.LearnLSBtn = QtWidgets.QPushButton(self.StatsFrame)
        self.LearnLSBtn.setStyleSheet("QPushButton {background-color: #2F2F2F; color: #edebeb; text-align: center; }")
        self.LearnLSBtn.setObjectName("LearnLSBtn")
        self.gridLayout.addWidget(self.LearnLSBtn, 12, 1, 1, 1)
        self.EpochLNum = QtWidgets.QLabel(self.StatsFrame)
        self.EpochLNum.setStyleSheet("QLabel{ color:#C1C1C1; margin-bottom: 5px;border: None;}")
        self.EpochLNum.setObjectName("EpochLNum")
        self.gridLayout.addWidget(self.EpochLNum, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 15, 0, 1, 1)
        self.PotenzSubBtn = QtWidgets.QPushButton(self.StatsFrame)
        self.PotenzSubBtn.setEnabled(False)
        self.PotenzSubBtn.setStyleSheet("QPushButton {background-color: #2F2F2F; color: #edebeb; text-align: center; }")
        self.PotenzSubBtn.setObjectName("PotenzSubBtn")
        self.gridLayout.addWidget(self.PotenzSubBtn, 10, 1, 1, 1)
        self.MaxEpochLabel = QtWidgets.QLabel(self.StatsFrame)
        self.MaxEpochLabel.setStyleSheet("QLabel{ color:#C1C1C1;margin-top: 5px;border: None;}")
        self.MaxEpochLabel.setObjectName("MaxEpochLabel")
        self.gridLayout.addWidget(self.MaxEpochLabel, 13, 0, 1, 1)
        self.MaxEpochBtn = QtWidgets.QPushButton(self.StatsFrame)
        self.MaxEpochBtn.setStyleSheet("QPushButton {background-color: #2F2F2F; color: #edebeb; text-align: center; }")
        self.MaxEpochBtn.setObjectName("MaxEpochBtn")
        self.gridLayout.addWidget(self.MaxEpochBtn, 14, 1, 1, 1)
        self.RSquaredLNum = QtWidgets.QLabel(self.StatsFrame)
        self.RSquaredLNum.setStyleSheet("QLabel{ color:#C1C1C1; margin-bottom: 5px;border: None;}")
        self.RSquaredLNum.setObjectName("RSquaredLNum")
        self.gridLayout.addWidget(self.RSquaredLNum, 5, 0, 1, 1)
        self.RSquaredL = QtWidgets.QLabel(self.StatsFrame)
        self.RSquaredL.setStyleSheet("QLabel{ color:#C1C1C1;border: None;}")
        self.RSquaredL.setObjectName("RSquaredL")
        self.gridLayout.addWidget(self.RSquaredL, 4, 0, 1, 2)
        self.MaxEpochLEdit = QtWidgets.QLineEdit(self.StatsFrame)
        self.MaxEpochLEdit.setEnabled(True)
        self.MaxEpochLEdit.setStyleSheet("QLineEdit {background-color: #2F2F2F; color: #edebeb; border: solid red; width: 9px 1px 1px 1px}")
        self.MaxEpochLEdit.setClearButtonEnabled(False)
        self.MaxEpochLEdit.setObjectName("MaxEpochLEdit")
        self.gridLayout.addWidget(self.MaxEpochLEdit, 14, 0, 1, 1)
        self.TimeLNum = QtWidgets.QLabel(self.StatsFrame)
        self.TimeLNum.setStyleSheet("QLabel{ color:#C1C1C1; margin-bottom: 10px;border: None;}")
        self.TimeLNum.setObjectName("TimeLNum")
        self.gridLayout.addWidget(self.TimeLNum, 7, 0, 1, 1)
        self.PotenzSpinBox = QtWidgets.QSpinBox(self.StatsFrame)
        self.PotenzSpinBox.setEnabled(False)
        self.PotenzSpinBox.setStyleSheet("")
        self.PotenzSpinBox.setWrapping(True)
        self.PotenzSpinBox.setMinimum(1)
        self.PotenzSpinBox.setMaximum(20)
        self.PotenzSpinBox.setObjectName("PotenzSpinBox")
        self.gridLayout.addWidget(self.PotenzSpinBox, 10, 0, 1, 1)
        self.EpochL = QtWidgets.QLabel(self.StatsFrame)
        self.EpochL.setStyleSheet("QLabel{ color:#C1C1C1; border: None;}")
        self.EpochL.setObjectName("EpochL")
        self.gridLayout.addWidget(self.EpochL, 2, 0, 1, 1)
        self.TimeL = QtWidgets.QLabel(self.StatsFrame)
        self.TimeL.setStyleSheet("QLabel{ color:#C1C1C1;border: None;}")
        self.TimeL.setObjectName("TimeL")
        self.gridLayout.addWidget(self.TimeL, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.StatsFrame)
        self.label.setStyleSheet("QLabel{ color:#C1C1C1;border: None;    border:  solid #C1C1C1; border-width: 2px 0px 0px 0px;padding-top:5px;}")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 8, 0, 1, 2)
        self.LearnL = QtWidgets.QLabel(self.StatsFrame)
        self.LearnL.setStyleSheet("QLabel{ color:#C1C1C1;margin-top: 5px;border: None; border:  solid #C1C1C1; border-width: 2px 0px 0px 0px; padding-top:5px;}")
        self.LearnL.setObjectName("LearnL")
        self.gridLayout.addWidget(self.LearnL, 11, 0, 1, 2)
        self.chartSettingFrame = QtWidgets.QFrame(self.summeryTab)
        self.chartSettingFrame.setGeometry(QtCore.QRect(20, 70, 651, 38))
        self.chartSettingFrame.setStyleSheet("QFrame{ border: solid #C1C1C1; border-width: 0px 0px 1px 0px;}")
        self.chartSettingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chartSettingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chartSettingFrame.setObjectName("chartSettingFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.chartSettingFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.chartSettingFrame)
        self.pushButton.setStyleSheet("QPushButton {background-color: #2F2F2F; color: #edebeb; text-align: center; }")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.TestBtn = QtWidgets.QRadioButton(self.chartSettingFrame)
        self.TestBtn.setStyleSheet("QRadioButton{ color:#C1C1C1;border: solid #C1C1C1; border-width: 0px 0px 0px 2px; padding-left: 5px}")
        self.TestBtn.setChecked(True)
        self.TestBtn.setObjectName("TestBtn")
        self.horizontalLayout.addWidget(self.TestBtn)
        self.TrainBtn = QtWidgets.QRadioButton(self.chartSettingFrame)
        self.TrainBtn.setStyleSheet("QRadioButton{ color:#C1C1C1; padding-right: 5px;border: solid #C1C1C1; border-width: 0px 2px 0px 0px;}")
        self.TrainBtn.setObjectName("TrainBtn")
        self.horizontalLayout.addWidget(self.TrainBtn)
        self.DynamcChartcheck = QtWidgets.QCheckBox(self.chartSettingFrame)
        self.DynamcChartcheck.setStyleSheet("QCheckBox{ color:#C1C1C1;}")
        self.DynamcChartcheck.setObjectName("DynamcChartcheck")
        self.horizontalLayout.addWidget(self.DynamcChartcheck)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.ChatFrame = QtWidgets.QFrame(self.summeryTab)
        self.ChatFrame.setGeometry(QtCore.QRect(20, 110, 651, 581))
        self.ChatFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ChatFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ChatFrame.setObjectName("ChatFrame")
        self.pushButton_2 = QtWidgets.QPushButton(self.summeryTab)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 50, 75, 23))
        self.pushButton_2.setStyleSheet("QPushButton {background-color: #2F2F2F; color: #edebeb; text-align: center; }")
        self.pushButton_2.setObjectName("pushButton_2")
        TabWidget.addTab(self.summeryTab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setStyleSheet("QWidget{background-color: #151819; }")
        self.tab_2.setObjectName("tab_2")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(300, 0, 350, 60))
        self.label_2.setStyleSheet("QLabel{ color:grey; font: bold;  font-size: 30px; border:solid grey; border-width: 0px px 5px 0px}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setGeometry(QtCore.QRect(19, 79, 911, 631))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 909, 629))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        TabWidget.addTab(self.tab_2, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.HeadingL.setText(_translate("TabWidget", "PlaceHolder"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("TabWidget", "Polynomial"))
        item = self.listWidget.item(1)
        item.setText(_translate("TabWidget", "Logarithmic"))
        item = self.listWidget.item(2)
        item.setText(_translate("TabWidget", "Exponential"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.LearnLSBtn.setText(_translate("TabWidget", "Set"))
        self.EpochLNum.setText(_translate("TabWidget", "NaN"))
        self.PotenzSubBtn.setText(_translate("TabWidget", "Set"))
        self.MaxEpochLabel.setText(_translate("TabWidget", "Max Epochs:"))
        self.MaxEpochBtn.setText(_translate("TabWidget", "Set"))
        self.RSquaredLNum.setText(_translate("TabWidget", "NaN"))
        self.RSquaredL.setText(_translate("TabWidget", "R Squared:"))
        self.TimeLNum.setText(_translate("TabWidget", "NaN"))
        self.EpochL.setText(_translate("TabWidget", "Epochs:"))
        self.TimeL.setText(_translate("TabWidget", "Time:"))
        self.label.setText(_translate("TabWidget", "Function Settings:"))
        self.LearnL.setText(_translate("TabWidget", "Learning Rate:"))
        self.pushButton.setText(_translate("TabWidget", "Chart: Standart"))
        self.TestBtn.setText(_translate("TabWidget", "Testing Set"))
        self.TrainBtn.setText(_translate("TabWidget", "Training Set"))
        self.DynamcChartcheck.setText(_translate("TabWidget", "Dynamic Chart"))
        self.pushButton_2.setText(_translate("TabWidget", "Reset"))
        TabWidget.setTabText(TabWidget.indexOf(self.summeryTab), _translate("TabWidget", "Summary"))
        self.label_2.setText(_translate("TabWidget", "PlaceHolder"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "Step Sizes"))
