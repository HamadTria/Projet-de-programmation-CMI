from turtle import width
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html

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
                html.H5("Ntot", className="mb-n1 text"),
                html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
                html.Small("Total quantity of acorns produced.", className='text')
            ],
            id='Ntot', action=True, active=True, className='list_group_item'),

        dbc.ListGroupItem(
            [
                html.H5("Oneacorn", className="mb-n1 text"),
                html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
                html.Small("Average mass of an acorn (g).", className='text')
            ],
            id='oneacorn', action=True, className='list_group_item'),

        dbc.ListGroupItem(
            [
                html.H5("Ntot1", className="mb-n1 text"),
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
            title_text = f"Average {column} over the years at the {hover} station.", hovermode="closest"))
    return fig

def histogram_figure(df):
    fig = px.histogram(df, x='Station', y='H', color='Station', barmode='relative', histfunc='avg', labels={'H':'tree height'})
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

def empty_graph():
    return go.Figure(
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )