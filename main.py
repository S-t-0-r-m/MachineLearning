#  CRIM   ZN  INDUS  CHAS NOX  RM   AGE  DIS   RAD  TAX   PTRATIO  B   LSTAT  MEDV
import time
import regression
import concurrent.futures
from interface import Interface
from data import Data


def main():

    inter = Interface()
    dep_feature = "MEDV"
    data = Data("data/housing.csv", dep_feature, "\s+")
    reg = create_single_regression_objs(data, dep_feature)
    inter.print_normalised_plot(data, reg)
    

def create_single_regression_objs(data, dep_feature):
    start = time.time()
    regrs_list = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        regrs_list = [executor.submit(dosomething,column, data, "polynomial", 3 ).result() for column in data.normalised_df if column == "RM"]
        #!= dep_feature
    end = time.time()
    print(f"Time: {end - start}")

    return regrs_list

def dosomething(column, data, name, num):
    return regression.SingleVarRegression(column, data, name, num)


if __name__ == "__main__":
    main()
