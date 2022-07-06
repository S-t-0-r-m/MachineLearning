import math


class Feature:
    def __init__(self, symbol, series) -> None:
        self.name = series.name
        self.symbol = symbol
        self.step_size = 1
        self.parameter = 0
        self.normalised_series = self.data_normalisation(series)

    def data_normalisation(self,series):
        normalised_series = None
        normalised_series = (series - series.min()) / (
            series.max() - series.min()
        )

        return normalised_series

    def get_step_size(self):
        return self.step_size

    def set_step_size(self, step_size):
        self.step_size = step_size

    def clac_new_step_size(self, sum_squared_residuals):
        self.step_size = math.sqrt(sum_squared_residuals ** 2)

    def get_parameter(self):
        return self.parameter

    def set_parameter(self, parameter):
        self.parameter = parameter

    def clac_new_parameter(self, sum_squared_residuals):
        self.parameter = self.parameter - sum_squared_residuals

    def get_symbol(self):
        return self.symbol

    def get_name(self):
        return self.name

    def get_normalised_series(self):
        return self.normalised_series

    def get_series_lenght(self):
        return self.normalised_series.size - 1

    def get_point(self, index):
        return self.normalised_series[index]


class DependentFeature(Feature):
    def __init__(self, symbol, series) -> None:
        super().__init__(symbol, series)


class IndependentFeature(Feature):
    def __init__(self, symbol, series) -> None:
        super().__init__(symbol, series)

