import math
import numpy as np
import settings


class Regression:
    def __init__(self, dataset) -> None:
        self.dataset = dataset
        self.learn_rate = settings.LEARN_RATE
        self.min_step_size = settings.MINIMUM_STEP_SIZE
        self.step_size_dict = {}
        self.num_of_epochs = 0

    def check_step_size_above_min(self):
        return self.number_step_size_above_min() < self.step_size_list.size
    
    def number_step_size_above_min(self):
        return np.where(self.step_size_list < self.min_step_size)[0].size

    def learning_rate_decay(self, epoch):
        self.learn_rate = (1/ (1+1*epoch)) * self.learn_rate

    def get_stochastic_sample(self):
        index_list= np.random.randint(self.dataset.get_num_of_train_examples(), size= settings.SAMPLE_SIZE)
        return (self.feat_matx[:, index_list], self.y_vector[index_list])
    
    def get_num_of_epochs(self):
        return self.num_of_epochs

    def update_num_of_epochs(self, epoch):
        self.num_of_epochs = epoch

    def linear_regression(self):
        num_rows = self.dataset.get_num_of_train_examples()
        epoch = 0
        while self.check_step_size_above_min() and epoch < settings.MAX_INTERATIONS:
            temp_hypothesis = self.hypothesis
            
            for i, feat_vec in enumerate(self.feat_matx):
                param = self.calc_mean_squared_error(feat_vec,temp_hypothesis, num_rows)

                self.update_step_size(i, param)
                self.update_parameter(i, param)
            
            epoch += 1
        self.update_num_of_epochs(epoch)

    def clac_loss(self, hypothesis):
        return  (hypothesis @ self.feat_matx) - self.y_vector 

    def calc_mean_squared_error(self, feat_vec, hypothesis, num_rows):
        A = feat_vec @ self.clac_loss(hypothesis)
        return self.learn_rate * (1 / num_rows) * np.sum(A)

    def update_step_size(self, i, parameter):
        self.step_size_list[i] = math.sqrt(parameter ** 2)

    def get_r_squard(self):
        sst = np.sum((self.y_vector - np.mean(self.y_vector))**2)
        ssr = np.sum(self.clac_loss(self.hypothesis)**2)
        return  round(100*(1 - (ssr/sst)),3)


    def update_parameter(self, i, parameter):
        self.hypothesis[i] = self.hypothesis[i] - parameter

class SingleVarRegression(Regression):
    def __init__(self, feature_name, dataset, function_type, exponent) -> None:
        super().__init__(dataset)
        self.exponent = exponent
        self.function_type = function_type
        self.feat_name_list = self.create_to_name_list(feature_name, exponent)
        self.y_vector = self.create_y_vector()
        self.feat_matx = self.create_feature_matrixes("norm", "train")
        self.step_size_list = self.create_step_size_list()
        self.hypothesis = self.create_hypothesis()

        self.linear_regression()

    def get_hypothesis(self):
        return self.hypothesis

    def get_featur_name(self):
        return self.feat_name_list[1]

    def create_to_name_list(self, name, exponent):
        name_list = [self.dataset.dep_feature]

        for _ in range(0, exponent):
            name_list.append(name)
        return name_list

    def create_y_vector(self):
        return self.dataset.get_train_series(self.feat_name_list[0],"norm")

    def create_feature_matrixes(self, df_type, size):
        feat_matx = np.ones(self.dataset.get_num_of_examples(size))

        for exponent, name in enumerate(self.feat_name_list):
            if name == self.dataset.get_dependet_feature():
                continue

            feature_vector = self.dataset.get_series(name, df_type, size).to_numpy()
            feature_vector = self.modify_vector(feature_vector, exponent,name)
            feat_matx = np.vstack([feat_matx, feature_vector])

        return feat_matx

    def modify_vector(self, feature_vector, exponent, name):
        if self.function_type == "polynomial":
            return  feature_vector ** exponent
            #return self.data.get_exposed_series(name, exponent ).to_numpy()

    def create_step_size_list(self):
        return np.ones(len(self.feat_name_list))

    def create_hypothesis(self):
        return np.random.rand(len(self.feat_name_list))


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)

