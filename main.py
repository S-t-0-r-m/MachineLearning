#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
import regression
from interface import Interface
from data import Data


def main():

    int = Interface()
    dep_feature = "MEDV"
    data = Data("housing.csv", dep_feature)
    reg = create_single_regression_objs(data, dep_feature)
    int.print_normalised_plot(data, reg)


def create_single_regression_objs(data, dep_feature):
    regrs_list = []

    for column in data.normalised_df:
        if column == dep_feature:
            continue
        else:
            
            sin_reg = regression.SingleVarRegression(column, data, "exponanial", 4)
            regrs_list.append(sin_reg)

    return regrs_list


if __name__ == "__main__":
    main()
