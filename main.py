#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
from regression import Regression
import feature
import interface
import pandas as pd
import os

def main():
    dependent_feature = "MEDV"

    df = read_csv()
    test_df, train_df = splitt_dataframe(df)
    feat_coll = feature.FeatureCollection(train_df, dependent_feature)
    reg = Regression(feat_coll, dependent_feature)
    reg.do_regression("single")


def splitt_dataframe(df):
    lenght = int(df.shape[0] * 0.2)
    
    test_df = df[:lenght]
    train_df = df[lenght:]

    return (test_df, train_df)


def read_csv():

    df = pd.read_csv(os.path.join(os.path.dirname(__file__),"data","housing.csv"), sep="\s+")
    return df


if __name__ == "__main__":
    main()
