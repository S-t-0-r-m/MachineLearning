import math
import numpy as np
import settings


class Regression:
    def __init__(self, data) -> None:
        self.data = data
        self.learn_rate = settings.LEARN_RATE
        self.min_step_size = settings.MINIMUM_STEP_SIZE
        self.step_size_dict = {}

    def check_step_size_above_min(self,):
        A = np.where(self.step_size_list < self.min_step_size)[0]
        return A.size < self.step_size_list.size

    def learning_rate_decay(self, epoch):
        print(self.learn_rate)
        self.learn_rate = (1/ (1+1*epoch)) * self.learn_rate
        #a = a - (a*0.1)

    def get_stochastic_sample(self):
        index_list= np.random.randint(self.data.get_num_rows_train(), size= settings.SAMPLE_SIZE)
        return (self.feat_matx[:, index_list], self.y_vector[index_list])

    def linear_regression(self):
        num_rows = self.data.get_num_rows_train()
        count = 0
        while self.check_step_size_above_min() and count < settings.MAX_INTERATIONS:
            param_vec = self.param_vector
            
            for i, feat_vec in enumerate(self.feat_matx):
                param = self.calc_mean_squared_error(feat_vec, param_vec, num_rows)

                self.update_step_size(i, param)
                self.update_parameter(i, param)
            
            count += 1
        print(self.name_list[1])
        print(count)
        print(self.get_r_squard())
        

    def clac_loss(self, param_vec):
        return (param_vec @ self.feat_matx) - self.y_vector

    def calc_mean_squared_error(self, feat_vec, param_vec, num_rows):
        A = feat_vec @ self.clac_loss(param_vec)
        return self.learn_rate * (1 / num_rows) * np.sum(A)

    def update_step_size(self, i, parameter):
        self.step_size_list[i] = math.sqrt(parameter ** 2)

    def get_r_squard(self):
        sst = np.sum((self.y_vector - np.mean(self.y_vector))**2)
        ssr = np.sum(self.clac_loss(self.param_vector)**2)
        return 1 - (ssr/sst)


    def update_parameter(self, i, parameter):
        self.param_vector[i] = self.param_vector[i] - parameter


class SingleVarRegression(Regression):
    def __init__(self, name, data, function_type, exponent) -> None:
        super().__init__(data)
        self.function_type = function_type
        self.name_list = self.create_to_name_list(name, exponent)
        self.y_vector, self.feat_matx = self.create_feature_matrixes()
        self.step_size_list = self.create_step_size_list()
        self.param_vector = self.create_param_vector()

        super().linear_regression()

    def create_to_name_list(self, name, exponent):
        name_list = [self.data.dep_feature]

        for i in range(0, exponent):
            name_list.append(name)
        return name_list

    def create_feature_matrixes(self):
        feat_matx = np.ones((self.data.get_num_rows_train()))
        y_vector = None

        for exponent, name in enumerate(self.name_list):
            feature_vector = self.data.get_train_series(name).to_numpy()

            if name == self.data.get_dep_feat():
                y_vector = feature_vector
            else:
                feature_vector = self.modify_vector(feature_vector, exponent,name)
                feat_matx = np.vstack([feat_matx, feature_vector])
        return (y_vector, feat_matx)

    def modify_vector(self, feature_vector, exponent, name):
        if self.function_type == "polynomial":
            return  feature_vector ** exponent
            #return self.data.get_exposed_series(name, exponent ).to_numpy()
        elif self.function_type == "log":
            pass
        elif self.function_type == "exponanial":
            pass

    def create_step_size_list(self):
        return np.ones(len(self.name_list))



    def create_param_vector(self):
        return np.random.rand(len(self.name_list))

    def override_regression_object(self, name, f_type, num):
        self.function_type = f_type
        self.name_list = self.create_to_name_list(self, name, num)
        self.y_vector, self.feat_matx = self.create_feature_matrixes()
        self.step_size_list = self.create_step_size_list()
        self.param_vector = self.create_param_vector()

        super().linear_regression()


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)

