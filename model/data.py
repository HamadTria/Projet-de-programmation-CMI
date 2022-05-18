import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_valley(con, all='Both'):
    list_valley = pd.read_sql(f'SELECT Valley FROM valley;', con)['Valley'].values.tolist()
    both = {'label':all, 'value':len(list_valley)}
    valley_and_both = [{'label':valley, 'value':value} for valley, value in zip(list_valley, range(len(list_valley)))] + [both]
    return valley_and_both

def error_Bar_data(con, column, hover):
    df = pd.read_sql(f'SELECT {column}, Year FROM harvest JOIN tree ON tree.Id_=Tree_id JOIN station ON station.Id_=Station_id WHERE Station="{hover}";', con)
    df = df.groupby(by=['Year'])[column].agg(['max', 'min', 'mean'])
    df['max'] = df['max'] - df['mean']
    df['min'] = df['mean'] - df['min']
    return df

def histogram_data(con, valley):
    query = f'SELECT Station, H FROM station JOIN valley ON valley.Id_=Valley_id JOIN tree ON station.Id_=Station_id WHERE valley="{valley}" AND H IS NOT NULL;'
    if valley == 'Both':
        query = 'SELECT Station, H FROM station JOIN valley ON valley.Id_=Valley_id JOIN tree ON station.Id_=Station_id WHERE H IS NOT NULL;'
    return pd.read_sql(query, con)