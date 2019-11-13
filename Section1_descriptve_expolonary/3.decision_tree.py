import pandas as pd
import matplotlib.pyplot as plt
import Section2_KPI.descriptive_analysis as da
from sklearn import tree
import graphviz


def conversion_rate_df(data,groups,countvalue):
    conversion_df = pd.DataFrame(data.groupby(groups).count()[countvalue]/data.shape[0]*100)
    return conversion_df.T

def binary_to_number(data, origin_column_name,new_column):
    """
    To return dataframe with addition column: write the new_column different from origin one
    To return dataframe which only change the values without adding new column: write new_column similar to the origin
    """
    data[new_column] = data[origin_column_name].apply(lambda x: 1 if x == "yes" else 0)

def month_to_number(data):
    months_dict = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
    data["month"] = data["month"].map(months_dict)
    return data

def categorical_to_dummy(data,variable_column):
    """
    In decision tree model, it is recommended to use binary value to categorical.
    This function will encode many categorical values columns into separated binary column
    """
    encoded_df = pd.get_dummies(data[variable_column])
    encoded_df.columns = ["{}_{}".format(variable_column,x) for x in encoded_df.columns]
    new_df = pd.concat([data,encoded_df], axis=1)
    return new_df


def decision_tree_model(data, features,response_var,export_name,export_format):
    """
    :param features: list of variable as the predictor
    :param response_var: the out put variable
    :return: the display of decision tree
    """
    #Train the model
    tree_model = tree.DecisionTreeClassifier(max_depth=4,criterion="entropy")
    tree_model.fit(data[features],data[response_var])
    #Visualize the Tree
    dot_graph = tree.export_graphviz(tree_model,feature_names= features,class_names= ["0","1"],
                                filled = True, rounded=True, special_characters= True)
    graph =graphviz.Source(dot_graph,filename=export_name,format=export_format)
    graph.view()



if __name__ == '__main__':
    df = pd.read_csv("bank-full.csv",sep= ";")
    # print(df.head())
    binary_to_number(df,"y","conversion")
    print(df.head())
    print(df["balance"])
    print(conversion_rate_df(df,"conversion","y"))

    conversion_by_job = da.conversion_by_segment(df.groupby("job"))
    print(conversion_by_job)
    print(da.conversion_rate_plot(conversion_by_job, "barh",title="Conversion Rate by Job Status"))
    da.pivot_table_and_plot(df,"y","default","conversion")
    da.box_plot(df,"conversion","balance",showfliers=False)

    connversion_by_contact = da.conversion_by_segment(df.groupby("campaign"))

    month_to_number(df)
    binary_to_number(df,"housing","housing")
    binary_to_number(df,"loan","loan")

    new_df = categorical_to_dummy(df,"job")

    print(new_df)
    new_df = categorical_to_dummy(new_df,"marital")
    print(new_df.columns)

    features = ["age","balance","campaign","previous","housing",'job_admin.',
       'job_blue-collar', 'job_entrepreneur', 'job_housemaid',
       'job_management', 'job_retired', 'job_self-employed', 'job_services',
       'job_student', 'job_technician', 'job_unemployed', 'job_unknown',
       'marital_divorced', 'marital_married', 'marital_single']

    decision_tree_model(new_df,features,"conversion","decision_tree_entropy","png")





