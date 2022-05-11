from tkinter import Y
import plotly.express as px
import plotly.figure_factory as ff

from dash import dcc
from dash import dash_table

def build_multi_value_dropdown_menu_distplot(menu_items):
    return dcc.Dropdown(
        id="multi_value_dropdown",
        options=menu_items,
        value=menu_items,
        multi=True
    )

def build_dropdown_menu(menu_items):
    return dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in menu_items],
        value=menu_items[1],
        clearable=False,
    )

def build_dropdown_menu_multi():
    return dcc.Dropdown(
        id="dropdown6",
        options=[{"label": x, "value": x} for x in ['Range','Altitude',
        'harv','Year','Ntot1','Ntot','Mtot','oneacorn','VH','H','SH',
        'tot_Germ','M_Germ','N_Germ','rate_Germ']],
        value=['oneacorn','Ntot','Mtot'],
        multi=True
    )
def build_dropdown_menu_multi_stations():
    return dcc.Dropdown(
        id="dropdown6",
        options=[{"label": x, "value": x} for x in ['Josbaig','Le-Hourcq','Bager','Gabas','Artouste','Laveyron','Ibos','Gedre-Bas','Papillon','Peguere']],
        value=['Josbaig'],
        multi=True
    )

def init_graph_distplot():
    return dcc.Graph(id="distplot_chart")

def init_animated_bar_chart():
    return dcc.Graph(id="animated_bar_chart")

def init_scatter_matrix():
    return dcc.Graph(id="scatter_matrix")

def build_figure_distplot(df, labels):
    fig = ff.create_distplot(df, labels, bin_size=0.1)
    fig.update_layout(height=800, xaxis_title="Oneacorn mean weight (g)")
    return fig

def build_figure_animated_bar_chart(df, attributes):
    x, y, t, z = attributes
    fig = px.bar(df, x=z, y=x, animation_frame=t, animation_group=x, color=y, log_y=True)
    return fig

def build_figure_scatter_matrix(df, dims):
    fig = px.scatter_matrix(df, dimensions=df[dims], color='Station')
    return fig

def data_table(dataframe):
    return dash_table.DataTable(data=dataframe.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in dataframe.columns],
                                page_size=30,
                                sort_action="native",
                                sort_mode="multi",
                                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                                )
