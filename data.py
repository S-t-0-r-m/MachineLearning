import pandas as pd
import os

class Data:
    def __init__(self, file_name, depend_ferature) -> None:
        self.dep_feature  = depend_ferature
        self.df = self.read_csv(file_name)
        self.normalised_df = self.normalise_dataframe(self.df)
        self.test_df, self.train_df = self.splitt_dataframe()

    def get_norm_df(self):
        return self.normalised_df

    def get_test_df(self):
        return self.test_df

    def get_train_df(self):
        return self.train_df

    def get_df(self):
        return self.df

    def get_dep_feat(self):
        return self.dep_feature
    
    def get_num_rows_train(self):
        return self.train_df.shape[0]

    def get_num_rows_train(self):
        return self.test_df.shape[0]

    def get_columns(self):
        return self.df.columns

    def get_norm_series(self, name):
        return self.normalised_df[name]

    def get_train_series(self, name):
        return self.train_df[name]
        
    def normalise_dataframe(self, df):
        return (df - df.min()) / (df.max() - df.min())

    def splitt_dataframe(self):
        lenght = int(self.normalised_df.shape[0] * 0.2)
        
        test_df = self.normalised_df[:lenght]
        train_df = self.normalised_df[lenght:]

        return (test_df, train_df)

    def read_csv(self,file_name):

        df = pd.read_csv(os.path.join(os.path.dirname(__file__),"data",file_name), sep="\s+")
        return df
        
