import math
import numpy as np
from requests import delete
import settings


class Regression:
    def __init__(self, data) -> None:
        self.data = data
        self.learn_rate = settings.LEARN_RATE
        self.min_step_size = settings.MINIMUM_STEP_SIZE

    def check_step_size_above_min(self,):
        A = np.where(self.step_size_list < self.min_step_size)[0]
        return A.size < self.step_size_list.size

    def linear_regression(self):
        num_rows = self.data.get_num_rows_train()
        
        while self.check_step_size_above_min():
            param_vec = self.param_vector

            for i, feat_vec in enumerate(self.feat_matx):
                param = self.calc_mean_squared_error(feat_vec, param_vec, num_rows)

                self.update_step_size(i, param)
                self.update_parameter(i, param)

    def clac_loss(self, param_vec):
        return (param_vec @ self.feat_matx) - self.y_vector

    def calc_mean_squared_error(self, feat_vec, param_vec, num_rows):
        A = feat_vec @ self.clac_loss(param_vec)
        return (1 / num_rows) * (np.sum(A) * self.learn_rate)

    def update_step_size(self, i, parameter):
        self.step_size_list[i] = math.sqrt(parameter ** 2)

    def update_parameter(self, i, parameter):
        self.param_vector[i] = self.param_vector[i] - parameter


class SingleVarRegression(Regression):
    def __init__(self, name, data ,f_type, num) -> None:
        super().__init__(data)
        self.f_type = f_type
        self.name_list = self.create_to_name_list(name, num)
        self.y_vector, self.feat_matx = self.create_feature_matrixes()
        self.step_size_list = self.create_step_size_list()
        self.param_vector = self.create_param_vector()

        super().linear_regression()

    def create_to_name_list(self, name, num):
        name_list = [self.data.dep_feature]

        for i in range(0,num):
            name_list.append(name)
        return name_list

    def create_feature_matrixes(self):
        feat_matx = np.ones((self.data.get_num_rows_train()))
        y_vector = None

        for expo, name in enumerate(self.name_list):
            A = self.data.get_train_series(name).to_numpy()

            if name == self.data.get_dep_feat():
                y_vector = A
            else:
                A = self.modify_matrix(A, expo)
                feat_matx = np.vstack([feat_matx, A])
        return (y_vector,feat_matx)

    def modify_matrix(self, A, expo):
        if self.f_type == "linear" or self.f_type == "exponanial":
            return  A ** expo
        elif self.f_type == "log":
            pass

    def create_step_size_list(self):
        return np.ones(len(self.name_list))
    
    def create_param_vector(self):
        return np.random.rand(len(self.name_list))

    def update_regression_object(self, name, f_type, num):
        self.f_type = f_type
        self.name_list = self.create_to_name_list(self, name, num)
        self.y_vector, self.feat_matx = self.create_feature_matrixes()
        self.step_size_list = self.create_step_size_list()
        self.param_vector = self.create_param_vector()

        super().linear_regression()


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)

