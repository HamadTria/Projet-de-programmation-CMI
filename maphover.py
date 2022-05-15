from tkinter import MULTIPLE
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('Repro_IS.csv', sep=';')
df_map = pd.read_csv('Stations.csv', sep=';')

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
            options=df_map['Valley'].unique(),
            value= 'Ossau',
            id="dropdown",
            ),
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ], style={
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='map',
            hoverData={'points': [{'hovertext': 'Josbaig'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='time-series'),
    ], style={'display': 'inline-block', 'width': '49%'})
])

@app.callback(
    Output('map', 'figure'),
    Input('dropdown', 'value'))
def update_map(value):
    px.set_mapbox_access_token("pk.eyJ1IjoidGVzdHRlc3Rlc3Rlc3RlcyIsImEiOiJjbDE3azhuZnQwNG85M2dvNHplMDZrNXBvIn0.3u58ECQNK1hoxK4gj6YObg")
    dff_map = df_map[df_map['Valley'] == value]
    fig = px.scatter_mapbox(dff_map, lat='Latitude', lon='Longitude', hover_name='Station', color='Ntot')
    return fig

@app.callback(
    Output('time-series', 'figure'),
    Input('map', 'hoverData'))
def update_timeseries(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    dff = df[df['Station'] == station_name]
    #dff = dff[['Ntot']].groupby(by=['Year']).mean()
    return px.bar(dff, x='Year', y='Ntot', color='Year',title=station_name)

if __name__ == '__main__':
    app.run_server(debug=True)