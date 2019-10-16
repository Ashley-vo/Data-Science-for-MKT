import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def plot_market_size(df):
    """
    :return: The plot of market size across different promotions
    """
    # Return the count of each market size for each promotion campaign
    market_size_distribution = df.groupby(["Promotion", "MarketSize"]).count()["MarketID"]
    #Plot
    ax = market_size_distribution.unstack('MarketSize').plot(kind='bar',figsize=(12,10),grid=True,stacked=True) # skip parameter stacked for the seperate bar chard
    ax.set_title('breakdowns of market sizes across different promotions')
    plt.show()


def plot_age_of_store(df):
    age_distribution = df.groupby(['AgeOfStore', 'Promotion']).count()['MarketID']
    ax = age_distribution.unstack("Promotion").iloc[::-1].plot(kind='barh',figsize=(12,15),grid=True)
    ax.set_ylabel('age')
    ax.set_xlabel('count')
    ax.set_title('overall distributions of age of store')
    plt.show()


# Compute t-value, p_value
def t_test(s1,s2):
    """
    :param s1: sample of group 1
    :param s2: sample of group 2
    :return: t_value and p_value of statistic hypothesis
    """
    t, p = stats.ttest_ind(
                s1.values,
                s2.values,
                equal_var=False)
    return print("This is t-test result:\nt_value: {}\np_value: {}".format(t,p))


if __name__ == '__main__':
    data_frame = pd.read_csv("WA_Fn-UseC_-Marketing-Campaign-Eff-UseC_-FastF.csv", sep=",")
    plot_market_size(data_frame)
    plot_age_of_store(data_frame)

    #sample groups
    s1 = data_frame.loc[data_frame['Promotion'] == 1, 'SalesInThousands']
    s2 = data_frame.loc[data_frame['Promotion'] == 2, 'SalesInThousands']
    s3 = data_frame.loc[data_frame['Promotion'] == 3, 'SalesInThousands']


    t_test(s1,s2)
    t_test(s1,s3)
