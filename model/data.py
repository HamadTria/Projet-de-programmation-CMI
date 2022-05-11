import pandas as pd

df = pd.read_csv('model/Repro_IS.csv', sep=';')
select_column = 'Valley'
select_column2 = 'Year'

def get_unique_values():
    return df[select_column].unique()

def get_unique_values_displot(column):
    return df[column].unique()

def extract_df_distplot(dims):
    return [df[(df['Station'] == Station) & (df['oneacorn'].notna())]['oneacorn'].to_numpy() for Station in dims]

def extract_df_animated_bar_chart(value):
    mask = df[select_column] == value
    df_valley = df[mask]
    # attributes used to specify grouping (and view)
    x_att = 'Ntot'
    y_att = 'VH'
    t_att = 'Year'
    z_att = 'Station'

    df_agreg = df_valley[[x_att, y_att, t_att, z_att]].sort_values(by=[t_att],ascending=True)
    df_agreg = df_valley[[x_att, y_att, t_att, z_att]].groupby(by=[z_att, t_att]).sum()
    df_agreg = df_agreg.reset_index()

    if value == 'Luz':
        mask = df_agreg['Year'] != 2011 
        df_agreg = df_agreg[mask]
    
    if value == 'Ossau':
        mask = df_agreg['Year'] != 2011
        df_agreg = df_agreg[mask]
        mask = df_agreg['Year'] != 2013
        df_agreg = df_agreg[mask]
    return df_agreg, (x_att, y_att, t_att, z_att)

def extract_df_scatter_matrix():
    return df