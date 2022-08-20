import numpy as np
import settings


class Regression:
    def __init__(self, dataset) -> None:
        self.dataset = dataset
        self.learn_rate = 0.1
        self.min_step_size = settings.MINIMUM_STEP_SIZE
        self.num_of_epochs = 0

    def check_step_size_above_min(self):
        return self.number_step_size_above_min() < self.step_size_list.size

    def number_step_size_above_min(self):
        return np.where(self.step_size_list < self.min_step_size)[0].size

    def learning_rate_decay(self, epoch):
        self.learn_rate = self.learn_rate - (self.learn_rate * 0.1)
        

    def get_stochastic_sample(self):
        index_list = np.random.randint(
            self.dataset.get_num_of_train_examples(), size=settings.SAMPLE_SIZE
        )
        return (self.feat_matx[:, index_list], self.y_vector[index_list])

    def get_num_of_epochs(self):
        return self.num_of_epochs

    def update_num_of_epochs(self, epoch):
        self.num_of_epochs = epoch

    def linear_regression(self):
        num_rows = self.dataset.get_num_of_train_examples()
        epoch = 0
        while  epoch < settings.MAX_INTERATIONS:
            temp_hypothesis = self.hypothesis

            param = self.calc_mean_squared_error(temp_hypothesis, num_rows)

            if (epoch % 10) == 0:
                self.update_step_size(param)

            self.update_parameter(param)

            epoch += 1
        self.update_num_of_epochs(epoch)

    def clac_loss(self, hypothesis):
        return ((hypothesis @ self.feat_matx) - self.y_vector).to_numpy()

    def calc_mean_squared_error(self, hypothesis, num_rows):
        A = self.clac_loss(hypothesis) * self.feat_matx
        return self.learn_rate * ((1 / num_rows) * np.sum(A, axis=1))

    def update_step_size(self, parameter):
        self.step_size_list = np.vstack([self.step_size_list, np.sqrt(parameter**2)])



    def get_r_squard(self):
        sst = np.sum((self.y_vector - np.mean(self.y_vector)) ** 2)
        ssr = np.sum(self.clac_loss(self.hypothesis) ** 2)
        return round(100 * (1 - (ssr / sst)), 3)

    def update_parameter(self, parameter):
        self.hypothesis =  self.hypothesis -parameter


class SingleVarRegression(Regression):
    def __init__(self, feature_name, dataset, function_type, exponent) -> None:
        super().__init__(dataset)
        self.exponent = exponent
        self.feat_name = feature_name
        self.dep_feat_name = dataset.get_dependet_feature()
        self.function_type = function_type
        self.y_vector = self.create_y_vector()
        self.feat_matx = self.create_feature_matrixes("norm", "train")
        self.step_size_list = self.create_step_size_list()
        self.hypothesis = self.create_hypothesis()

        #self.linear_regression()

    def get_hypothesis(self):
        return self.hypothesis

    def get_featur_name(self):
        return self.feat_name

    def create_y_vector(self):
        return self.dataset.get_train_series(self.dep_feat_name, "norm")

    def create_feature_matrixes(self, df_type, size):
        feat_matx = np.ones(self.dataset.get_num_of_examples(size))

        for exponent in range(1, self.exponent + 1):

            feature_vector = self.dataset.get_series(
                self.feat_name, df_type, size
            ).to_numpy()
            feat_matx = np.vstack(
                [
                    feat_matx,
                    self.modify_vector(feature_vector, exponent, self.feat_name, size),
                ]
            )
        return feat_matx

    def modify_vector(self, feature_vector, exponent, name, size):
        if self.function_type == "polynomial":
            return feature_vector**exponent
            #return self.get_potentiated_series(name, exponent, size).to_numpy()
    
    def get_potentiated_series(self, name, exponent, size, df_type="default",): 
        series = self.dataset.get_series(name,  df_type, size)
        return  self.dataset.normalise_series(series**exponent)

    def create_step_size_list(self):
        return np.ones(self.exponent+1)

    def create_hypothesis(self):
        return np.random.rand(self.exponent+1)


class MultiVarRegression(Regression):
    def __init__(self, feat_list, data) -> None:
        super().__init__(feat_list, data)
