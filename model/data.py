import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def call_figure(con, index=0):
    df = pd.read_sql('SELECT oneacorn, Year FROM harvest;', con)
    df = df.groupby(by=['Year'])['oneacorn'].agg(['max', 'min', ('mean oneacorn', 'mean')])
    df['max'] = df['max'] - df['mean oneacorn']
    df['min'] = df['mean oneacorn'] - df['min']

    fig = go.Figure(
        data=[go.Scatter(
                    x = (df.index).tolist()[:index+1] if index != 0 else [(df.index).tolist()[index]],
                    y = df['mean oneacorn'].iloc[:index+1] if index != 0 else [df['mean oneacorn'].iloc[index]],
                    error_y = dict(
                        type = 'data',
                        symmetric = False,
                        array = df['max'].iloc[:index+1] if index != 0 else [df['max'].iloc[index]],
                        arrayminus = df['min'].iloc[:index+1] if index != 0 else [df['min'].iloc[index]]))],
        layout = go.Layout(
            xaxis = dict(range=[2010,2021], autorange=False, zeroline=False, title='Year'),
            yaxis = dict(range=[-1,7], autorange=False, zeroline=False, title='Mean oneacorn'),
            title_text = "OMG!", hovermode="closest"))
    return fig