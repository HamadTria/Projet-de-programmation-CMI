import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def call_figure(con, column, index=0):
    df = pd.read_sql(f'SELECT {column}, Year FROM harvest;', con)
    df = df.groupby(by=['Year'])[column].agg(['max', 'min', 'mean'])
    df['max'] = df['max'] - df['mean']
    df['min'] = df['mean'] - df['min']

    fig = go.Figure(
        data=[go.Scatter(
                    x = (df.index).tolist()[:index+1] if index != 0 else [(df.index).tolist()[index]],
                    y = df['mean'].iloc[:index+1] if index != 0 else [df['mean'].iloc[index]],
                    error_y = dict(
                        type = 'data',
                        symmetric = False,
                        array = df['max'].iloc[:index+1] if index != 0 else [df['max'].iloc[index]],
                        arrayminus = df['min'].iloc[:index+1] if index != 0 else [df['min'].iloc[index]]))],
        layout = go.Layout(
            xaxis = dict(range=[2010,2021], autorange=False, zeroline=False, title='Year'),
            yaxis = dict(range=[df['min'].min() - df['mean'].max(), df['max'].max() + 2*df['mean'].max()], autorange=False, zeroline=False, title=f'Mean {column}'),
            title_text = "OMG!", hovermode="closest"))
    return fig