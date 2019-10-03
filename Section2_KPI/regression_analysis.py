import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from Section2_KPI.KPI_descriptive_analysis import pivot_table_and_plot



def encode_output_into_numberic(data,origin,newfield):
    """
    :param origin: in str format, the field need to converted
    :param newfield: name of new column after convert
    :return: returned data frame will add 1 more column as the newfield name
    """
    data[newfield] = data[origin].apply(lambda x: 1 if x == "Yes" else 0)
    return data

def engagement_rate(data,groups,countvalue):
    engagement = pd.DataFrame(data.groupby(groups).count()[countvalue]/data.shape[0]*100)
    return engagement.T


def box_plot(data,x_axis_value,y_axis_value):
    ax = df[[x_axis_value, y_axis_value]].boxplot(by=x_axis_value,showfliers=False, figsize=(7, 5))
    ax.set_xlabel(x_axis_value)
    ax.set_ylabel(y_axis_value)
    plt.suptitle("")
    plt.show()


def logit_regression_continuous(data):
    """
    This function return the Logit Regression model for continuous variable
    """
    # Get all variable with numerical values:
    continuous_vars = list(data.describe().columns.values)
    del continuous_vars[-1] # eliminate the "Engaged" element in the list since it is used for outcome variable
    print(continuous_vars)

    # Logit Regression
    logit = sm.Logit(data["Engaged"], data[continuous_vars])
    logit_fit = logit.fit()
    print(logit_fit.summary())

def convert_categorical_to_numerical(data, variable,category):
    """
    :param variable: the column with categorical values need to encode
    :param category: the order of value in column that are giving values 0,1,2,3,4....
    :return: returned data frame will add 1 more column
    """
    categories = pd.Categorical(data[variable], categories=category)
    data["Factorized {}".format(variable)] = categories.codes
    return data



if __name__ == '__main__':
   df = pd.read_csv("WA_Fn-UseC_-Marketing-Customer-Value-Analysis.csv")
   print(df.shape)


   df = encode_output_into_numberic(df,"Response","Engaged")

   # print(engagement_rate(df,"Engaged","Response"))

   pivot_table_and_plot(df,"Response","Sales Channel","Engaged")
   box_plot(df,"Engaged", "Total Claim Amount" )

   print(convert_categorical_to_numerical(df,"Gender",["F","M"]))









