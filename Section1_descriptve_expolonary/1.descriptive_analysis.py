import pandas as pd
import matplotlib.pyplot as plt


def conversion_rate():
    """
    :return: general conversion rate
    """
    # total number of conversions:
    conversion_no= df["conversion"].sum()
    # total number of leads. In this case, all client are MQL
    lead_no = df.shape[0]
    rate = conversion_no/lead_no*100
    return print("Total conversion is {} out of {}.\nThe conversion rate is: {:.2f}%".format(conversion_no,lead_no,rate))


def conversion_by_segment(segment):
    #calculate conversion rate
    total_no = segment["conversion"].count()
    conversion_by_segment = segment["conversion"].sum()
    conversion_rate = conversion_by_segment/total_no*100
    return conversion_rate

def age_segmentation(df):
    df["age_group"] = df["age"].apply(
        lambda row: "[18, 30)" if row < 30 else "[30, 40)" if row < 40
            else "[40, 50)" if row < 50 else "[50, 60)" if row < 60
            else "[60, 70)" if row < 70 else '70+')
    df =df.drop(columns = "age")
    return df

def conversion_rate_simple_plot(converted_series):
    """
    :return: The line chart of conversion rate
    """
    ax = converted_series.plot(grid=True, title ="Conversion Rate")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Conversion rate %")
    plt.show()

def conversion_rate_plot(converted_series,plottype,title):
    ax = converted_series.plot(kind=plottype, figsize=(10, 7), color ="skyblue", grid=True, title=title)
    ax.set_ylabel('conversion rate (%)')
    ax.set_xlabel('age')
    plt.show()


def box_plot(data,x_axis_value,y_axis_value,showfliers):
    ax = data[[x_axis_value, y_axis_value]].boxplot(by=x_axis_value,showfliers=showfliers, figsize=(7, 5))
    ax.set_xlabel(x_axis_value)
    ax.set_ylabel(y_axis_value)
    plt.suptitle("")
    plt.show()


def pivot_table_and_plot(data,value,index_column,column):
    """
    This function compare the distribution of a filed(variable) among the output groups(Engaged vs Not Engaged)
    """
    engagement_df = pd.pivot_table(
        data, values=value, index=index_column, columns=column, aggfunc=len).fillna(0.0)
    engagement_df.columns = [str("Not " + column), str(column)]
    print(engagement_df)
    ax = engagement_df.plot(kind='pie',figsize=(15, 7), startangle=90, subplots=True, autopct=lambda x: '%0.1f%%' % x)
    plt.show()

def two_variables_conversion(df,va1,va2):
    """
    :param df: input data frame
    :param va1: first attribute
    :param va2: second attribute
    :return:
    - The table with conversion rate grouped by va1 & va2 attributes
    - The bar graph of this conversion rate
    """
    # create the table
    age_marital_df = df.groupby([va1, va2])["conversion"].sum().unstack(va2).fillna(0)
    age_marital_df = age_marital_df.divide(df.groupby(va1)["conversion"].count(),axis=0)
    print(age_marital_df)
    # plot
    ax = age_marital_df.plot(kind= "bar", grid=True, stacked = "True",figsize=(10,7)) # skip the stacked to return combine bar chart
    ax.set_title("Conversion rates by {} & {}".format(va1,va2))
    ax.set_xlabel(va1)
    ax.set_ylabel('conversion rate (%)')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv("bank-additional-full.csv", sep=";")
    # check missing value
    print(df.isnull().sum())
    # check variables type
    print(df.dtypes)
    # Length of data set
    print(df.shape[0])

    # convert output variable into 0-1 values
    df["conversion"] = df["y"].apply(lambda x: 1 if x == "yes" else 0)


    pivot_table_and_plot(df,"y","marital","conversion")

    new_df = age_segmentation(df)

    print(conversion_by_segment(new_df.groupby("age_group")))

    new_df = age_segmentation(df)
    two_variables_conversion(new_df,"age_group","marital")
