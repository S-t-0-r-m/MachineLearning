#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
from regression import Regression
import pandas as pd
import os


def main():
    dependent_var = "MEDV"
    independent_var = "RAD"

    df = read_csv()
    x_df, y_df = splitt_dataframe(df, dependent_var, independent_var)

    reg = Regression(x_df, y_df, independent_var)
    reg.linear_regression()
    reg.print_normalised_plot(independent_var)


def splitt_dataframe(df, dependent_var, independent_var):
    # x_df = df.drop(columns = dependent_var)
    # df[independent_var]
    y_df = df[dependent_var]

    x_df = df[independent_var]
    return (x_df, y_df)


def read_csv():

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "housing.csv"), sep="\s+")
    return df


if __name__ == "__main__":
    main()
