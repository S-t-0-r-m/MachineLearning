import math
import numpy as np


class Feature:
    def __init__(self, name, series) -> None:
        self.series = series.to_numpy()
        self.name = name
        self.step_size = 1
        self.parameter = 0

    def get_parameter(self):
        return self.parameter

    def set_parameter(self, parameter):
        self.parameter = parameter

    def update_parameter(self, sum_squared_residuals):
        self.parameter = self.parameter - sum_squared_residuals

    def get_series(self):
        return self.series

    def get_name(self):
        return self.name

    def get_step_size(self):
        return self.step_size

    def reset_step_size(self):
        self.step_size = 1

    def update_step_size(self, sum_squared_residuals):
        self.step_size = math.sqrt(sum_squared_residuals ** 2)


class DependentFeature(Feature):
    def __init__(self, name, series) -> None:
        super().__init__(name, series)
        self.ones = np.ones((series.size))

    def get_ones_vector(self):
        return self.ones

