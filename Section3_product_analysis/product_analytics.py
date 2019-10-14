import pandas as pd
import matplotlib.pyplot as plt

def plot_by_month_year(dataset,y_label):
    ax = pd.DataFrame(dataset.values).plot(grid=True, figsize=(10, 7), legend=False)
    ax.set_xlabel('date')
    ax.set_ylabel(y_label)
    ax.set_title('Total {} over time'.format(y_label))
    ax.set_ylim([0,max(dataset.values)])

    plt.xticks(range(len(dataset.index)),[x.strftime('%m.%Y') for x in dataset.index], rotation=45)
    plt.show()

def comparision_chart(df1,df2,df3,y_label_left,y_label_right,title,lim):
    """
    :param df1: data from repeat customer
    :param df2: data from total unique customer
    :param df3: percentage values
    :param lim: set upper limit for y_axis of df1 and df2, lim must set based on higher total values
    :return:
    """
    ax1 = pd.DataFrame(df1.values).plot(grid= True, figsize=(10, 7))
    ax2_total = pd.DataFrame(df2.values).plot(grid= True,ax=ax1)
    ax3_percentage = pd.DataFrame(df3.values).plot(kind = "bar",ax=ax1,grid= True,secondary_y = True, color = "green",alpha=0.2)

    ax1.set_xlabel('date')
    ax1.set_ylabel(y_label_left)
    ax1.set_title(title)
    ax3_percentage.set_ylabel(y_label_right)
    ax1.set_ylim([0, df2.values.max() + lim])  # set range for y axis
    ax3_percentage.set_ylim([0, 100])

    ax1.legend(['From repeat customers', 'From all customers'])
    ax3_percentage.legend(['Percentage of Repeat'], loc='upper right')
    plt.xticks(
        range(len(df1.index)),[x.strftime('%m.%Y') for x in df1.index], rotation=45)
    plt.show()


if __name__ == '__main__':

    df = pd.read_excel(io="Online Retail.xlsx",sheet_name="Online Retail")

    #clean data
    #eleminate cancelled or refunded orders
    df = df.loc[df["Quantity"]> 0]
    # eliminate data from 01.12.2011
    df = df[df["InvoiceDate"] < "2011-12-01"]


    monthly_order_df = df.set_index("InvoiceDate")["InvoiceNo"].resample("M").nunique()
    print(monthly_order_df)
   # plot_by_month_year(monthly_order_df,"number of orders")

    # Calculate Revenue
    df["Sales"] = df["Quantity"] * df["UnitPrice"]


    #Create dataframe that has only one record for each purchase order/ sum up the sales of order with same invoiceNo at the same time
    invoice_customer_df = df.groupby(["InvoiceNo","InvoiceDate"]).agg({"Sales": sum,"CustomerID":min,"Country": min}).reset_index()

    monthly_unique_customers_df = df.set_index("InvoiceDate")["CustomerID"].resample("M").nunique()

    monthly_repeat_customers_df = invoice_customer_df.set_index("InvoiceDate").groupby([
        pd.Grouper(freq="M"), "CustomerID"
    ]).filter(lambda x: len(x) > 1).resample("M").nunique()["CustomerID"]

    monthly_repeat_percentage = monthly_repeat_customers_df/monthly_unique_customers_df * 100.0

    comparision_chart(monthly_repeat_customers_df,monthly_unique_customers_df,monthly_repeat_percentage,"Number of customers","Percentage %","Distribution of Repeat customer over time",100)


    monthly_revenue_df = df.set_index("InvoiceDate")["Sales"].resample("M").sum()

    monthly_revenue_repeat_customer_df = invoice_customer_df.set_index("InvoiceDate").groupby([
        pd.Grouper(freq="M"),"CustomerID"]).filter(lambda x: len(x) >1).resample("M").sum()["Sales"]

    monthly_revenue_percentage = monthly_revenue_repeat_customer_df/monthly_revenue_df * 100

    comparision_chart(monthly_revenue_repeat_customer_df,monthly_revenue_df,monthly_revenue_percentage,"Total revenue","Percentage %","Distribution of Revenue from repeat customer",100000)