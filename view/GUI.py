from dash import dcc, dash_table, html
import dash_bootstrap_components as dbc
import plotly.express as px

mapbox_token = "pk.eyJ1IjoidGVzdHRlc3Rlc3Rlc3RlcyIsImEiOiJjbDE3azhuZnQwNG85M2dvNHplMDZrNXBvIn0.3u58ECQNK1hoxK4gj6YObg"

def build_dropdown(options):
    return dcc.Dropdown(
                options= options,
                value='Ossau',
                id="dropdown",
            )

def init_timeseries():
    return dcc.Graph(id='timeseries')

def init_map():
    return dcc.Graph(id='map',hoverData={'points': [{'hovertext': 'Josbaig'}]})

def init_data_table():
    return html.Div(id='data_table')

def build_map(dff_map):
    px.set_mapbox_access_token(mapbox_token)
    fig = px.scatter_mapbox(dff_map, lat='Latitude', lon='Longitude', hover_name='Station',
                            color_discrete_sequence=["red"], mapbox_style="satellite-streets", zoom=5,
                            title="<b>Hover on a station to visualise timeseries and mean values</b>")
    return fig

def build_timeseries(sub_df, station_name):
    fig = px.line(sub_df, x=sub_df.index, y='Ntot', title='<b>Station: {}</b>'.format(station_name))
    return fig

def build_table(sub_df, station_name):
    return dbc.Label('Mean values for {}'.format(station_name)), dash_table.DataTable(data=sub_df.to_dict('records'))