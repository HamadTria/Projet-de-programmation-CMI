from dash import Dash, html, Input, Output
import model.data
import view.GUI

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2("Geographic representation of harvest stations", className="display-4",
            style={'font-family': 'system-ui', 'font-weight': 'bold'}),
    html.P("To interact hover on a station",
           className="display-4", style={'font-family': 'system-ui'}),
    html.Div([
        html.Div([
            view.GUI.build_dropdown(model.data.get_dropdown_values('Valley')),
        ],
        style={'width': '49%', 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'})]),
    
    html.Div([
        view.GUI.init_timeseries(),
    ],
    style={ 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'}),
    html.Div([
        view.GUI.init_map(),
    ],
    style={ 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777'}),
    html.Div([
        view.GUI.init_data_table(),
    ],
    style={ 'width': '50%', 'display': 'inline-block', 'font-weight': 'bold', 'border': '1px solid black', 
    'border-radius': '4px','box-shadow': '0 10px 6px -6px #777','margin-left':'25%','margin-right':'25%'}),
])


@app.callback(
    Output('map', 'figure'),
    Input('dropdown', 'value'))
def update_map(value):
    dff_map = model.data.get_unique_values_map('Valley',value)
    fig = view.GUI.build_map(dff_map)
    return fig


@app.callback(
    Output('timeseries', 'figure'),
    Input('map', 'hoverData'))
def update_timeseries(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    sub_df = model.data.get_groupby_values_df('Station',station_name,'DD','Ntot')
    fig = view.GUI.build_timeseries(sub_df, station_name)
    return fig


@app.callback(
    Output('data_table', 'children'),
    Input('map', 'hoverData'))
def data_table(hoverData):
    station_name = hoverData['points'][0]['hovertext']
    sub_df = model.data.get_groupby_values_df('Station',station_name,'Station',('Altitude', 'SH','VH','H'))
    table = view.GUI.build_table(sub_df, station_name)
    return table


if __name__ == '__main__':
    app.run_server(debug=True)
