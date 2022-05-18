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
                style={"textDecoration": "none"},
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button("Stats", id="stats-pop", color="light", outline=True, style={'font-size':'22px'}),
                                    dbc.Popover(
                                        dbc.PopoverBody("My `target` is `popover-target`."),
                                        target="stats-pop",
                                        trigger="hover",
                                        placement='bottom'
                                    ),
                                ]
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button("Map", id="map-pop", color="light", outline=True, style={'font-size':'22px'}),
                                    dbc.Popover(
                                        dbc.PopoverBody("My `target` is `popover-target`."),
                                        target="map-pop",
                                        trigger="hover",
                                        placement='bottom'
                                    ),
                                ]
                            ),
                            md=3,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button("Data", id="data-pop", color="light", outline=True, style={'font-size':'22px'}),
                                    dbc.Popover(
                                        dbc.PopoverBody("My `target` is `popover-target`."),
                                        target="data-pop",
                                        trigger="hover",
                                        placement='bottom'
                                    ),
                                ]
                            ),
                            md=3,
                        )
                    ],
                    align="center",
                    style={'user-select': 'none', 'display':'flex', 'justify-content':'space-between', 'width':'100%'},
                )
            )
        ]
    ),
    color="dark",
    dark=True,
    style={'width':'100%', 'height':'80px', 'margin-bottom':'10px'}
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
            html.Div(
                [
                html.H5("Ntot ~", className="mb-n1"),
                html.Div(
                    [
                    html.Small("Data sanity : "),
                    html.Small("Clean !", className="text-success")
                    ])
                ], className="d-flex w-100 justify-content-between"),
            html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
            html.Small("Total quantity of acorns produced.")
            ], id='Ntot', action=True, active=True),

        dbc.ListGroupItem(
            [
            html.Div(
                [
                html.H5("Oneacorn ~", className="mb-n1"),
                html.Div(
                    [
                    html.Small("Data sanity : "),
                    html.Small("Clean !", className="text-success")
                    ])
                ], className="d-flex w-100 justify-content-between"),
            html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
            html.Small("Average mass of an acorn (g).")
            ], id='oneacorn', action=True),

        dbc.ListGroupItem(
            [
            html.Div(
                [
                html.H5("Ntot1 ~", className="mb-n1"),
                html.Div(
                    [
                    html.Small("Data sanity : "),
                    html.Small("Unfinished", className="text-danger")
                    ])
                ], className="d-flex w-100 justify-content-between"),
            html.Hr(style={'margin-top':'1px', 'margin-bottom':'5px'}),
            html.Small("Total quantity of acorns produced without sprouted fruit and without deteriorated acorns.")
            ], id='Ntot1', action=True),
        ],horizontal=True, className="mb-0 w-50 p-1")

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
            xaxis = dict(range=[2010, 2021], autorange=False, zeroline=False, title='Year'),
            yaxis = dict(range=[df['min'].min() - df['mean'].max(), df['max'].max() + 2*df['mean'].max()], autorange=False, zeroline=False, title=f'Average of {column}'),
            title_text = f"Average {column} over the years at the {hover} station.", hovermode="closest"))
    return fig

def histogram_figure(df):
    return px.histogram(df, x='Station', y='H', color='Station', barmode='relative', histfunc='avg', labels={'H':'tree height'})