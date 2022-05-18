from turtle import width
from click import style
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash_extensions import Lottie
mapbox_token = "pk.eyJ1IjoidGVzdHRlc3Rlc3Rlc3RlcyIsImEiOiJjbDE3azhuZnQwNG85M2dvNHplMDZrNXBvIn0.3u58ECQNK1hoxK4gj6YObg"

def navbar():
    return dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='../assets/image/logo.png', height="30px")),
                        dbc.Col(dbc.NavbarBrand("Home", className="ms-2")),
                    ],
                    align="center",
                    className="g-0 h-10 p-1 text-white bg-success rounded-3",
                ),
                href="/",
                className='text'
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Button("Stats", className='main_button', href="/stats", id="stats-pop", color="light", outline=True),
                                dbc.Popover(
                                    dbc.PopoverBody("Statistical data visualization"),
                                    target="stats-pop",
                                    trigger="hover",
                                    placement='bottom'
                                )
                            ],
                            className='Col'
                        ),
                        dbc.Col(
                            [
                                dbc.Button("Map", className='main_button', href="/map", id="map-pop", color="light", outline=True),
                                dbc.Popover(
                                    dbc.PopoverBody("Visualization on a map"),
                                    target="map-pop",
                                    trigger="hover",
                                    placement='bottom'
                                )
                            ],
                            className='Col'
                        ),
                        dbc.Col(
                            [
                                dbc.Button("Data", className='main_button', href="/data", id="data-pop", color="light", outline=True),
                                dbc.Popover(
                                    dbc.PopoverBody("Data visualizer"),
                                    target="data-pop",
                                    trigger="hover",
                                    placement='bottom'
                                )
                            ],
                            className='Col'
                        )
                    ],
                    align="center",
                    className='items'
                )
            )
        ]
    ),
    color="dark",
    dark=True,
    className='navbar_container'
)

def button_group(options):
    return html.Div(
    [
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=options,
            value=0,
        ),
    ],
    className="radio-group",
)

def list_group():
    return dbc.ListGroup(
        [
        dbc.ListGroupItem(
            [
                html.Div([
                    html.Img(src='../assets/image/leaf.png', height='25px'),
                    html.H5("Ntot", className="mb-n1 text")
                ], className='inline'),
                html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
                html.Small("Total quantity of acorns produced.", className='text')
            ],
            id='Ntot', action=True, active=True, className='list_group_item'),

        dbc.ListGroupItem(
            [
                html.Div([
                    html.Img(src='../assets/image/leaf.png', height='25px'),
                    html.H5("Oneacorn", className="mb-n1 text"),
                ], className='inline'),
                html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
                html.Small("Average mass of an acorn (g).", className='text')
            ],
            id='oneacorn', action=True, className='list_group_item'),

        dbc.ListGroupItem(
            [
                html.Div([
                    html.Img(src='../assets/image/leaf.png', height='25px'),
                    html.H5("Ntot1", className="mb-n1 text"),
                ], className='inline'),
                html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
                html.Small("Total quantity of acorns produced without sprouted fruit and without deteriorated acorns.", className='text')
            ],
            id='Ntot1', action=True, className='list_group_item'),
        ],horizontal=True)

def error_Bar_figure(df, column, index, hover):
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
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis = dict(range=[2010, 2021], autorange=False, zeroline=False, title='Year'),
            yaxis = dict(range=[df['min'].min() - df['mean'].max(), df['max'].max() + 2*df['mean'].max()], autorange=False, zeroline=False, title=f'Average of {column}'),
            title_text = f"Average {column} over the years at the {hover} station. (Fly over another station)", hovermode="closest"))
    return fig

def histogram_figure(df):
    fig = px.histogram(df, x='Station', y='H', color='Station', barmode='relative', histfunc='avg', labels={'H':'tree height'})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

def build_dropdown(options):
    return dcc.Dropdown(options= options, value='Ossau', id="dropdown")

def lottie(url):
    return Lottie(
        options=dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice')),
        width="50%", url=url)

def init_figure(name, nameClass=''):
    return dcc.Graph(id=name, className=nameClass)

def init_map():
    return dcc.Graph(id='map',hoverData={'points': [{'hovertext': 'Josbaig'}]})

def build_map(dff_map):
    px.set_mapbox_access_token(mapbox_token)
    fig = px.scatter_mapbox(dff_map, lat='Latitude', lon='Longitude', hover_name='Station',
                            color_discrete_sequence=["red"], mapbox_style="satellite-streets", zoom=5,
                            title="<b>Hover on a station to visualise timeseries and mean values</b>")
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

def build_timeseries(sub_df, station_name):
    fig = px.line(sub_df, x=sub_df.index, y='Ntot', title='<b>Station: {}</b>'.format(station_name))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

def build_table(sub_df, station_name):
    table = dbc.Label('Mean values for {}'.format(station_name), style={'font-weight': 'bold'}), dash_table.DataTable(data=sub_df.to_dict('records'))
    return table
