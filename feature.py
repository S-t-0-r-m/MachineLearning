import math
import numpy as np


class Feature():
    def __init__(self, name , series)-> None:
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
    def __init__(self,name, series) -> None:
        super().__init__(name, series)
        self.ones = np.ones((series.size))

    def get_ones_vector(self):
        return self.ones
        

class FeatureCollection:
    def __init__(self, df,  dependent_feature) -> None:
        self.feature_dict = self.create_feature_dict(dependent_feature)
        
    def create_feature_dict(self, name):
        feature_dict = {}

        dep_feature = DependentFeature(name,self.normalised_df[name])
        feature_dict[name] = dep_feature

        for column in self.df:
            if column == name:
                continue

            ind_feature = Feature(column ,self.normalised_df[column])
            feature_dict[column] = ind_feature

            dep_feature.append_sing_param_dict(column)

        return feature_dict

    def get_dep_feature(self):
        return self.feature_dict[self.dependent_feature]

    def insert_row_of_ones(self):
        ones = np.ones((self.number_training_exaples, 1))
        self.normalised_df.insert(loc=0, column="one", value=ones)

    def normalise_series(self, series):
        return  (series - series.min()) / (series.max() - series.min())

    def get_column_n_df(self, name):
        return  self.normalised_df[name]

    def get_normalised_df(self):
        return self.normalised_df
    
    def get_feature_dict(self):
        return self.feature_dict

    def get_df_lenght(self):
        return self.number_training_exaples

    def get_single_reg_dict(self, name):
        dep_feature = self.get_dep_feature()
        indep_feature = self.feature_dict[name]
        feat_dict =  {dep_feature.name : dep_feature, indep_feature.name: indep_feature}
        return feat_dict




