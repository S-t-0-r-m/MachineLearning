import pandas as pd
import numpy as np
import os


class Dataset:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.df = dataframe
        self.normalised_df = self.normalise_dataframe(self.df)
        self.splitt_index = int(self.df.shape[0] * 0.3)

    def shuffle_dataframe(self) -> None:
        self.df.reindex(np.random.permutation(self.df.index))
        self.df.reset_index(inplace=True, drop=True)
        self.normalised_df = self.normalise_dataframe(self.df)

    def get_df(self, part: str = "full") -> pd.DataFrame:
        """
        No parameter will return complett dataframe.
        Enter 'test' to get the testing part of the dataframe.
        Enter 'train' to get the training part of the dataframe.
        """
        if part == "train":
            return self.df[: self.splitt_index]
        elif part == "test":
            return self.df[self.splitt_index:]
        else:
            return self.df

    def get_normalised_df(self, part: str = "full") -> pd.DataFrame:
        """
        No parameter will return complett dataframe.
        Enter 'test' to get the testing part of the dataframe.
        Enter 'train' to get the training part of the dataframe.
        """
        if part == "train":
            return self.normalised_df[: self.splitt_index]
        elif part == "test":
            return self.normalised_df[self.splitt_index:]
        else:
            return self.normalised_df

    def get_num_of_examples(self, part: str = "full") -> int:
        """
        No parameter returns the number of rows in the complett dataframe.
        Enter 'test' to get the number of rows in the testing set.
        Enter 'train' to get the number of rows in the training set.
        """
        if part == "test":
            return self.get_num_of_test_examples()
        elif part == "train":
            return self.get_num_of_train_examples()
        else:
            return self.df.shape[0]

    def get_num_of_train_examples(self) -> int:
        return self.df.shape[0] - self.splitt_index

    def get_num_of_test_examples(self) -> int:
        return self.splitt_index

    def get_columns(self) -> list[str]:
        return self.df.columns

    def get_series(self, name: str, part: str = "full") -> pd.Series:
        """
        No parameter will return complett Series.
        Enter 'test' to get the testing part of the Series.
        Enter 'train' to get the training part of the Series.
        """
        if part == "train":
            return self.df[name][: self.splitt_index]
        elif part == "test":
            return self.df[name][self.splitt_index:]
        else:
            return self.df[name]

    def get_normalised_series(self, name: str, part: str = "full") -> pd.Series:
        """
        No parameter will return complett Series.
        Enter 'test' to get the testing part of the Series.
        Enter 'train' to get the training part of the Series.
        """
        if part == "train":
            return self.normalised_df[name][: self.splitt_index]
        elif part == "test":
            return self.normalised_df[name][self.splitt_index:]
        else:
            return self.normalised_df[name]

    def normalise_series(self, series: pd.Series) -> pd.Series:
        return (series - series.min()) / (series.max() - series.min())

    def normalise_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        return (df - df.min()) / (df.max() - df.min())

    def normalise_value(self, value: float, series_name: str) -> float:
        series_min = self.df[series_name].min()
        series_max = self.df[series_name].max()

        return (value - series_min) / (series_max - series_min)

    def denormalise_value(self, value: float, series_name: str) -> float:
        series_min = self.df[series_name].min()
        series_max = self.df[series_name].max()

        return value * (series_max - series_min) + series_min

    def denormalise_hypothesis(self, hypothesis: np.ndarray, series_name: str):
        pass


def read_csv(path: str, fullpath: bool, separator: str) -> pd.DataFrame:
    if not fullpath:
        path = os.path.join(os.path.dirname(__file__), path)

    return pd.read_csv(path, sep=separator)


def save_dataset(dataframe: pd.DataFrame, project_name: str, seperator: str) -> None:
    path = os.path.join(os.path.dirname(__file__), "projects", project_name)

    if not os.path.exists(path):
        os.mkdir(path)

    dataframe.to_csv(f"{path}/{project_name}_df.csv",
                     sep=seperator, index=False)


def load_dataset(path: str, project_name: str, separator: str) -> Dataset:
    if not os.path.exists(path):
        return

    return Dataset(
        pd.read_csv(f"{path}/{project_name}_df.csv", sep=separator), separator
    )
