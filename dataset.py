import pandas as pd
import numpy as np
import os
import csv


class Dataset:
    def __init__(self) -> None:
        pass

    def set_up(self, path, depend_ferature, sep, fullpath) -> None:
        self.seperator = sep
        self.dep_feature = depend_ferature
        self.df = self.shuffle_dataframe(self.read_csv(path, fullpath))
        self.normalised_df = self.normalise_dataframe(self.df)
        self.splitt_index = int(self.df.shape[0] * 0.3)

    def get_dependet_feature(self):
        return self.dep_feature

    def set_dependet_feature(self, depend_ferature):
        self.dep_feature = depend_ferature

    def get_df(self, df_type="default"):
        if df_type == "default":
            return self.df
        elif df_type == "norm":
            return self.normalised_df

    def shuffle_dataframe(self, df):
        df = df.reindex(np.random.permutation(df.index))
        df.reset_index(inplace=True, drop=True)
        return df

    def get_test_df(self, df_type="default"):
        if df_type == "default":
            return self.df[: self.splitt_index]
        elif df_type == "norm":
            return self.normalised_df[: self.splitt_index]

    def get_train_df(self, df_type="default"):
        if df_type == "default":
            return self.df[self.splitt_index :]
        elif df_type == "norm":
            return self.normalised_df[self.splitt_index :]

    def get_num_of_examples(self, size="default"):
        if size == "test":
            return self.get_num_of_test_examples()
        elif size == "train":
            return self.get_num_of_train_examples()
        else:
            return self.df.shape[0]

    def get_num_of_train_examples(self):
        return self.df.shape[0] - self.splitt_index

    def get_num_of_test_examples(self):
        return self.splitt_index

    def get_columns(self):
        return self.df.columns

    def get_series(self, name, df_type="default", size="default"):
        if size == "test":
            return self.get_test_series(name, df_type)
        elif size == "train":
            return self.get_train_series(name, df_type)

        if df_type == "default":
            return self.df[name]
        elif df_type == "norm":
            return self.normalised_df[name]

    def get_test_series(self, name, df_type="default"):
        if df_type == "default":
            return self.df[name][: self.splitt_index]
        elif df_type == "norm":
            return self.normalised_df[name][: self.splitt_index]

    def get_train_series(self, name, df_type="default"):
        if df_type == "default":
            return self.df[name][self.splitt_index :]
        elif df_type == "norm":
            return self.normalised_df[name][self.splitt_index:]

    def normalise_series(self, series):
        return (series - series.min()) / (series.max() - series.min())

    def normalise_dataframe(self, df):
        return (df - df.min()) / (df.max() - df.min())

    def normalise_value(self, value, series_name):
        min = self.df[series_name].min()
        max = self.df[series_name].max()

        norm_value = (value - min) / (max - min)

        return norm_value

    def denormalise_value(self, value, series_name):
        min = self.df[series_name].min()
        max = self.df[series_name].max()

        denorm_value = value * (max - min) + min

        return denorm_value

    def denormalise_hypothesis(self, value, series_name):
        pass

    def read_csv(self, path, fullpath):

        if fullpath == False:
            path = os.path.join(os.path.dirname(__file__), path)

        df = pd.read_csv(path, sep=self.seperator)
        return df

    def save_dataset(self, project_name):
        path = os.path.join(os.path.dirname(__file__), "projects", project_name)

        if not os.path.exists(path):
            os.mkdir(path)

        self.df.to_csv(f"{path}/{project_name}_df.csv", index=False)
        self.normalised_df.to_csv(
            f"{path}/{project_name}_normalised_df.csv", index=False
        )

        with open(
            f"{path}/{project_name}_misc.csv",
            "w",
        ) as file:
            file.write(f"{self.dep_feature};,;{self.splitt_index}")

    def load_dataset(self, path, project_name):
        if not os.path.exists(path):
            return

        path = f"{path}/{project_name}"

        self.df = pd.read_csv(f"{path}_df.csv")
        self.normalised_df = pd.read_csv(f"{path}_normalised_df.csv")

        with open(f"{path}_misc.csv", "r") as file:
            text = csv.reader(file, delimiter=";")
            for row in text:
                self.dep_feature = row[0]
                self.seperator = row[1]
                self.splitt_index = int(row[2])

#     def get_potentiated_series(self, name, exponent ): # wrong
#         test_df, train_df = self.splitt_dataframe(self.df)
#         serien = train_df[name]
#         return  self.normalise_series(serien**exponent)
