import math
import numpy as np
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
                param = self.calc_mean_squared_error(feat_vec ,param_vec, num_rows)

                self.update_step_size(i,param)
                self.update_parameter(i,param)

    def clac_loss(self, param_vec):
        A = ( param_vec @ self.feat_matx)

        return A - self.y_vector

    def calc_mean_squared_error(self, feat_vec, param_vec, num_rows):
        A = self.clac_loss(param_vec)
        A = feat_vec @ A 

        return (1 / num_rows) * (np.sum(A) * self.learn_rate)

    def update_step_size(self, i,parameter):
        self.step_size_list[i] = math.sqrt(parameter ** 2)

    def update_parameter(self,i, parameter):
        test = self.param_vector[i]- parameter
        self.param_vector[i] = self.param_vector[i] - parameter
    

class SingleVarRegression(Regression):
    def __init__(self, name_list, data) -> None:
        super().__init__(data)
        self.name_list = name_list
        self.y_vector =  None
        self.feat_matx = self.create_feature_matrix()
        self.step_size_list = np.array([1,1], dtype= np.float)
        self.param_vector = np.array([0,0], dtype= np.float)
        
        super().linear_regression()

    def create_feature_matrix(self):
        feat_matx = np.ones((self.data.get_num_rows_train()))

        for name in self.name_list:
            A = self.data.get_train_series(name).to_numpy()

            if name == self.data.get_dep_feat():
                self.y_vector = A
            else:
                feat_matx = np.vstack([feat_matx, A])

        return feat_matx


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)

