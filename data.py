import pandas as pd
import os


class Data:
    def __init__(self, path, depend_ferature, sepe) -> None:
        self.dep_feature = depend_ferature
        self.df = self.read_csv(path, sepe)
        self.normalised_df = self.normalise_dataframe(self.df)
        self.test_df, self.train_df = self.splitt_dataframe(self.normalised_df)

    def get_norm_df(self):
        return self.normalised_df

    def get_test_df(self):
        return self.test_df

    def get_train_df(self):
        return self.train_df

    def get_exposed_series(self, name, exponent ):
        test_df, train_df = self.splitt_dataframe(self.df)
        serien = train_df[name]
        return  self.normalise_series(serien**exponent)

    def get_df(self):
        return self.df

    def get_dep_feat(self):
        return self.dep_feature

    def get_num_rows_train(self):
        return self.train_df.shape[0]

    def get_num_rows_test(self):
        return self.test_df.shape[0]

    def get_columns(self):
        return self.df.columns

    def get_norm_series(self, name):
        return self.normalised_df[name]

    def get_train_series(self, name):
        return self.train_df[name]

    def normalise_series(self, series):
        return  (series - series.min()) / (series.max() - series.min())

    def normalise_dataframe(self, df):
        return (df - df.min()) / (df.max() - df.min())

    def splitt_dataframe(self,df):
        lenght = int(self.normalised_df.shape[0] * 0.3)

        test_df = df[:lenght]
        train_df = df[lenght:]

        return (test_df, train_df)

    def read_csv(self, path,sepe):

        df = pd.read_csv(
            os.path.join(os.path.dirname(__file__), path), sep=sepe
        )
        return df
