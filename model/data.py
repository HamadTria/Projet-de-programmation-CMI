import pandas as pd

df = pd.read_csv('model/Repro_IS.csv', sep=';')
df_map = pd.read_csv('model/Stations.csv', sep=';')

def get_dropdown_values(select_column):
    return df_map[select_column].unique()

def get_unique_values_map(select_column,value):
    return df_map[df_map[select_column] == value]

def get_groupby_values_df(select_column,value,groupby,select_variables):
    sub_df = df[df[select_column] == value]
    sub_df = sub_df.groupby(groupby)[select_variables].mean()
    if groupby == 'DD':
        sub_df.index.set_names(["Harvest day in julian"], inplace=True) 
        #rename the 'DD' column by 'Harvest day in julian'
    return sub_df