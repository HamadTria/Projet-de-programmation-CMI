import model.data
import view.GUI

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SKETCHY], suppress_callback_exceptions=True)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Rendu Projet CMI", className="display-4",
                style={'font-family': 'system-ui'}),
        html.Hr(),
        html.P(
            "Forêt Pyrénnées", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Displot chart",
                            href="/", active="exact"),
                dbc.NavLink("Animated bar chart",
                            href="/animated_bar_chart", active="exact"),
                dbc.NavLink("Scatter matrix",
                            href="/scatter_matrix", active="exact"),
                dbc.NavLink("Tableur", href="/table", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):

    if pathname == "/":
        multi_value_dropdown = view.GUI.build_multi_value_dropdown_menu_distplot(
            model.data.get_unique_values('Station'))
        graph = view.GUI.init_graph_distplot()
        return [
            html.Div([
                multi_value_dropdown
            ]),
            html.Hr(style={'width': '100%', 'align': 'center'}),
            html.H1('Le distplot affiche une combinaison de représentations statistiques de données numériques. Un histogramme, un graphique kde et un graphique rugueux sont affichés.', id='line_view',
                    style={'textAlign': 'center', 'marginTop': '10px', 'font-size': '1.5rem'}),
            html.Div([
                graph
            ])
        ]

    if pathname == "/animated_bar_chart":
        dropdown = view.GUI.build_dropdown_menu(
            model.data.get_unique_values('Valley'))
        graph = view.GUI.init_animated_bar_chart()
        return [
            html.H1("Figure: animated bar chart, répartition de la quantité de glands produits (Ntot) en fonction de la station.",
                    style={'textAlign': 'center', 'font-family': 'system-ui'}),
            html.Div([
                dropdown, graph
            ]),
            html.P("Description: représentation plus interactive, le animated-bar-chart donne la possibilité de faire avancer une variable (les années par exemple) grâce à une animation. Le code couleur rajoute une information supplémentaire (ici le volume du houppier). Le drop down permet de sélectionner la vallée désirée.",
                   style={'textAlign': 'left', 'font-family': 'system-ui', 'font-weight': 'normal'})
        ]

    if pathname == "/scatter_matrix":
        dropdown = view.GUI.build_dropdown_menu_multi()
        graph = view.GUI.init_scatter_matrix()
        return [
            html.H1("Figure: scatter matrix.",
                    style={'textAlign': 'center', 'font-family': 'system-ui'}),
            html.Div([
                dropdown, graph
            ]),
            html.P("Description: pour le scatter matrix, le choix des variables est laissé à l'utilisateur. Grâce au multiple-drop-down, il est possible de sélectionner des variables et un scatter-plot sera générer. Libre à l'utilisateur de trouver les corrélations les plus pertinentes!",
                   style={'textAlign': 'left', 'font-family': 'system-ui', 'font-weight': 'normal'})
        ]

    if pathname == "/table":
        # fetch client info
        return [
            html.H1('Données forêt pyrénnées (tableur)', id='table_view',
                    style={'textAlign': 'left', 'font-family': 'system-ui'}),
            html.Hr(style={'width': '75%', 'align': 'center'}),
            html.Div(id='data_table', children=view.GUI.data_table(model.data.df))
        ]

    else:
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


@app.callback(
    Output("distplot_chart", "figure"),
    [Input("multi_value_dropdown", "value")])
def update_distplot_chart(multi_value_dropdown):
    sub_df = model.data.extract_df_distplot(multi_value_dropdown)
    return view.GUI.build_figure_distplot(sub_df, multi_value_dropdown)


@app.callback(
    Output("animated_bar_chart", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(value):
    sub_df, attributes = model.data.extract_df_animated_bar_chart(
        value, 'Valley')
    return view.GUI.build_figure_animated_bar_chart(sub_df, attributes)


@app.callback(
    Output("scatter_matrix", "figure"),
    [Input("dropdown6", "value")])
def update_bar_chart(dims):
    sub_df = model.data.extract_df_scatter_matrix()
    return view.GUI.build_figure_scatter_matrix(sub_df, dims)


if __name__ == '__main__':
    app.run_server(debug=True)
