import numpy as np


class Regression:
    def __init__(self, feat, dependent_feature, learning_rate=0.01,) -> None:
        self.all_features = feat
        self.dep_feature = dependent_feature
        self.learning_rate = learning_rate
        self.minimum_step_size = 0.001

    def check_step_size_above_min(self, feat_dict):
        step_size_above_min = False

        for key, feature in feat_dict.items():
            if feature.get_step_size() > self.minimum_step_size:
                step_size_above_min = True

        return step_size_above_min
 
    def create_prameter_vector(self, feat_dict, task, name ):# not ready 
        parm_vec = np.array([])

        for key, featur in feat_dict.items():

            if task == "single" and key == self.dep_feature:
                parm_vec = np.append(parm_vec ,featur.get_intry_from_dict(name))
            else:
                parm_vec = np.append(parm_vec ,featur.get_mul_parameter())

        return np.transpose(parm_vec)

    def create_feature_matrix(self, feat_dict):
        feat_matx = np.array([])

        for key, featur in feat_dict.items():

            if key == self.dependent_feature: 
                feat_matx =  featur.get_ones_vector()
            else:
                A = featur.get_series() 
                feat_matx = np.vstack([feat_matx, A])
        
        return np.transpose(feat_matx)

    def do_regression(self,task):

        if task == "multi" or task == "both":
            feat_dict = self.all_features.get_feature_dict()
            self.linear_regression(self,feat_dict, "", "multi")

        if task == "single" or task == "both":
            for key, feature in self.all_features.feature_dict.items():
                if key != self.dep_feature:
                    feature.reset_step_size()
                    feat_dict =  self.all_features.get_single_reg_dict(key)
                    self.linear_regression( feat_dict, key, "single")

    def linear_regression(self,feat_dict, name, task):
        
        feat_matx = self.create_feature_matrix(feat_dict)

        while self.check_step_size_above_min(feat_dict):
            param_vec = self.create_prameter_vector(feat_dict, task)
            i = 0
            for key, feature in feat_dict.items():
                param = self.calc_mean_squared_error(i, feature, param_vec, feat_matx)
                self.append_parameter(self, task, feature, param, name)
                i += 1

    def calc_mean_squared_error(self, i, param_vec, feat_matx):

        temp_A = feat_matx @ param_vec
        temp_A = temp_A - self.all_features.get_dep_feature().get_series()
        temp_A = np.transpose([temp_A]) @ [feat_matx[i]]

        param = (1 / self.get_num_train_exaples()) * (np.sum(temp_A) * self.learning_rate)
        return param

    def append_parameter(self, task, feature, param, key):
        feature.update_step_size(param)

        if task == "multi":
            feature.update_mul_parameter(param)
        elif feature.name != self.dep_featur:
            feature.update_sing_parameter(param)
        elif feature.name != self.dep_featur:
            feature.append_sing_param_dict(key)
            
    def get_num_train_exaples(self):
        return self.all_features.get_df_lenght()

class SingleVarRegression(Regression):
    def __init__(self, feat, dependent_feature, learning_rate=0.01) -> None:
        super().__init__(feat, dependent_feature, learning_rate)
    
class MultiVarRegression(Regression):
    def __init__(self, feat, dependent_feature, learning_rate=0.01) -> None:
        super().__init__(feat, dependent_feature, learning_rate)





