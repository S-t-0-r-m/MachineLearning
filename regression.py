import feature
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from sympy import *
import os


class Regression:
    def __init__(
        self, x_df, y_series, var ,minimum_step_size=0.0001, learning_rate=0.1, sample_size=10, 

    ) -> None:
        self.sampel_indexes = []
        self.var = var
        self.learning_rate = learning_rate
        self.number_training_exaples = y_series.size
        self.sample_size = int((sample_size/100) * self.number_training_exaples)
        self.minimum_step_size = minimum_step_size

        self.y_feature = feature.DependentFeature(symbols("y"), y_series)
        self.x_feature_dict = self.create_feature_dict(y_series, x_df)

    def create_feature_dict(self, y_series, x_df):
        # for series in x_df.loc():
        # indepen_feature = feature.DependentFeature(symbols("y"), y_series)
        # step_size_dict[series.name] = indepen_feature

        feature_dict = {}

        # depen_feature = feature.DependentFeature(symbols("y"), y_series)
        # feature_dict[y_series.name] = depen_feature

        indepen_feature = feature.DependentFeature(symbols("x"), x_df)
        feature_dict[x_df.name] = indepen_feature

        return feature_dict



    def create_sample_list(self):
        self.sampel_indexes = []

        for i in range(0, self.sample_size):
            index = random.randint(0, (self.number_training_exaples - 1))

            self.sampel_indexes.append(index)
        

    def check_step_size_above_min(self):
        step_size_above_min = False

        for key, feature in self.x_feature_dict.items():
            if feature.get_step_size() > self.minimum_step_size:
                step_size_above_min = True

        if self.y_feature.get_step_size() > self.minimum_step_size:
            step_size_above_min = True

        return step_size_above_min

    def linear_regression(self):

        while self.check_step_size_above_min():
            self.create_sample_list()

            self.calc_sum_squared_residuals(self.y_feature)

            for key , feature in self.x_feature_dict.items():
                self.calc_sum_squared_residuals(feature) 


    def get_point(self, feature,index):
        if type(feature) is "DependentFeature":
            return [
                feature.get_point(index), 
                self.y_feature.get_point(index),
            ]  
        else:
            return [
                feature.get_point(index), 
                self.y_feature.get_point(index),
            ]  


    def calc_sum_squared_residuals(self, feature):
    
        x, y = symbols("x y")
        sum_squared_residuals = 0

        for index in self.sampel_indexes:

            point = self.get_point(feature,index)
            symbol = feature.get_symbol()

            derivative_eq = diff((point[1] - (y + x * point[0])) ** 2, symbol)
            
            
            slope = feature.get_parameter() 
            intercept = self.y_feature.get_parameter()

            sum_squared_residuals += (derivative_eq.subs({y: intercept,x: slope})/ self.sample_size) * self.learning_rate 

        feature.clac_new_step_size(sum_squared_residuals)
        feature.clac_new_parameter(sum_squared_residuals)

    def print_normalised_plot(self, name):

        f, ax = plt.subplots(1)

        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 1.5)

        slope = self.x_feature_dict[name].get_parameter()
        intercept = self.y_feature.get_parameter()

        print(f"Intercept: {round(intercept, 4)}")
        print(f"slope: {round(slope, 4)}")

        x = np.linspace(-1, 1)
        y = slope * x + intercept
        ax.plot(x, y, "r")

        ax.scatter(
            self.y_feature.get_normalised_series(),
            self.x_feature_dict[name].get_normalised_series(),
        )

        plt.show()

