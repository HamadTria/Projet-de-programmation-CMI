from tkinter import MULTIPLE
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import numpy as np
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('Repro_IS.csv', sep=';')
df_map = pd.read_csv('Stations.csv', sep=';')

app.layout = html.Div([
    html.H2("Geographic representation of harvest stations", className="display-4",
            style={'font-family': 'system-ui', 'font-weight': 'bold'}),
    html.P("To interact hover on a station",
           className="display-4", style={'font-family': 'system-ui'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                options=df_map['Valley'].unique(),
                value='Ossau',
                id="dropdown",
            ),
        ],style={'width': '49%', 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'})]),
    
    html.Div([
        dcc.Graph(id='time-series'),
    ],
    style={ 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'}),
    html.Div([
        dcc.Graph(id='map',hoverData={'points': [{'hovertext': 'Josbaig'}]})
    ],
    style={ 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'}),
    html.Div([
        html.P("Mean values: "),
        html.Div(id='data_table'),
    ],
    style={ 'width': '50%', 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777','margin-left':'25%','margin-right':'25%'}),
])


@app.callback(
    Output('map', 'figure'),
    Input('dropdown', 'value'))
def update_map(value):
    px.set_mapbox_access_token(
        "pk.eyJ1IjoidGVzdHRlc3Rlc3Rlc3RlcyIsImEiOiJjbDE3azhuZnQwNG85M2dvNHplMDZrNXBvIn0.3u58ECQNK1hoxK4gj6YObg")
    dff_map = df_map[df_map['Valley'] == value]
    fig = px.scatter_mapbox(dff_map, lat='Latitude', lon='Longitude', hover_name='Station',
                            color_discrete_sequence=["red"], mapbox_style="satellite-streets", zoom=5,
                            title="<b>Hover on a station to visualise timeseries and mean values</b>")
    return fig


@app.callback(
    Output('time-series', 'figure'),
    Input('map', 'hoverData'))
def update_timeseries(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    mask = df['Station'] == station_name
    sub_df = df[mask]
    sub_df = sub_df.groupby('Year').mean()
    return px.bar(sub_df, x=sub_df.index, y='Ntot', title='<b>Station: {}</b>'.format(station_name))


@app.callback(
    Output('data_table', 'children'),
    Input('map', 'hoverData'))
def data_table(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    mask = df['Station'] == station_name
    sub_df = df[mask]
    sub_df = sub_df.groupby('Station')[
        'Altitude', 'Ntot', 'Mtot', 'oneacorn'].mean()
    return dash_table.DataTable(data=sub_df.to_dict('records'))


if __name__ == '__main__':
    app.run_server(debug=True)
