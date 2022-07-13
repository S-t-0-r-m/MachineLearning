from feature import DependentFeature
from data import Data
import numpy as np
import settings


class Regression:
    def __init__(self, feat_list, data) -> None:
        self.data = data
        self.feat_list = feat_list
        self.feat_matx = self.create_feature_matrix()
        self.learn_rate = settings.LEARN_RATE
        self.min_step_size = settings.MINIMUM_STEP_SIZE

    def check_step_size_above_min(self,):
        step_size_above_min = False

        for feature in self.feat_list:
            if feature.get_step_size() > self.min_step_size:
                step_size_above_min = True

        return step_size_above_min

    def create_prameter_vector(self):
        parm_vec = np.array([])

        for featur in self.feat_list:
            parm_vec = [np.append(parm_vec, featur.get_parameter())]

        return np.transpose(parm_vec)

    def create_feature_matrix(self):
        feat_matx = np.array([])

        for featur in self.feat_list:
            if isinstance(featur, DependentFeature):
                feat_matx = featur.get_ones_vector()
            else:
                A = featur.get_series()
                feat_matx = np.vstack([feat_matx, A])

        return np.transpose(feat_matx)

    def linear_regression(self):
        num_rows = self.data.get_num_rows_train()

        while self.check_step_size_above_min():
            param_vec = self.create_prameter_vector()

            for i, feature in enumerate(self.feat_list):
                param = self.calc_mean_squared_error(i, param_vec, num_rows)
                self.append_parameter(feature, param)

    def calc_mean_squared_error(self, i, param_vec, num_rows):

        temp_A = self.feat_matx @ param_vec
        temp_A = temp_A - np.transpose([self.feat_list[0].get_series()])
        temp_A = self.feat_matx[:, i] @ np.transpose([temp_A])

        return (1 / num_rows) * (np.sum(temp_A) * self.learn_rate)

    def append_parameter(self, feature, param):
        feature.update_step_size(param)
        feature.update_parameter(param)


class SingleVarRegression(Regression):
    def __init__(self, name, feat_list, data) -> None:
        super().__init__(feat_list, data)
        self.name = name


        
        super().linear_regression()


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)

